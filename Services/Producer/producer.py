import socket
import os
#from dotenv import find_dotenv, load_dotenv
from kafka import KafkaProducer
from kafka.errors import KafkaError

#Test de connexion au cluster Kafka Redpanda en local
#load_dotenv(find_dotenv(".env"), override=True)      # config
#load_dotenv(find_dotenv(".env.secrets"), override=True)   # secrets only useful on local environment

producer = KafkaProducer(
  bootstrap_servers="d89g6r8hvfrjvm53ss50.any.eu-central-1.mpx.prd.cloud.redpanda.com:9092",
  security_protocol="SASL_SSL",
  sasl_mechanism="<SCRAM-SHA-256 or SCRAM-SHA-512>",
  sasl_plain_username="jefraudai",
  sasl_plain_password=os.environ["KAFKA_PASSWORD"],
)
hostname = str.encode(socket.gethostname())

def on_success(metadata):
  print(f"Sent to topic '{metadata.topic}' at offset {metadata.offset}")

def on_error(e):
  print(f"Error sending message: {e}")

# Produce 100 messages asynchronously
for i in range(2):
  msg = f"asynchronous message #{i}"
  future = producer.send(
    "demo-topic",
    key=hostname,
    value=str.encode(msg)
  )
  future.add_callback(on_success)
  future.add_errback(on_error)
producer.flush()
producer.close()