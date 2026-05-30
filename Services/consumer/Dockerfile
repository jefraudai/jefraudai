FROM python:3.11-slim

# Secrets à définir
#ENV DB_URI="postgresql://user:password@host:port/dbname"
#ENV RESEND_API_KEY="re_xxxxxxxxx"

# Variables d'environnement pour l'application
ENV KAFKA_BOOTSTRAP_SERVERS="d8c0ur6uk85ifvcgnlrg.any.eu-west-2.mpx.prd.cloud.redpanda.com:9092"
ENV RESEND_BASE_URL="https://api.resend.com/emails"
ENV SMTP_USER="jefraudai@sustcoop.fr"
ENV ALERT_TO="jefraudai@free.fr"
ENV KAFKA_TOPIC_IN="real-time-payments"

# Variables techniquesd'environnement
ENV PYTHONDONTWRITEBYTECODE=1
# Logs immédiats (important pour debugging HF)
ENV PYTHONUNBUFFERED=1

# Dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

# Dossier de travail
COPY . /app
WORKDIR /app

# Installer les dépendances Python
COPY requirements.txt requirements-internal.txt pyproject.toml .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-internal.txt

# HF Spaces attend souvent un port (même si non utilisé)
EXPOSE 7860

CMD ["python", "-u", "consumer.py"]
