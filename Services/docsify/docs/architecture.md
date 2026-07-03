# Architecture Détaillée

## 🏛️ Vue d'ensemble de l'Architecture

Le système de détection de fraude est construit selon une architecture microservices orientée événements, utilisant Kafka pour le streaming temps réel et MLflow pour la gestion des modèles ML.

### Composants Principaux

```mermaid
graph TD
    subgraph "Couche Externe"
        UI[API Endpoint<br/>HuggingFace Space]
    end
    
    subgraph "Couche Streaming"
        KP[Kafka Producer<br/>Python]
        KT[Kafka Topic<br/>real-time-payments]
        KC[Kafka Consumer<br/>Python]
    end
    
    subgraph "Couche ML"
        ML[MLflow Server<br/>Model Registry]
        AG[AutoGluon Model<br/>TabularPredictor]
    end
    
    subgraph "Couche Données"
        PG[PostgreSQL<br/>Neon Cloud]
        S3[Supabase S3<br/>Artifacts Storage]
    end
    
    subgraph "Couche Monitoring"
        GF[Grafana Cloud<br/>Dashboard]
        EV[Evidently AI<br/>Validation & Performance]
        RS[Resend<br/>Email Service]
    end
    
    UI --> KP
    KP --> KT
    KT --> KC
    KC --> ML
    ML --> AG
    KC --> PG
    ML --> S3
    PG --> GF
    KC --> EV
    KC --> RS
    
    style UI fill:#e1f5ff
    style KP fill:#fff4e1
    style KC fill:#e1ffe1
    style ML fill:#f3e1ff
    style PG fill:#e1f5ff
    style GF fill:#fff4e1
```

## 🔄 Pipeline de Traitement Temps Réel

### Flux de Traitement

```mermaid
sequenceDiagram
    participant API as Payment API
    participant KP as Kafka Producer
    participant KT as Kafka Topic
    participant KC as Kafka Consumer
    participant ML as MLflow Model
    participant PG as PostgreSQL
    participant RS as Resend Email
    
    API->>KP: Transaction Data
    KP->>KP: Sérialisation JSON
    KP->>KT: Publish Message
    KT->>KC: Consume Message
    KC->>ML: Load Model (alias: prod)
    ML-->>KC: Model Loaded
    KC->>KC: Preprocess Features
    KC->>ML: Predict Fraud
    ML-->>KC: Prediction + Confidence
    KC->>PG: Store Prediction
    KC->>KC: Check Fraud Threshold
    alt Fraud Detected
        KC->>RS: Send Alert Email
        RS-->>KC: Email Sent
    end
```

### Producer Service

```mermaid
graph TD
    subgraph "Producer Service"
        P1[Payment API Listener]
        P2[Data Validation]
        P3[JSON Serialization]
        P4[Kafka Producer Client]
        P5[Error Handler]
    end
    
    subgraph "Kafka Cluster"
        K1[Topic: real-time-payments]
        K2[Partitions: 3]
        K3[Replication Factor: 2]
    end
    
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> K1
    P4 --> P5
    P5 -->|Retry| P4
    
    style P1 fill:#e1f5ff
    style P4 fill:#fff4e1
    style K1 fill:#ffe1e1
```

**Fonctionnalités du Producer:**
- Écoute les événements de paiement depuis l'API
- Valide la structure des données
- Sérialise en JSON
- Publie sur le topic Kafka `real-time-payments`
- Gestion des erreurs avec retry automatique

### Consumer Service

```mermaid
graph TD
    subgraph "Consumer Service"
        C1[Kafka Consumer Client]
        C2[Message Deserializer]
        C3[Feature Preprocessing]
        C4[MLflow Model Loader]
        C5[Prediction Engine]
        C6[Database Handler]
        C7[Alert Manager]
    end
    
    subgraph "MLflow"
        M1[Model Registry]
        M2[Production Alias<br/>prod]
        M3[Model Artifacts]
    end
    
    subgraph "PostgreSQL"
        D1[Predictions Table]
    end
    
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C4 --> M1
    M1 --> M2
    M2 --> M3
    M3 --> C4
    C4 --> C5
    C5 --> C6
    C6 --> D1
    C5 --> C7
    C7 -->|Fraud Alert| Email
    
    style C1 fill:#e1f5ff
    style C5 fill:#e1ffe1
    style M1 fill:#f3e1ff
    style D1 fill:#fff4e1
```

**Fonctionnalités du Consumer:**
- Consomme les messages du topic Kafka
- Charge le modèle depuis MLflow via l'alias `prod`
- Prétraite les features (imputation, scaling, encoding)
- Génère les prédictions avec score de confiance
- Stocke les résultats en PostgreSQL
- Déclenche les alertes email en cas de fraude

## 🧠 Pipeline ML d'Entraînement

### Étapes du Pipeline

