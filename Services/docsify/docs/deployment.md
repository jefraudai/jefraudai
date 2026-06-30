# Déploiement

## 🚀 Vue d'ensemble du Déploiement

Le projet est déployé sur HuggingFace Spaces avec des services cloud externes pour Kafka, PostgreSQL et le stockage.

## 🏗️ Architecture de Déploiement

### Infrastructure Cloud

```mermaid
graph TD
    subgraph "HuggingFace Spaces"
        HF1[Producer Service<br/>Docker]
        HF2[Consumer Service<br/>Docker]
        HF3[MLflow UI<br/>Docker]
        HF4[API Endpoint<br/>FastAPI]
    end
    
    subgraph "Redpanda Cloud"
        RP1[Kafka Cluster]
        RP2[Topic: real-time-payments]
        RP3[Partitions: 3]
    end
    
    subgraph "Neon Cloud"
        NE1[PostgreSQL Database]
        NE2[Pooled Connections]
        NE3[Auto-scaling]
    end
    
    subgraph "Supabase"
        SB1[S3 Storage]
        SB2[MLflow Artifacts]
        SB3[Bucket: mlflow-artifacts]
    end
    
    subgraph "Grafana Cloud"
        GF1[Dashboard]
        GF2[Metrics Collection]
        GF3[Alerting]
    end
    
    subgraph "Resend"
        RS1[Email Service]
        RS2[API Integration]
        RS3[Alert Delivery]
    end
    
    HF1 --> RP1
    HF2 --> RP1
    HF2 --> NE1
    HF3 --> SB1
    HF2 --> GF1
    HF2 --> RS1
    
    style HF1 fill:#e1f5ff
    style RP1 fill:#fff4e1
    style NE1 fill:#e1ffe1
    style GF1 fill:#ffe1e1
```

## 🐳 Docker Configuration

### Producer Dockerfile

```mermaid
graph TD
    subgraph "Producer Dockerfile"
        D1[FROM python:3.11-slim]
        D2[WORKDIR /app]
        D3[COPY requirements.txt]
        D4[RUN pip install]
        D5[COPY producer.py]
        D6[COPY src/]
        D7[CMD python producer.py]
    end
    
    subgraph "Dependencies"
        DP1[kafka-python]
        DP2[python-dotenv]
        DP3[pandas]
    end
    
    D4 --> DP1
    D4 --> DP2
    D4 --> DP3
    
    style D1 fill:#e1f5ff
    style DP1 fill:#fff4e1
```

### Consumer Dockerfile

```mermaid
graph TD
    subgraph "Consumer Dockerfile"
        D1[FROM python:3.11-slim]
        D2[WORKDIR /app]
        D3[COPY requirements.txt]
        D4[RUN pip install]
        D5[COPY consumer.py]
        D6[COPY src/]
        D7[CMD python consumer.py]
    end
    
    subgraph "Dependencies"
        DP1[kafka-python]
        DP2[mlflow]
        DP3[psycopg2-binary]
        DP4[autogluon.tabular]
        DP5[pandas]
        DP6[python-dotenv]
    end
    
    D4 --> DP1
    D4 --> DP2
    D4 --> DP3
    D4 --> DP4
    D4 --> DP5
    D4 --> DP6
    
    style D1 fill:#e1f5ff
    style DP1 fill:#fff4e1
```

### Docsify Dockerfile

```mermaid
graph TD
    subgraph "Docsify Dockerfile"
        D1[FROM node:alpine]
        D2[WORKDIR /docs]
        D3[COPY index.html]
        D4[COPY docs/]
        D5[EXPOSE 3000]
        D6[CMD npx docsify serve]
    end
    
    subgraph "Static Files"
        SF1[index.html]
        SF2[docs/*.md]
        SF3[Mermaid Plugin]
    end
    
    D3 --> SF1
    D4 --> SF2
    D4 --> SF3
    
    style D1 fill:#e1f5ff
    style SF1 fill:#fff4e1
```

## 📦 Services HuggingFace Spaces

### Producer Service

