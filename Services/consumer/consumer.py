import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaException, KafkaError, OFFSET_BEGINNING, OFFSET_END, TopicPartition
from sqlalchemy import create_engine, text

from fraud_detection.configuration import get_mlflow_config, load_config

try:
    from fraud_detection.data.data_transformer import clean_data
    from fraud_detection.models.inference_model import InferenceModel
    _HAS_FRAUD_LIB = True
except ImportError:
    clean_data = None
    InferenceModel = None
    _HAS_FRAUD_LIB = False

load_dotenv()

config = load_config()
mlflow_config = get_mlflow_config(config)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_USERNAME          = os.getenv("KAFKA_USERNAME") or "consumer"
KAFKA_TOPIC_IN          = os.getenv("KAFKA_TOPIC_IN")
KAFKA_TOPIC_OUT         = os.getenv("KAFKA_TOPIC_OUT")
MLFLOW_TRACKING_URI     = mlflow_config.get("tracking_uri")
MLFLOW_MODEL_URI        = os.getenv("MLFLOW_MODEL_URI")
MLFLOW_MODEL_NAME       = os.getenv("MLFLOW_MODEL_NAME") or mlflow_config.get("model_name")
MLFLOW_EXPERIMENT_NAME  = mlflow_config.get("experiment_name")
MLFLOW_PROD_ALIAS       = os.getenv("MLFLOW_PROD_ALIAS") or mlflow_config.get("prod_alias") or "prod"
DB_URI                  = os.getenv("POSTGRES_URI")
SMTP_USER               = os.getenv("SMTP_USER")
ALERT_TO                = os.getenv("ALERT_TO")
KAFKA_GROUP_ID          = os.getenv("KAFKA_GROUP_ID", "fraud-consumer-group")
KAFKA_AUTO_OFFSET_RESET = os.getenv("KAFKA_AUTO_OFFSET_RESET", "latest")

def preprocess(transaction: dict) -> pd.DataFrame:
    """Prépare les données de transaction en utilisant uniquement clean_data."""
    df = pd.DataFrame([transaction])

    if _HAS_FRAUD_LIB:
        try:
            df = clean_data(df)
            print(f"[CONSUMER] data prétraitée : {df.columns.tolist()}")
        except Exception as e:
            print(f"[CONSUMER] clean_data error: {e}")

    return df


def infer_model_name(model_uri):
    if not model_uri:
        return None
    if model_uri.startswith("models:/"):
        model_part = model_uri.split("models:/", 1)[1]
        if "@" in model_part:
            model_part = model_part.split("@", 1)[0]
        return model_part
    return None


def get_valid_offset(consumer, topic, partition, requested_offset):
    try:
        tp = TopicPartition(topic, partition)
        low, high = consumer.get_watermark_offsets(tp)
        # Some brokers may return negative watermarks when unavailable
        if low is None or low < 0:
            low = 0
        if high is None or high <= 0:
            print(f"[CONSUMER] Aucune watermark valide pour {topic}:{partition}, fallback sur {KAFKA_AUTO_OFFSET_RESET}")
            return OFFSET_BEGINNING if KAFKA_AUTO_OFFSET_RESET == "earliest" else OFFSET_END

        # `high` is the upper watermark (last_offset + 1). Max valid offset is high - 1
        max_valid = high - 1
        if requested_offset < low:
            return low
        if requested_offset > max_valid:
            print(f"[CONSUMER] Requested offset {requested_offset} > max valid {max_valid}, using {max_valid}")
            return max_valid
        return requested_offset
    except Exception as e:
        print(f"[CONSUMER] Erreur watermark pour {topic}:{partition} : {e}")
        return OFFSET_BEGINNING if KAFKA_AUTO_OFFSET_RESET == "earliest" else OFFSET_END


def on_assign(consumer, partitions):
    print(f"[CONSUMER] Partitions assignées : {[f'{p.topic}:{p.partition}' for p in partitions]}")
    committed = consumer.committed(partitions, timeout=10.0)
    for idx, p in enumerate(partitions):
        committed_partition = committed[idx] if committed and idx < len(committed) else None
        if committed_partition is None or committed_partition.offset < 0:
            start_offset = OFFSET_BEGINNING if KAFKA_AUTO_OFFSET_RESET == "earliest" else OFFSET_END
            print(f"[CONSUMER] Aucun offset committé pour {p.topic}:{p.partition}, positionnement sur {start_offset}")
            partitions[idx].offset = start_offset
        else:
            valid_offset = get_valid_offset(consumer, p.topic, p.partition, committed_partition.offset)
            if valid_offset != committed_partition.offset:
                print(f"[CONSUMER] Offset committé invalide {p.topic}:{p.partition} {committed_partition.offset} -> {valid_offset}")
            partitions[idx].offset = valid_offset
    consumer.assign(partitions)


