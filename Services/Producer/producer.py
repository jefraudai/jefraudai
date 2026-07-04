import socket
import os
import time
import requests
import json
from datetime import datetime
from confluent_kafka import Producer, KafkaException

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_USERNAME          = os.getenv("KAFKA_USERNAME") or "avnadmin"
KAFKA_TOPIC             = os.getenv("KAFKA_TOPIC")
API_URL                 = os.getenv("API_URL")
POLL_INTERVAL_SECONDS   = int(os.getenv("POLL_INTERVAL_SECONDS"))

#Test de connexion au cluster Kafka Redpanda en local
#load_dotenv(find_dotenv(".env"), override=True)      # config
#load_dotenv(find_dotenv(".env.secrets"), override=True)   # secrets only useful on local environment

# SSL configuration for Aiven
producer_config = {
  "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
  "security.protocol": "SASL_SSL",
  "sasl.mechanism": "PLAIN",
  "sasl.username": KAFKA_USERNAME,
  "sasl.password": os.environ["KAFKA_PASSWORD"],
  "ssl.endpoint.identification.algorithm": "none",
  "enable.ssl.certificate.verification": False,
  # Timeout configurations
  "socket.timeout.ms": 10000,
  "request.timeout.ms": 30000,
  "delivery.timeout.ms": 120000,
  "message.timeout.ms": 120000,
  "reconnect.backoff.ms": 1000,
  "reconnect.backoff.max.ms": 10000,
  # Connection retries
  "message.send.max.retries": 5,
  "retry.backoff.ms": 100,
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
# Note: CA verification is disabled, so KAFKA_CA_CERT is not used
cert_files = []
access_cert = os.getenv("KAFKA_ACCESS_CERT")
access_key = os.getenv("KAFKA_ACCESS_KEY")
if access_cert and access_key:
    cert_path = write_cert_to_file(access_cert, ".crt")
    key_path = write_cert_to_file(access_key, ".key")
    if cert_path != access_cert:
        cert_files.append(cert_path)
    if key_path != access_key:
        cert_files.append(key_path)
    producer_config["ssl.certificate.location"] = cert_path
    producer_config["ssl.key.location"] = key_path

def test_network_connectivity(host, port, timeout=5):
    """Test basic TCP connectivity to a broker."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            print(f"[PRODUCER] Network connectivity OK: {host}:{port}")
            return True
        else:
            print(f"[PRODUCER] Network connectivity FAILED: {host}:{port} (error code: {result})")
            return False
    except Exception as e:
        print(f"[PRODUCER] Network connectivity error for {host}:{port}: {e}")
        return False

def diagnose_kafka_connection():
    """Diagnose Kafka connection issues."""
    print("[PRODUCER] === Kafka Connection Diagnostics ===")
    print(f"[PRODUCER] Bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"[PRODUCER] Username: {KAFKA_USERNAME}")
    print(f"[PRODUCER] Topic: {KAFKA_TOPIC}")
    
    # Test each broker
    brokers = KAFKA_BOOTSTRAP_SERVERS.split(",")
    for broker in brokers:
        # Parse host:port from sasl_ssl://host:port
        if "://" in broker:
            broker = broker.split("://")[1]
        if ":" in broker:
            host, port = broker.split(":")
            port = int(port)
            test_network_connectivity(host, port)
    print("[PRODUCER] === End Diagnostics ===")

producer = Producer(producer_config)
hostname = str.encode(socket.gethostname())

def verify_connection(producer, timeout=30):
    """Verify Kafka connection by triggering metadata refresh."""
    try:
        producer.poll(timeout=0)
        cluster_metadata = producer.list_topics(timeout=timeout)
        print(f"[PRODUCER] Connection verified. Cluster ID: {cluster_metadata.cluster_id}")
        return True
    except Exception as e:
        print(f"[PRODUCER] Connection verification failed: {e}")
        return False

def delivery_report(err, msg):
  """Called once for each produced message to indicate delivery result."""
  if err is not None:
    print(f"[PRODUCER] Error delivering message: {err}")
  else:
    print(f"[PRODUCER] Sent to topic '{msg.topic()}' [{msg.partition()}] at offset {msg.offset()}")

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

# Run diagnostics before connection verification
diagnose_kafka_connection()

# Verify connection before starting
if not verify_connection(producer):
    print("[PRODUCER] WARNING: Connection verification failed. Proceeding anyway...")

# Produce n messages asynchronously
for i in range(1000):
  transaction = fetch_transaction()
  if transaction:
    trans_num = transaction.get("trans_num", "unknown")
    print(f"[PRODUCER] Transaction récupérée : {trans_num} | montant={transaction.get('amt')} | marchand={transaction.get('merchant')}")
    try:
        producer.produce(
          KAFKA_TOPIC,
          key=trans_num.encode("utf-8"),
          value=json.dumps(transaction).encode("utf-8"),
          callback=delivery_report
        )
        producer.poll(0)  # Trigger delivery reports
    except KafkaException as e:
        print(f"[PRODUCER] Kafka error producing message: {e}")
        print(f"[PRODUCER] Retrying connection verification...")
        if verify_connection(producer, timeout=10):
            print(f"[PRODUCER] Connection recovered, retrying message")
            try:
                producer.produce(
                  KAFKA_TOPIC,
                  key=trans_num.encode("utf-8"),
                  value=json.dumps(transaction).encode("utf-8"),
                  callback=delivery_report
                )
                producer.poll(0)
            except Exception as retry_e:
                print(f"[PRODUCER] Retry failed: {retry_e}")
        else:
            print(f"[PRODUCER] Connection still unavailable, skipping message")
  else:
    print(f"[PRODUCER] Aucune transaction récupérée pour le message #{i}")
  # Always sleep to respect API rate limit (5 calls/minute = 12 seconds minimum)
  time.sleep(POLL_INTERVAL_SECONDS)

# Flush all messages before closing
producer.flush()
print("[PRODUCER] All messages delivered, producer closed")