```mermaid
graph TD
    subgraph "Producer Service"
        PS1[app.py / producer.py]
        PS2[requirements.txt]
        PS3[Dockerfile]
        PS4[README.md]
    end
    
    subgraph "Environment"
        E1[KAFKA_BOOTSTRAP_SERVERS]
        E2[KAFKA_API_KEY]
        E3[KAFKA_API_SECRET]
        E4[KAFKA_TOPIC]
    end
    
    subgraph "Functionality"
        F1[Receive HTTP Requests]
        F2[Validate Transaction Data]
        F3[Serialize to JSON]
        F4[Publish to Kafka]
        F5[Handle Errors]
    end
    
    PS1 --> E1
    E1 --> F1
    F1 --> F2
    F2 --> F3
    F3 --> F4
    F4 --> F5
    
    style PS1 fill:#e1f5ff
    style E1 fill:#fff4e1
    style F1 fill:#e1ffe1
```

**URL:** https://huggingface.co/spaces/jefraudai/Producer

### Consumer Service

```mermaid
graph TD
    subgraph "Consumer Service"
        CS1[consumer.py]
        CS2[requirements.txt]
        CS3[Dockerfile]
        CS4[README.md]
    end
    
    subgraph "Environment"
        E1[KAFKA_BOOTSTRAP_SERVERS]
        E2[KAFKA_API_KEY]
        E3[KAFKA_API_SECRET]
        E4[KAFKA_TOPIC]
        E5[DATABASE_URI]
        E6[MLFLOW_TRACKING_URI]
    end
    
    subgraph "Functionality"
        F1[Consume from Kafka]
        F2[Load MLflow Model]
        F3[Preprocess Features]
        F4[Predict Fraud]
        F5[Store in PostgreSQL]
        F6[Send Alerts]
    end
    
    CS1 --> E1
    E1 --> F1
    F1 --> F2
    F2 --> F3
    F3 --> F4
    F4 --> F5
    F5 --> F6
    
    style CS1 fill:#e1f5ff
    style E1 fill:#fff4e1
    style F1 fill:#e1ffe1
```

**URL:** https://huggingface.co/spaces/jefraudai/consumer

### MLflow UI

```mermaid
graph TD
    subgraph "MLflow Service"
        MS1[MLflow Server]
        MS2[Model Registry]
        MS3[Artifact Storage]
    end
    
    subgraph "Environment"
        E1[MLFLOW_TRACKING_URI]
        E2[MLFLOW_S3_ENDPOINT_URL]
        E3[AWS_ACCESS_KEY_ID]
        E4[AWS_SECRET_ACCESS_KEY]
    end
    
    subgraph "Features"
        F1[Experiment Tracking]
        F2[Model Versioning]
        F3[Model Aliases]
        F4[Artifact Storage]
    end
    
    MS1 --> E1
    E1 --> F1
    F1 --> F2
    F2 --> F3
    F3 --> F4
    
    style MS1 fill:#e1f5ff
    style E1 fill:#fff4e1
    style F1 fill:#e1ffe1
```

**URL:** https://jefraudai-mlflow.hf.space/#/models

## ☁️ Services Cloud Externes

### Redpanda Cloud (Kafka)

```mermaid
graph TD
    subgraph "Redpanda Configuration"
        RC1[Cluster: d8c0ur6uk85ifvcgnlrg]
        RC2[Topic: real-time-payments]
        RC3[Partitions: 3]
        RC4[Replication Factor: 2]
        RC5[Retention: 7 days]
    end
    
    subgraph "Connection"
        CN1[Bootstrap Servers]
        CN2[API Key]
        CN3[API Secret]
        CN4[SASL/SSL]
    end
    
    RC1 --> CN1
    RC2 --> CN1
    CN1 --> CN2
    CN2 --> CN3
    CN3 --> CN4
    
    style RC1 fill:#e1f5ff
    style CN1 fill:#fff4e1
```

**URL:** https://cloud.redpanda.com/clusters/d8c0ur6uk85ifvcgnlrg/topics/real-time-payments/

### Neon Cloud (PostgreSQL)

