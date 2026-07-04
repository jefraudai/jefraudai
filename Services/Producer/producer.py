import socket
import os
import time
import requests
import json
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_USERNAME          = os.getenv("KAFKA_USERNAME") or "producer"
KAFKA_TOPIC             = os.getenv("KAFKA_TOPIC")
API_URL                 = os.getenv("API_URL")
POLL_INTERVAL_SECONDS   = int(os.getenv("POLL_INTERVAL_SECONDS"))

#Test de connexion au cluster Kafka Redpanda en local
#load_dotenv(find_dotenv(".env"), override=True)      # config
#load_dotenv(find_dotenv(".env.secrets"), override=True)   # secrets only useful on local environment

# SSL configuration for Aiven
producer_config = {
  "bootstrap_servers": KAFKA_BOOTSTRAP_SERVERS,
  "security_protocol": "SASL_SSL",
  "sasl_mechanism": "SCRAM-SHA-256",
  "sasl_plain_username": KAFKA_USERNAME,
  "sasl_plain_password": os.environ["KAFKA_PASSWORD"],
  "ssl_check_hostname": False,  # Disable hostname verification for Aiven
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
    producer_config["ssl_cafile"] = ca_path

access_cert = os.getenv("KAFKA_ACCESS_CERT")
access_key = os.getenv("KAFKA_ACCESS_KEY")
if access_cert and access_key:
    cert_path = write_cert_to_file(access_cert, ".crt")
    key_path = write_cert_to_file(access_key, ".key")
    if cert_path != access_cert:
        cert_files.append(cert_path)
    if key_path != access_key:
        cert_files.append(key_path)
    producer_config["ssl_certfile"] = cert_path
    producer_config["ssl_keyfile"] = key_path

producer = KafkaProducer(**producer_config)
hostname = str.encode(socket.gethostname())

def on_success(metadata):
  print(f"Sent to topic '{metadata.topic}' at offset {metadata.offset}")

def on_error(e):
  print(f"Error sending message: {e}")

def fetch_transaction() -> dict | None:
  try:
      response = requests.get(API_URL, timeout=10)
      response.raise_for_status()      
      payload = response.json()      
      # L'API retourne parfois une string JSON encodée deux fois
      if isinstance(payload, str):
          import json
          payload = json.loads(payload)
          
      columns = payload["columns"]
      data    = payload["data"][0]
      transaction = dict(zip(columns, data))
      if "trans_date_trans_time" not in transaction and "current_time" in transaction:
          try:
              timestamp_ms = int(transaction["current_time"])
              transaction["trans_date_trans_time"] = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
          except Exception as e:
              print(f"[PRODUCER] Impossible de convertir current_time en trans_date_trans_time: {e}")
      return transaction
  except requests.exceptions.RequestException as e:
      print(f"[PRODUCER] Erreur API : {e}")
      return None
  except (KeyError, IndexError) as e:
      print(f"[PRODUCER] Format de réponse inattendu : {e}")
      return None

# Produce n messages asynchronously
for i in range(1000):
  transaction = fetch_transaction()
  if transaction:
    trans_num = transaction.get("trans_num", "unknown")
    print(f"[PRODUCER] Transaction récupérée : {trans_num} | montant={transaction.get('amt')} | marchand={transaction.get('merchant')}")
    future = producer.send(
      KAFKA_TOPIC,
      key=trans_num.encode("utf-8"),
      value=json.dumps(transaction).encode("utf-8")
    )
    future.add_callback(on_success)
    future.add_errback(on_error)
  else:
    print(f"[PRODUCER] Aucune transaction récupérée pour le message #{i}")
    time.sleep(POLL_INTERVAL_SECONDS)

producer.flush()
producer.close()