# Envoie Email d'alerte en cas de fraude détectée
def send_alert_email(transaction: dict, score: float):
    if not SMTP_USER or not ALERT_TO:
        print("[CONSUMER] Email non configuré, alerte ignorée")
        return

    trans_num = transaction.get("trans_num", "N/A")
    amt       = transaction.get("amt", "N/A")
    merchant  = transaction.get("merchant", "N/A")
    city      = transaction.get("city", "N/A")
    state     = transaction.get("state", "N/A")

    subject = f"[ALERTE FRAUDE] Transaction {trans_num}"
    body = f"""
    Une transaction suspecte a été détectée.

    Transaction : {trans_num}
    Montant     : ${amt}
    Marchand    : {merchant}
    Lieu        : {city}, {state}
    Score fraude: {score:.4f}
    Heure       : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """

    msg = MIMEMultipart()
    msg["From"]    = SMTP_USER
    msg["To"]      = ALERT_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    
    try:
        from resend_client import ResendClient
        client = ResendClient()
        result = client.send_email(
            from_email=msg["From"],
            to=msg["To"],
            subject=msg["Subject"],
            html=msg.as_string(),
        )
        print("E-mail envoyé avec succès!")
        print(result)
    except Exception as e:
        print(f"[CONSUMER] Echec envoi email : {e}")


# Stockage des résultats dans PostgreSQL
def save_to_postgres(engine, transaction: dict, is_fraud_pred: int, fraud_score: float):
    query = text("""
        INSERT INTO predictions
            (trans_num, cc_num, merchant, category, amt, city, state,
             is_fraud_true, is_fraud_pred, fraud_score)
        VALUES
            (:trans_num, :cc_num, :merchant, :category, :amt, :city, :state,
             :is_fraud_true, :is_fraud_pred, :fraud_score)
        ON CONFLICT (trans_num) DO NOTHING
    """)
    with engine.connect() as conn:
        conn.execute(query, {
            "trans_num":     transaction.get("trans_num"),
            "cc_num":        transaction.get("cc_num"),
            "merchant":      transaction.get("merchant"),
            "category":      transaction.get("category"),
            "amt":           transaction.get("amt"),
            "city":          transaction.get("city"),
            "state":         transaction.get("state"),
            "is_fraud_true": transaction.get("is_fraud", -1),
            "is_fraud_pred": is_fraud_pred,
            "fraud_score":   fraud_score,
        })
        conn.commit()

def create_predictions_table(engine):
    ddl = """
    CREATE TABLE IF NOT EXISTS predictions (
        trans_num TEXT PRIMARY KEY,
        cc_num TEXT,
        merchant TEXT,
        category TEXT,
        amt NUMERIC,
        city TEXT,
        state TEXT,
        is_fraud_true INTEGER,
        is_fraud_pred INTEGER,
        fraud_score DOUBLE PRECISION,
        predicted_at TIMESTAMP DEFAULT now()
    );
    """
    with engine.connect() as conn:
        conn.execute(text(ddl))
        conn.commit()