```mermaid
graph TD
    subgraph "Neon Configuration"
        NC1[Project: restless-shadow-27935644]
        NC2[Database: fraud_detection]
        NC3[Pooling: Enabled]
        NC4[Auto-scaling: Enabled]
    end
    
    subgraph "Connection"
        CN1[Connection String]
        CN2[SSL Mode: require]
        CN3[Connection Pool]
    end
    
    subgraph "Features"
        F1[Serverless]
        F2[Branching]
        F3[Time Travel]
        F4[Auto-scaling]
    end
    
    NC1 --> CN1
    CN1 --> F1
    F1 --> F2
    F2 --> F3
    F3 --> F4
    
    style NC1 fill:#e1f5ff
    style CN1 fill:#fff4e1
    style F1 fill:#e1ffe1
```

**URL:** https://console.neon.tech/app/projects/restless-shadow-27935644

### Supabase (S3 Storage)

```mermaid
graph TD
    subgraph "Supabase Configuration"
        SC1[Project: xjkkzjtjgdsmemheppgl]
        SC2[Bucket: mlflow-artifacts]
        SC3[Region: auto]
        SC4[Public: false]
    end
    
    subgraph "Connection"
        CN1[S3 Endpoint]
        CN2[Access Key]
        CN3[Secret Key]
    end
    
    subgraph "Usage"
        US1[MLflow Artifacts]
        US2[Model Files]
        US3[Preprocessors]
    end
    
    SC1 --> CN1
    CN1 --> US1
    US1 --> US2
    US2 --> US3
    
    style SC1 fill:#e1f5ff
    style CN1 fill:#fff4e1
    style US1 fill:#e1ffe1
```

**URL:** https://supabase.com/dashboard/project/xjkkzjtjgdsmemheppgl/storage/files/buckets/mlflow-artifacts

### Grafana Cloud

```mermaid
graph TD
    subgraph "Grafana Configuration"
        GC1[Stack: jefraudai]
        GC2[Dashboard: Fraud Detection]
        GC3[Refresh: 1m]
    end
    
    subgraph "Data Sources"
        DS1[PostgreSQL]
        DS2[Prometheus]
        DS3[MLflow]
    end
    
    subgraph "Panels"
        PN1[Fraud Rate]
        PN2[Prediction Latency]
        PN3[Kafka Lag]
        PN4[Model Performance]
    end
    
    GC1 --> DS1
    DS1 --> PN1
    DS2 --> PN2
    DS3 --> PN3
    DS1 --> PN4
    
    style GC1 fill:#e1f5ff
    style DS1 fill:#fff4e1
    style PN1 fill:#e1ffe1
```

**URL:** https://jefraudai.grafana.net/public-dashboards/2b818560e4654e5ba8d5ae9a8a3dc72e

### Resend (Email Service)

```mermaid
graph TD
    subgraph "Resend Configuration"
        RC1[Account: Jenedai]
        RC2[API Key]
        RC3[From Email]
        RC4[Rate Limit]
    end
    
    subgraph "Email Types"
        ET1[Fraud Alert]
        ET2[System Alert]
        ET3[Daily Report]
    end
    
    subgraph "Recipients"
        RE1[Security Team]
        RE2[Operations Team]
        RE3[Management]
    end
    
    RC1 --> ET1
    ET1 --> RE1
    ET2 --> RE2
    ET3 --> RE3
    
    style RC1 fill:#e1f5ff
    style ET1 fill:#fff4e1
    style RE1 fill:#e1ffe1
```

**URL:** https://resend.com/

## 🔧 Configuration du Déploiement

### Variables d'Environnement

```mermaid
graph TD
    subgraph "Producer Env Vars"
        PE1[KAFKA_BOOTSTRAP_SERVERS]
        PE2[KAFKA_API_KEY]
        PE3[KAFKA_API_SECRET]
        PE4[KAFKA_TOPIC]
    end
    
    subgraph "Consumer Env Vars"
        CE1[KAFKA_BOOTSTRAP_SERVERS]
        CE2[KAFKA_API_KEY]
        CE3[KAFKA_API_SECRET]
        CE4[KAFKA_TOPIC]
        CE5[DATABASE_URI]
        CE6[MLFLOW_TRACKING_URI]
        CE7[MLFLOW_EXPERIMENT_NAME]
        CE8[MLFLOW_MODEL_NAME]
        CE9[RESEND_API_KEY]
        CE10[ALERT_EMAIL]
    end
    
    subgraph "MLflow Env Vars"
        ME1[MLFLOW_TRACKING_URI]
        ME2[MLFLOW_S3_ENDPOINT_URL]
        ME3[AWS_ACCESS_KEY_ID]
        ME4[AWS_SECRET_ACCESS_KEY]
    end
    
    style PE1 fill:#e1f5ff
    style CE1 fill:#fff4e1
    style ME1 fill:#e1ffe1
```

