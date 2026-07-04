import os
import json
from confluent_kafka import Producer, KafkaException

# Configuration Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME") or "avnadmin"
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "real-time-payments")

print(f"=== Test Producer Kafka ===")
print(f"Bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")
print(f"Username: {KAFKA_USERNAME}")
print(f"Password: {'*' * len(KAFKA_PASSWORD) if KAFKA_PASSWORD else 'NOT SET'}")
print(f"Topic: {KAFKA_TOPIC}")
print()

producer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": KAFKA_USERNAME,
    "sasl.password": KAFKA_PASSWORD,
    "ssl.endpoint.identification.algorithm": "none",
    "enable.ssl.certificate.verification": False,
}

def delivery_report(err, msg):
    """Called once for each produced message to indicate delivery result."""
    if err is not None:
        print(f"[ERR] Error delivering message: {err}")
    else:
        print(f"[OK] Sent to topic '{msg.topic()}' [{msg.partition()}] at offset {msg.offset()}")

print("Création du producer...")
try:
    producer = Producer(producer_config)
    print("[OK] Producer créé avec succès")
    
    # Message de test
    test_message = {
        "test": True,
        "timestamp": "2026-07-04T12:00:00Z",
        "message": "Test message from producer"
    }
    
    print(f"Envoi d'un message de test vers '{KAFKA_TOPIC}'...")
    producer.produce(
        KAFKA_TOPIC,
        value=json.dumps(test_message).encode('utf-8'),
        key=b'test-key',
        callback=delivery_report
    )
    
    # Wait for delivery report
    producer.flush(timeout=10)
    print("[OK] Producer fermé")
    
except KafkaException as e:
    print(f"[ERR] Erreur Kafka: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"[ERR] Erreur: {e}")
    import traceback
    traceback.print_exc()
