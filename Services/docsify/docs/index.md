# Automatic Fraud Detection - Documentation

## 📋 Vue d'ensemble

Système de détection de fraude en temps réel utilisant l'IA pour analyser les transactions de paiement et alerter automatiquement en cas de suspicion.

### Objectifs

- Être averti dès qu'une fraude est détectée
- Vérifier quotidiennement tous les paiements et fraudes de la veille
- Pipeline de données temps réel avec monitoring et gouvernance

## 🏗️ Architecture Globale

```mermaid
graph TD
    subgraph "Source"
        API[Payment API]
    end
    
    subgraph "Streaming"
        KP[Kafka Producer]
        KT[Kafka Topic<br/>real-time-payments]
        KC[Fraud Consumer<br/>ML Prediction]
    end
    
    subgraph "ML & Storage"
        ML[MLflow<br/>Model Registry]
        PG[PostgreSQL<br/>Neon DB]
    end
    
    subgraph "Monitoring & Alerts"
        GF[Grafana<br/>Dashboard]
        EM[Email<br/>Resend]
    end
    
    API --> KP
    KP --> KT
    KT --> KC
    KC --> PG
    KC --> ML
    PG --> GF
    KC --> EM
    
    style API fill:#e1f5ff
    style KP fill:#fff4e1
    style KT fill:#ffe1e1
    style KC fill:#e1ffe1
    style ML fill:#f3e1ff
    style PG fill:#e1f5ff
    style GF fill:#fff4e1
    style EM fill:#ffe1e1
```

## 🔄 Flux de Données

```mermaid
graph TD
    subgraph "Événement Paiement"
        E1[Transaction Initiale]
        E2[Données Paiement]
    end
    
    subgraph "Ingestion"
        I1[Kafka Producer<br/>Python]
        I2[Sérialisation JSON]
        I3[Publication Topic]
    end
    
    subgraph "Traitement Temps Réel"
        T1[Kafka Consumer]
        T2[Chargement Modèle MLflow]
        T3[Prédiction Fraude]
        T4[Score de Confiance]
    end
    
    subgraph "Stockage"
        S1[PostgreSQL]
        S2[Table Predictions]
        S3[Table Transactions]
    end
    
    subgraph "Alertes"
        A1[Fraud Detected?]
        A2[Email Resend]
        A3[Grafana Alert]
    end
    
    E1 --> E2
    E2 --> I1
    I1 --> I2
    I2 --> I3
    I3 --> T1
    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> S1
    S1 --> S2
    S1 --> S3
    T4 --> A1
    A1 -->|Oui| A2
    A1 -->|Oui| A3
    
    style E1 fill:#e1f5ff
    style I1 fill:#fff4e1
    style T1 fill:#e1ffe1
    style S1 fill:#f3e1ff
    style A1 fill:#ffe1e1
```

## 🧠 Pipeline ML

```mermaid
graph TD
    subgraph "Données"
        D1[CSV Raw]
        D2[Data Loader]
        D3[Data Validator]
    end
    
    subgraph "Prétraitement"
        P1[Data Transformer<br/>Nettoyage]
        P2[Data Preparation<br/>Imputation/Scaling/Encoding]
        P3[Train/Test Split]
    end
    
    subgraph "Entraînement"
        M1[AutoGluon<br/>TabularPredictor]
        M2[Hyperparameter Tuning]
        M3[Model Training]
    end
    
    subgraph "Évaluation & Monitoring"
        E1[Model Evaluation]
        E2[Performance Metrics]
        E3[Evidently AI<br/>Drift Detection]
    end
    
    subgraph "MLOps"
        O1[MLflow Logging]
        O2[Model Registry]
        O3[Staging → Production]
    end
    
    D1 --> D2
    D2 --> D3
    D3 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> M1
    M1 --> M2
    M2 --> M3
    M3 --> E1
    E1 --> E2
    E2 --> E3
    E1 --> O1
    O1 --> O2
    O2 --> O3
    
    style D1 fill:#e1f5ff
    style P1 fill:#fff4e1
    style M1 fill:#e1ffe1
    style E1 fill:#f3e1ff
    style O1 fill:#ffe1e1
```

