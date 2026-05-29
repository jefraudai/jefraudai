FROM python:3.10-slim

# VAriables à définir dans les variables d'environnement de votre conteneur ou de votre service d'orchestration
#ENV DB_URI="postgresql://user:password@host:port/dbname"
#ENV RESEND_API_KEY="re_xxxxxxxxx"

ENV RESEND_BASE_URL="https://api.resend.com/emails"
ENV SMTP_USER="jefraudai@sustcoop.fr"
ENV ALERT_TO="jefraudai@free.fr"
ENV PYTHONPATH=/app/src

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    librdkafka-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-internal.txt pyproject.toml .
COPY src ./src

# numpy<2 doit être installé avant xgboost et mlflow pour éviter les conflits
RUN pip install --no-cache-dir "numpy<2" && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-internal.txt

COPY . .

CMD ["python", "consumer.py"]
