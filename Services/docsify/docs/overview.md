# Automatic-Fraud-Detection - Documentation

## 📋 Besoins

Système de détection de fraude en temps réel utilisant l'IA pour analyser les transactions de paiement et alerter automatiquement en cas de suspicion.

- Être averti en temps réel qu'une fraude est détectée
- Une fois chaque matin, pouvoir vérifier tous les paiements et fraudes intervenus la veille.

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
    
    style Source fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style Streaming fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style "ML & Storage" fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style "Monitoring & Alerts" fill:#1e293b,stroke:#4a90d9,color:#ffffff
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
    E1 --> O1
    O1 --> O2
    O2 --> O3
    
    style D1 fill:#e1f5ff
    style P1 fill:#fff4e1
    style M1 fill:#e1ffe1
    style E1 fill:#f3e1ff
    style O1 fill:#ffe1e1
    
    style Données fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style Prétraitement fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style Entraînement fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style "Évaluation & Monitoring" fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style MLOps fill:#1e293b,stroke:#4a90d9,color:#ffffff
```

## 📊 Schéma de Données

### Features Utilisées

Pour faciliter l'entrainement avec des ressources limités, certaines données ont volontairement été omises. La prédiction peut être amélioré en ajoutant ses données aux features.
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
    
    style "Features Temporelles" fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style "Features Catégorielles" fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style "Features Numériques" fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style Target fill:#1e293b,stroke:#4a90d9,color:#ffffff
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
    
    style "HuggingFace Spaces" fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style "Cloud Services" fill:#1e293b,stroke:#4a90d9,color:#ffffff
    style Monitoring fill:#1e293b,stroke:#4a90d9,color:#ffffff
```

## 📚 Navigation

- [Architecture Détaillée](architecture.md)
- [Schéma de Données](data.md)
- [Pipeline ML](pipeline.md)
- [Configuration](configuration.md)
- [Déploiement](deployment.md)