## 📊 Schéma de Données

### Schéma des Transactions

```mermaid
erDiagram
    TRANSACTION ||--o{ PREDICTION : génère
    TRANSACTION {
        string trans_num PK
        datetime trans_date_trans_time
        string cc_num
        string merchant
        category category
        float amount
        string gender
        string street
        string city
        string state
        int zip
        float lat
        float long
        int city_pop
        string job
        datetime dob
        string trans_num
        int unix_time
        float merch_lat
        float merch_long
        boolean is_fraud
    }
    
    PREDICTION {
        int id PK
        string trans_num FK
        boolean is_fraud_prediction
        float confidence_score
        string model_version
        timestamp prediction_time
        string model_alias
    }
    
    MONITORING {
        int id PK
        timestamp metric_time
        float accuracy
        float precision
        float recall
        float f1_score
        boolean drift_detected
        string drift_score
    }
```

### Features Utilisées

```mermaid
graph TD
    subgraph "Features Temporelles"
        F1[trans_date_trans_time]
        F2[month]
        F3[hour]
        F4[weekday]
        F5[is_weekend]
    end
    
    subgraph "Features Catégorielles"
        C1[category]
        C2[gender]
        C3[job]
    end
    
    subgraph "Features Numériques"
        N1[amount]
        N2[city_pop]
    end
    
    subgraph "Target"
        T1[is_fraud]
    end
    
    F1 --> F2
    F1 --> F3
    F1 --> F4
    F1 --> F5
    F2 --> T1
    F3 --> T1
    F4 --> T1
    F5 --> T1
    C1 --> T1
    C2 --> T1
    C3 --> T1
    N1 --> T1
    N2 --> T1
    
    style F1 fill:#e1f5ff
    style C1 fill:#fff4e1
    style N1 fill:#e1ffe1
    style T1 fill:#ffe1e1
```

## 🔧 Configuration

### Structure du Config YAML

```mermaid
graph TD
    subgraph "config.yaml"
        CFG[Configuration]
        
        subgraph "Data"
            D1[raw_path]
            D2[processed_path]
            D3[drop_columns]
            D4[target_column]
        end
        
        subgraph "Model"
            M1[test_size]
            M2[random_state]
            M3[model_type]
        end
        
        subgraph "Training"
            T1[epochs]
            T2[batch_size]
            T3[learning_rate]
        end
        
        subgraph "MLflow"
            L1[tracking_uri]
            L2[experiment_name]
            L3[model_name]
            L4[prod_alias]
        end
        
        subgraph "Monitoring"
            O1[reference_data_path]
            O2[dashboard_path]
            O3[report_path]
        end
    end
    
    CFG --> D1
    CFG --> M1
    CFG --> T1
    CFG --> L1
    CFG --> O1
    
    style CFG fill:#f3e1ff
```

## 🚀 Services de Déploiement

### Microservices Architecture

```mermaid
graph TD
    subgraph "HuggingFace Spaces"
        HF1[Producer Service]
        HF2[Consumer Service]
        HF3[MLflow UI]
        HF4[API Endpoint]
    end
    
    subgraph "Cloud Services"
        CS1[Redpanda Kafka]
        CS2[Neon PostgreSQL]
        CS3[Supabase S3<br/>MLflow Artifacts]
    end
    
    subgraph "Monitoring"
        MN1[Grafana Cloud]
        MN2[Resend Email]
    end
    
    HF1 --> CS1
    CS1 --> HF2
    HF2 --> CS2
    HF3 --> CS3
    HF2 --> MN1
    HF2 --> MN2
    HF4 --> HF1
    
    style HF1 fill:#e1f5ff
    style CS1 fill:#fff4e1
    style MN1 fill:#e1ffe1
```

## 📚 Navigation

- [Architecture Détaillée](architecture.md)
- [Schéma de Données](schema.md)
- [Pipeline ML](pipeline.md)
- [API Documentation](api.md)
- [Configuration](configuration.md)
- [Déploiement](deployment.md)