### GitHub Secrets

```mermaid
graph TD
    subgraph "GitHub Secrets"
        GS1[KAFKA_BOOTSTRAP_SERVERS]
        GS2[KAFKA_API_KEY]
        GS3[KAFKA_API_SECRET]
        GS4[DATABASE_URI]
        GS5[MLFLOW_TRACKING_URI]
        GS6[RESEND_API_KEY]
        GS7[ALERT_EMAIL]
    end
    
    subgraph "Usage"
        US1[CI/CD Pipelines]
        US2[HuggingFace Spaces]
        US3[Docker Builds]
    end
    
    GS1 --> US1
    GS2 --> US1
    GS3 --> US2
    GS4 --> US2
    GS5 --> US3
    
    style GS1 fill:#e1f5ff
    style US1 fill:#fff4e1
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```mermaid
graph TD
    subgraph "CI/CD Pipeline"
        CD1[Push to GitHub]
        CD2[Trigger Workflow]
        CD3[Run Tests]
        CD4[Build Docker Image]
        CD5[Push to HuggingFace]
        CD6[Deploy to Spaces]
        CD7[Health Check]
    end
    
    subgraph "Testing"
        T1[Unit Tests]
        T2[Integration Tests]
        T3[Model Tests]
    end
    
    subgraph "Deployment"
        D1[Producer Space]
        D2[Consumer Space]
        D3[MLflow Space]
    end
    
    CD1 --> CD2
    CD2 --> CD3
    CD3 --> T1
    T1 --> T2
    T2 --> T3
    T3 --> CD4
    CD4 --> CD5
    CD5 --> CD6
    CD6 --> D1
    CD6 --> D2
    CD6 --> D3
    D1 --> CD7
    D2 --> CD7
    D3 --> CD7
    
    style CD1 fill:#e1f5ff
    style T1 fill:#fff4e1
    style D1 fill:#e1ffe1
```

## 📊 Monitoring en Production

### Stack de Monitoring

```mermaid
graph TD
    subgraph "Monitoring Sources"
        MS1[PostgreSQL Metrics]
        MS2[Kafka Metrics]
        MS3[MLflow Metrics]
        MS4[Application Logs]
    end
    
    subgraph "Collection"
        CL1[Grafana Agent]
        CL2[Prometheus]
        CL3[Loki Logs]
    end
    
    subgraph "Visualization"
        VI1[Grafana Dashboards]
        VI2[Alerts]
        VI3[Reports]
    end
    
    MS1 --> CL1
    MS2 --> CL1
    MS3 --> CL2
    MS4 --> CL3
    CL1 --> VI1
    CL2 --> VI1
    CL3 --> VI1
    VI1 --> VI2
    VI2 --> VI3
    
    style MS1 fill:#e1f5ff
    style CL1 fill:#fff4e1
    style VI1 fill:#e1ffe1
```

### Métriques Clés

```mermaid
graph TD
    subgraph "Business Metrics"
        BM1[Fraud Detection Rate]
        BM2[False Positive Rate]
        BM3[Alert Response Time]
    end
    
    subgraph "Technical Metrics"
        TM1[Prediction Latency]
        TM2[Kafka Consumer Lag]
        TM3[Database Query Time]
        TM4[API Response Time]
    end
    
    subgraph "ML Metrics"
        MM1[Model Accuracy]
        MM2[Model Drift]
        MM3[Data Drift]
    end
    
    style BM1 fill:#e1f5ff
    style TM1 fill:#fff4e1
    style MM1 fill:#e1ffe1