# Main
def main():
    if InferenceModel is None:
        print("[CONSUMER] Impossible d'importer InferenceModel, vérifiez le package fraud_detection")
        return

    model_name = MLFLOW_MODEL_NAME or infer_model_name(MLFLOW_MODEL_URI)
    if not model_name:
        print("[CONSUMER] Nom du modèle MLflow non défini")
        return

    print(f"[CONSUMER] Chargement du modèle MLflow '{model_name}' via alias '{MLFLOW_PROD_ALIAS}'")
    inference_model = InferenceModel(
        mlflow_tracking_uri=MLFLOW_TRACKING_URI,
        experiment_name=MLFLOW_EXPERIMENT_NAME,
    )
    if not inference_model.load_production_model(model_name, alias_prod=MLFLOW_PROD_ALIAS):
        print("[CONSUMER] Échec du chargement du modèle en production")
        return
    print(f"[CONSUMER] Modèle chargé avec succès : {inference_model.get_model_info()}")

    engine = create_engine(DB_URI)
    create_predictions_table(engine)
    print("[CONSUMER] Connexion PostgreSQL établie")
 
    # SSL configuration for Aiven
    consumer_config = {
        "bootstrap.servers":  KAFKA_BOOTSTRAP_SERVERS,
        "security.protocol": "SASL_SSL",
        "sasl.mechanism": "SCRAM-SHA-256",
        "sasl.username": KAFKA_USERNAME,
        "sasl.password": os.environ["KAFKA_PASSWORD"],
        "group.id":           KAFKA_GROUP_ID,
        "auto.offset.reset":  KAFKA_AUTO_OFFSET_RESET,
        "enable.auto.commit": True,
        "isolation.level":    "read_committed",  # Lire uniquement les messages confirmés
        "session.timeout.ms": 30000,  # 30 secondes pour détecter les pannes
        "ssl.endpoint.identification.algorithm": "none",  # Disable hostname verification
    }
    
    # Helper to write certificate content to temp file
    def write_cert_to_file(content, suffix):
        if not content or content.startswith("/"):
            return content  # Already a path or empty
        import tempfile
        fd, path = tempfile.mkstemp(suffix=suffix, text=True)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return path
    
    # Add mTLS certificates if provided (for Aiven)
    cert_files = []
    ca_cert = os.getenv("KAFKA_CA_CERT")
    if ca_cert:
        ca_path = write_cert_to_file(ca_cert, ".crt")
        if ca_path != ca_cert:
            cert_files.append(ca_path)
        consumer_config["ssl.ca.location"] = ca_path
    
    access_cert = os.getenv("KAFKA_ACCESS_CERT")
    access_key = os.getenv("KAFKA_ACCESS_KEY")
    if access_cert and access_key:
        cert_path = write_cert_to_file(access_cert, ".crt")
        key_path = write_cert_to_file(access_key, ".key")
        if cert_path != access_cert:
            cert_files.append(cert_path)
        if key_path != access_key:
            cert_files.append(key_path)
        consumer_config["ssl.certificate.location"] = cert_path
        consumer_config["ssl.key.location"] = key_path
    
    consumer = Consumer(consumer_config)
    consumer.subscribe([KAFKA_TOPIC_IN], on_assign=on_assign)
    print(f"[CONSUMER] Abonné au topic : {KAFKA_TOPIC_IN} [group={KAFKA_GROUP_ID}]")
 
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
 
            if msg is None:
                continue
            if msg.error():
                error = msg.error()
                if error.code() == KafkaError.OFFSET_OUT_OF_RANGE:
                    print(f"[CONSUMER] ERREUR OFFSET : {error}")
                    partitions = consumer.assignment()
                    if partitions:
                        committed = consumer.committed(partitions, timeout=10.0)
                        for idx, p in enumerate(partitions):
                            committed_partition = committed[idx] if committed and idx < len(committed) else None
                            requested_offset = committed_partition.offset if committed_partition and committed_partition.offset >= 0 else 0
                            valid_offset = get_valid_offset(consumer, p.topic, p.partition, requested_offset)
                            print(f"[CONSUMER] Réinitialisation offset {p.topic}:{p.partition} -> {valid_offset}")
                            p.offset = valid_offset
                        consumer.assign(partitions)
                        continue
                    print("[CONSUMER] Aucune partition assignée pour réinitialiser l'offset")
                    continue
                raise KafkaException(error)
 
            transaction  = json.loads(msg.value().decode("utf-8"))
            trans_num    = transaction.get("trans_num", "unknown")
            print(f"[CONSUMER] Message reçu : {trans_num}")
 
            features      = preprocess(transaction)
            predictions, confidence_scores = inference_model.predict(features)
            if predictions is None:
                print(f"[CONSUMER] Échec de prédiction pour {trans_num}")
                continue

            pred_value = int(np.asarray(predictions).ravel()[0])
            if confidence_scores is not None:
                fraud_score = float(np.asarray(confidence_scores).ravel()[0])
                is_fraud_pred = 1 if fraud_score >= 0.5 else 0
            else:
                fraud_score = float(pred_value)
                is_fraud_pred = pred_value
            print(f"[CONSUMER] {trans_num} | score={fraud_score:.4f} | is_fraud={is_fraud_pred}")
 
            result = {
                "trans_num":     trans_num,
                "amt":           transaction.get("amt"),
                "merchant":      transaction.get("merchant"),
                "category":      transaction.get("category"),
                "is_fraud_pred": is_fraud_pred,
                "fraud_score":   fraud_score,
                "predicted_at":  datetime.now().isoformat(),
            }
 
            save_to_postgres(engine, transaction, is_fraud_pred, fraud_score)
 
            if is_fraud_pred == 1:
                print(f"[CONSUMER] FRAUDE DETECTEE : {trans_num} (score={fraud_score:.4f})")
                send_alert_email(transaction, fraud_score)
 
    except KeyboardInterrupt:
        print("[CONSUMER] Arrêt")
    finally:
        consumer.close()
        engine.dispose()


main()