```mermaid
graph TD
    subgraph "Phase 1: Ingestion"
        I1[Load CSV Data]
        I2[Data Validation<br/>Evidently AI]
        I3[Quality Report]
    end
    
    subgraph "Phase 2: Prétraitement"
        P1[Data Cleaning<br/>Drop Columns]
        P2[Date Transformation<br/>Month/Hour/Weekday]
        P3[Feature Engineering]
        P4[Train/Test Split<br/>80/20]
    end
    
    subgraph "Phase 3: Préparation - Autogluon"
        R1[Auto-detect Types<br/>Numeric/Categorical]
        R2[Numeric Pipeline<br/>Imputer + Scaler]
        R3[Categorical Pipeline<br/>OneHotEncoder]
        R4[ColumnTransformer]
    end
    
    subgraph "Phase 4: Entraînement"
        T1[AutoGluon TabularPredictor]
        T2[Hyperparameter Tuning]
        T3[Model Fitting]
        T4[Feature Importance]
    end
    
    subgraph "Phase 5: Évaluation"
        E1[Model Evaluation]
        E2[Metrics Calculation<br/>Accuracy/Precision/Recall/F1]
        E3[Performance Monitoring<br/>Evidently AI]
    end
    
    subgraph "Phase 6: MLOps"
        M1[MLflow Logging]
        M2[Model Registration]
        M3[Staging Alias]
        M4[Production Promotion<br/>Alias: prod]
    end
    
    I1 --> I2
    I2 --> I3
    I3 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> R1
    R1 --> R2
    R1 --> R3
    R2 --> R4
    R3 --> R4
    R4 --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> E1
    E1 --> E2
    E2 --> E3
    E1 --> M1
    M1 --> M2
    M2 --> M3
    M3 --> M4
    
    style I1 fill:#e1f5ff
    style P1 fill:#fff4e1
    style R1 fill:#e1ffe1
    style T1 fill:#f3e1ff
    style E1 fill:#ffe1e1
    style M1 fill:#e1f5ff
```

### Détail du Prétraitement

```mermaid
graph TD
    subgraph "Input"
        IN[Raw DataFrame]
    end
    
    subgraph "Stateless Transform"
        S1[Strip Column Names]
        S2[Drop Unnamed Columns]
        S3[Drop Configured Columns]
        S4[Transform Dates<br/>to Month/Hour/Weekday]
    end
    
    subgraph "Stateful Transform - Autogluon"
        F1[Detect Feature Types]
        F2[Numeric Features<br/>Imputer + Scaler]
        F3[Categorical Features<br/>OneHotEncoder]
        F4[ColumnTransformer Fit]
        F5[ColumnTransformer Transform]
    end
    
    subgraph "Output"
        OUT[Transformed Array]
    end
    
    IN --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> F1
    F1 --> F2
    F1 --> F3
    F2 --> F4
    F3 --> F4
    F4 --> F5
    F5 --> OUT
    
    style IN fill:#e1f5ff
    style S1 fill:#fff4e1
    style F1 fill:#e1ffe1
    style OUT fill:#ffe1e1
```


## 🔐 Sécurité et Gouvernance

### Gestion des Secrets

```mermaid
graph TD
    subgraph "Secrets Management"
        G1[GitHub Secrets]
        G2[Environment Variables]
        G3[Config YAML Override]
    end
    
    subgraph "Credentials"
        C1[Database URI]
        C2[MLflow Tracking URI]
        C3[Kafka Credentials]
        C4[Resend API Key]
    end
    
    subgraph "Access Control"
        A1[Model Aliases<br/>Staging/Production]
        A2[Database Roles]
        A3[Kafka ACLs]
    end
    
    G1 --> G2
    G2 --> G3
    G2 --> C1
    G2 --> C2
    G2 --> C3
    G2 --> C4
    C1 --> A2
    C2 --> A1
    C3 --> A3
    
    style G1 fill:#e1f5ff
    style C1 fill:#fff4e1
    style A1 fill:#e1ffe1
```

## 🚀 Infrastructure Cloud

### Déploiement sur HuggingFace Spaces

```mermaid
graph TD
    subgraph "HuggingFace Spaces"
        HF1[Producer Service<br/>Python + Docker]
        HF2[Consumer Service<br/>Python + Docker]
        HF3[MLflow UI<br/>Python + Docker]
    end
    
    subgraph "External Cloud"
        EC1[Redpanda Cloud<br/>Kafka]
        EC2[Neon Cloud<br/>PostgreSQL]
        EC3[Supabase<br/>S3 Storage]
    end
    
    subgraph "Monitoring Cloud"
        MC1[Grafana Cloud]
        MC2[Resend<br/>Email Service]
    end
    
    HF1 --> EC1
    HF2 --> EC1
    HF2 --> EC2
    HF3 --> EC3
    MC1 --> EC2
    HF2 --> MC2
    
    style HF1 fill:#e1f5ff
    style EC1 fill:#fff4e1
    style MC1 fill:#e1ffe1
```

### Services et Endpoints

| Service        | URL                                                                                                                                                         | Description        |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| API Production | https://sdacelo-real-time-fraud-detection.hf.space/                                                                                                         | Endpoint principal |
| MLflow UI      | https://jefraudai-mlflow.hf.space/#/models                                                                                                                  | Interface MLflow   |
| Producer       | https://huggingface.co/spaces/jefraudai/Producer                                                                                                            | Service Producer   |
| Consumer       | https://huggingface.co/spaces/jefraudai/consumer                                                                                                            | Service Consumer   |
| Kafka          | https://cloud.redpanda.com/clusters/d8c0ur6uk85ifvcgnlrg/topics/real-time-payments/                                                                         | Cluster Redpanda   |
| Dashboard      | https://jefraudai.grafana.net/public-dashboards/44a8ad6003bc4887880bfcfb8ebb6598?from=2023-12-04T13:55:58.556Z&to=2028-12-03T13:55:58.556Z&timezone=browser | Grafana Dashboard  |