```

## 🔐 Sécurité

### Mesures de Sécurité

```mermaid
graph TD
    subgraph "Security Layers"
        SL1[API Authentication]
        SL2[Database Encryption]
        SL3[Kafka SASL/SSL]
        SL4[Secrets Management]
    end
    
    subgraph "Access Control"
        AC1[GitHub Secrets]
        AC2[HuggingFace Secrets]
        AC3[IP Whitelist]
        AC4[Rate Limiting]
    end
    
    subgraph "Data Protection"
        DP1[PII Redaction]
        DP2[Encryption at Rest]
        DP3[Encryption in Transit]
        DP4[Audit Logging]
    end
    
    SL1 --> AC1
    SL2 --> AC2
    SL3 --> AC3
    SL4 --> AC4
    AC1 --> DP1
    AC2 --> DP2
    AC3 --> DP3
    AC4 --> DP4
    
    style SL1 fill:#e1f5ff
    style AC1 fill:#fff4e1
    style DP1 fill:#e1ffe1
```

## 🚨 Gestion des Incidents

### Procédure d'Alerte

```mermaid
graph TD
    subgraph "Alert Detection"
        AD1[Threshold Breached]
        AD2[Anomaly Detected]
        AD3[Service Down]
    end
    
    subgraph "Response"
        RP1[Auto-Alert Email]
        RP2[Slack Notification]
        RP3[PagerDuty]
    end
    
    subgraph "Investigation"
        IN1[Check Logs]
        IN2[Check Metrics]
        IN3[Check Status Page]
    end
    
    subgraph "Resolution"
        RS1[Restart Service]
        RS2[Rollback Model]
        RS3[Scale Resources]
    end
    
    AD1 --> RP1
    AD2 --> RP2
    AD3 --> RP3
    RP1 --> IN1
    RP2 --> IN2
    RP3 --> IN3
    IN1 --> RS1
    IN2 --> RS2
    IN3 --> RS3
    
    style AD1 fill:#ffe1e1
    style RP1 fill:#fff4e1
    style IN1 fill:#e1ffe1
    style RS1 fill:#e1f5ff
```

## 📈 Scaling

### Stratégie de Scaling

```mermaid
graph TD
    subgraph "Auto-scaling"
        AS1[CPU Threshold > 70%]
        AS2[Memory Threshold > 80%]
        AS3[Request Latency > 500ms]
    end
    
    subgraph "Scaling Actions"
        SA1[Add Kafka Partitions]
        SA2[Scale Consumer Instances]
        SA3[Scale Database Pool]
        SA4[Enable Caching]
    end
    
    subgraph "Load Balancing"
        LB1[Kafka Partitions]
        LB2[Consumer Groups]
        LB3[Database Pooling]
    end
    
    AS1 --> SA1
    AS2 --> SA2
    AS3 --> SA3
    SA1 --> LB1
    SA2 --> LB2
    SA3 --> LB3
    
    style AS1 fill:#e1f5ff
    style SA1 fill:#fff4e1
    style LB1 fill:#e1ffe1
```

## 🔄 Mises à jour

### Procédure de Déploiement

```mermaid
graph TD
    subgraph "Deployment Steps"
        DS1[Train New Model]
        DS2[Register in MLflow]
        DS3[Set Staging Alias]
        DS4[Run Validation]
        DS5[Promote to Prod]
        DS6[Monitor Metrics]
    end
    
    subgraph "Rollback Plan"
        RB1[Previous Model Version]
        RB2[Revert Alias]
        RB3[Verify Metrics]
    end
    
    DS1 --> DS2
    DS2 --> DS3
    DS3 --> DS4
    DS4 --> DS5
    DS5 --> DS6
    DS6 -->|Failure| RB1
    RB1 --> RB2
    RB2 --> RB3
    
    style DS1 fill:#e1f5ff
    style RB1 fill:#ffe1e1
```

## 📝 Résumé des Endpoints Production

| Service | URL | Description |
|---------|-----|-------------|
| API | https://sdacelo-real-time-fraud-detection.hf.space/ | Endpoint principal |
| MLflow | https://jefraudai-mlflow.hf.space/#/models | Interface MLflow |
| Producer | https://huggingface.co/spaces/jefraudai/Producer | Service Producer |
| Consumer | https://huggingface.co/spaces/jefraudai/consumer | Service Consumer |
| Kafka | https://cloud.redpanda.com/... | Cluster Redpanda |
| Dashboard | https://jefraudai.grafana.net/... | Grafana Dashboard |
