import os
from confluent_kafka import Consumer

# Configuration Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_USERNAME = os.getenv("KAFKA_USERNAME")
KAFKA_PASSWORD = os.getenv("KAFKA_PASSWORD")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "real-time-payments")

print(f"=== Test Consumer Kafka ===")
print(f"Bootstrap servers: {KAFKA_BOOTSTRAP_SERVERS}")
print(f"Username: {KAFKA_USERNAME}")
print(f"Password: {KAFKA_PASSWORD}")
print(f"Topic: {KAFKA_TOPIC}")
print()

consumer_config = {
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": KAFKA_USERNAME,
    "sasl.password": KAFKA_PASSWORD,
    "group.id": "test-group",
    "auto.offset.reset": "latest",
    "ssl.endpoint.identification.algorithm": "none",
    "enable.ssl.certificate.verification": False,
}

print("Création du consumer...")
try:
    consumer = Consumer(consumer_config)
    print("[OK] Consumer créé avec succès")
    
    print(f"Abonnement au topic '{KAFKA_TOPIC}'...")
    consumer.subscribe([KAFKA_TOPIC])
    print("[OK] Abonné au topic")
    
    print("En attente de messages (timeout 30s)...")
    msg = consumer.poll(timeout=30.0)
    
    if msg is None:
        print("[INFO] Aucun message reçu (normal si topic vide)")
    elif msg.error():
        print(f"[ERR] Erreur: {msg.error()}")
    else:
        print(f"[OK] Message reçu: {msg.value().decode('utf-8')}")
    
    consumer.close()
    print("[OK] Consumer fermé")
    
except Exception as e:
    print(f"[ERR] Erreur: {e}")
    import traceback
    traceback.print_exc()
