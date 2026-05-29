import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaException
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
KAFKA_TOPIC_IN          = os.getenv("KAFKA_TOPIC_IN")
KAFKA_TOPIC_OUT         = os.getenv("KAFKA_TOPIC_OUT")
MLFLOW_TRACKING_URI     = mlflow_config.get("tracking_uri")
MLFLOW_MODEL_URI        = os.getenv("MLFLOW_MODEL_URI")
MLFLOW_MODEL_NAME       = os.getenv("MLFLOW_MODEL_NAME")
MLFLOW_EXPERIMENT_NAME  = mlflow_config.get("experiment_name")
MLFLOW_PROD_ALIAS       = mlflow_config.get("prod_alias")
DB_URI                  = os.getenv("POSTGRES_URI")
SMTP_USER               = os.getenv("SMTP_USER")
ALERT_TO                = os.getenv("ALERT_TO")

def preprocess(transaction: dict) -> pd.DataFrame:
    """Prépare les données de transaction en utilisant uniquement clean_data."""
    df = pd.DataFrame([transaction])

    if _HAS_FRAUD_LIB:
        try:
            df = clean_data(df)
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

    print("E-mail envoyé avec succès!")
    try:
        from resend_client import ResendClient
        client = ResendClient()
        result = client.send_email(
            from_email=msg["From"],
            to=msg["To"],
            subject=msg["Subject"],
            html=msg.as_string(),
        )
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
    inference_model = InferenceModel(MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME)
    if not inference_model.load_production_model(model_name, alias_prod=MLFLOW_PROD_ALIAS):
        print("[CONSUMER] Échec du chargement du modèle en production")
        return
    print(f"[CONSUMER] Modèle chargé avec succès : {inference_model.get_model_info()}")

    engine = create_engine(DB_URI)
    print("[CONSUMER] Connexion PostgreSQL établie")
 
    consumer = Consumer({
        "bootstrap.servers":  KAFKA_BOOTSTRAP_SERVERS,
        "group.id":           "fraud-consumer-group",
        "auto.offset.reset":  "latest",
        "enable.auto.commit": True,
    })
    consumer.subscribe([KAFKA_TOPIC_IN])
    print(f"[CONSUMER] Abonné au topic : {KAFKA_TOPIC_IN}")
 
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
 
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
 
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
