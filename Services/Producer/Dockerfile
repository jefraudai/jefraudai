FROM python:3.10-slim

WORKDIR /app

# Dépendances système nécessaires (Kafka client / compilation / SSL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    librdkafka-dev \
    build-essential \
    libsasl2-dev \
    libsasl2-modules \
    openssl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code source
COPY . .

# HF Spaces attend souvent un port (même si non utilisé)
EXPOSE 7860

# Logs immédiats (important pour debugging HF)
ENV PYTHONUNBUFFERED=1

# Lancement du producer
CMD ["python", "-u", "producer.py"]