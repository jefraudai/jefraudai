# Schéma de Données

## 📊 Vue d'ensemble du Schéma

Le système utilise PostgreSQL comme base de données principale pour stocker les transactions et les prédictions de fraude.

## 🗄️ Schéma de Base de Données

### Diagramme Entité-Association

```mermaid
erDiagram
    TRANSACTION ||--o{ PREDICTION : génère
    TRANSACTION ||--o{ MONITORING_METRIC : est_monitorée
    MODEL_VERSION ||--o{ PREDICTION : utilise
    MODEL_VERSION {
        int version_id PK
        string model_name
        int version_number
        string alias
        timestamp created_at
        string mlflow_run_id
        float accuracy
        float precision
        float recall
        float f1_score
    }
    
    TRANSACTION {
        bigint trans_num PK
        datetime trans_date_trans_time
        string cc_num
        string merchant
        string category
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
        int unix_time
        float merch_lat
        float merch_long
        boolean is_fraud
        timestamp created_at
    }
    
    PREDICTION {
        bigint id PK
        bigint trans_num FK
        boolean is_fraud_prediction
        float confidence_score
        int model_version_id FK
        timestamp prediction_time
        string processing_time_ms
        string status
    }
    
    MONITORING_METRIC {
        int id PK
        timestamp metric_time
        float accuracy
        float precision
        float recall
        float f1_score
        boolean drift_detected
        float drift_score
        int total_predictions
        int fraud_predictions
        int total_transactions
    }
    
    ALERT_LOG {
        int id PK
        bigint trans_num FK
        timestamp alert_time
        string alert_type
        string recipient_email
        boolean sent_successfully
        string error_message
    }
    
    TRANSACTION ||--o{ ALERT_LOG : déclenche
```

## 📋 Structure des Tables

### Table: TRANSACTION

```mermaid
graph TD
    subgraph "TRANSACTION Table"
        T1[trans_num<br/>BIGINT<br/>PK]
        T2[trans_date_trans_time<br/>TIMESTAMP]
        T3[cc_num<br/>VARCHAR]
        T4[merchant<br/>VARCHAR]
        T5[category<br/>VARCHAR]
        T6[amount<br/>FLOAT]
        T7[gender<br/>VARCHAR]
        T8[street<br/>VARCHAR]
        T9[city<br/>VARCHAR]
        T10[state<br/>VARCHAR]
        T11[zip<br/>INTEGER]
        T12[lat<br/>FLOAT]
        T13[long<br/>FLOAT]
        T14[city_pop<br/>INTEGER]
        T15[job<br/>VARCHAR]
        T16[dob<br/>TIMESTAMP]
        T17[unix_time<br/>INTEGER]
        T18[merch_lat<br/>FLOAT]
        T19[merch_long<br/>FLOAT]
        T20[is_fraud<br/>BOOLEAN]
        T21[created_at<br/>TIMESTAMP]
    end
    
    style T1 fill:#ffe1e1
    style T6 fill:#e1f5ff
    style T20 fill:#e1ffe1
```

**Colonnes principales:**
- `trans_num`: Identifiant unique de la transaction (clé primaire)
- `trans_date_trans_time`: Date et heure de la transaction
- `amount`: Montant de la transaction
- `category`: Catégorie du marchand
- `is_fraud`: Label de fraude (ground truth)

### Table: PREDICTION

```mermaid
graph TD
    subgraph "PREDICTION Table"
        P1[id<br/>BIGINT<br/>PK<br/>AUTO_INCREMENT]
        P2[trans_num<br/>BIGINT<br/>FK]
        P3[is_fraud_prediction<br/>BOOLEAN]
        P4[confidence_score<br/>FLOAT]
        P5[model_version_id<br/>INTEGER<br/>FK]
        P6[prediction_time<br/>TIMESTAMP]
        P7[processing_time_ms<br/>FLOAT]
        P8[status<br/>VARCHAR]
    end
    
    style P1 fill:#ffe1e1
    style P3 fill:#e1f5ff
    style P4 fill:#e1ffe1
```

**Colonnes principales:**
- `id`: Identifiant unique de la prédiction
- `trans_num`: Référence vers la transaction
- `is_fraud_prediction`: Prédiction du modèle (0/1)
- `confidence_score`: Score de confiance (0-1)
- `model_version_id`: Version du modèle utilisée
- `processing_time_ms`: Temps de traitement en millisecondes

### Table: MODEL_VERSION

```mermaid
graph TD
    subgraph "MODEL_VERSION Table"
        M1[version_id<br/>INTEGER<br/>PK<br/>AUTO_INCREMENT]
        M2[model_name<br/>VARCHAR]
        M3[version_number<br/>INTEGER]
        M4[alias<br/>VARCHAR<br/>staging/prod]
        M5[created_at<br/>TIMESTAMP]
        M6[mlflow_run_id<br/>VARCHAR]
        M7[accuracy<br/>FLOAT]
        M8[precision<br/>FLOAT]
        M9[recall<br/>FLOAT]
        M10[f1_score<br/>FLOAT]
    end
    
    style M1 fill:#ffe1e1
    style M4 fill:#e1f5ff
    style M7 fill:#e1ffe1
```

**Colonnes principales:**
- `version_id`: Identifiant unique de la version
- `model_name`: Nom du modèle dans MLflow
- `version_number`: Numéro de version
- `alias`: Alias (staging, prod)
- `mlflow_run_id`: ID de la run MLflow

### Table: MONITORING_METRIC

```mermaid
graph TD
    subgraph "MONITORING_METRIC Table"
        O1[id<br/>INTEGER<br/>PK<br/>AUTO_INCREMENT]
        O2[metric_time<br/>TIMESTAMP]
        O3[accuracy<br/>FLOAT]
        O4[precision<br/>FLOAT]
        O5[recall<br/>FLOAT]
        O6[f1_score<br/>FLOAT]
        O7[drift_detected<br/>BOOLEAN]
        O8[drift_score<br/>FLOAT]
        O9[total_predictions<br/>INTEGER]
        O10[fraud_predictions<br/>INTEGER]
        O11[total_transactions<br/>INTEGER]
    end
    
    style O1 fill:#ffe1e1
    style O7 fill:#e1f5ff
    style O8 fill:#e1ffe1
```

### Table: ALERT_LOG

```mermaid
graph TD
    subgraph "ALERT_LOG Table"
        A1[id<br/>INTEGER<br/>PK<br/>AUTO_INCREMENT]
        A2[trans_num<br/>BIGINT<br/>FK]
        A3[alert_time<br/>TIMESTAMP]
        A4[alert_type<br/>VARCHAR]
        A5[recipient_email<br/>VARCHAR]
        A6[sent_successfully<br/>BOOLEAN]
        A7[error_message<br/>TEXT]
    end
    
    style A1 fill:#ffe1e1
    style A4 fill:#e1f5ff
    style A6 fill:#e1ffe1
```

## 🔗 Relations entre Tables

```mermaid
graph TD
    subgraph "Relations"
        R1[TRANSACTION]
        R2[PREDICTION]
        R3[MODEL_VERSION]
        R4[MONITORING_METRIC]
        R5[ALERT_LOG]
    end
    
    R1 -->|1:N| R2
    R3 -->|1:N| R2
    R1 -->|1:N| R4
    R1 -->|1:N| R5
    
    style R1 fill:#e1f5ff
    style R2 fill:#fff4e1
    style R3 fill:#e1ffe1
    style R4 fill:#ffe1e1
    style R5 fill:#e1f5ff
```

## 📦 Schéma des Données Kafka

### Message Structure (Topic: real-time-payments)

```mermaid
graph TD
    subgraph "Kafka Message Schema"
        K1[message_id<br/>UUID]
        K2[timestamp<br/>ISO8601]
        K3[transaction<br/>OBJECT]
        K4[metadata<br/>OBJECT]
    end
    
    subgraph "Transaction Object"
        T1[trans_num<br/>STRING]
        T2[trans_date_trans_time<br/>STRING]
        T3[cc_num<br/>STRING]
        T4[merchant<br/>STRING]
        T5[category<br/>STRING]
        T6[amount<br/>FLOAT]
        T7[gender<br/>STRING]
        T8[street<br/>STRING]
        T9[city<br/>STRING]
        T10[state<br/>STRING]
        T11[zip<br/>INTEGER]
        T12[lat<br/>FLOAT]
        T13[long<br/>FLOAT]
        T14[city_pop<br/>INTEGER]
        T15[job<br/>STRING]
        T16[dob<br/>STRING]
        T17[unix_time<br/>INTEGER]
        T18[merch_lat<br/>FLOAT]
        T19[merch_long<br/>FLOAT]
    end
    
    subgraph "Metadata Object"
        M1[source<br/>STRING]
        M2[producer_id<br/>STRING]
        M3[partition<br/>INTEGER]
        M4[offset<br/>BIGINT]
    end
    
    K1 --> K3
    K2 --> K4
    K3 --> T1
    K4 --> M1
    
    style K1 fill:#e1f5ff
    style K3 fill:#fff4e1
    style K4 fill:#e1ffe1
```

### Exemple de Message JSON

```json
{
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T10:30:00Z",
  "transaction": {
    "trans_num": "1234567890",
    "trans_date_trans_time": "2024-01-15 10:30:00",
    "cc_num": "************1234",
    "merchant": "Merchant Name",
    "category": "grocery_pos",
    "amount": 150.50,
    "gender": "F",
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": 10001,
    "lat": 40.7128,
    "long": -74.0060,
    "city_pop": 8400000,
    "job": "Engineer",
    "dob": "1990-01-01",
    "unix_time": 1705319400,
    "merch_lat": 40.7138,
    "merch_long": -74.0070
  },
  "metadata": {
    "source": "payment_api",
    "producer_id": "producer-1",
    "partition": 0,
    "offset": 12345
  }
}
```

## 🧪 Schéma des Features ML

### Features d'Entrée du Modèle

```mermaid
graph TD
    subgraph "Features Temporelles"
        FT1[trans_date_trans_time_month<br/>INTEGER<br/>1-12]
        FT2[trans_date_trans_time_hour<br/>INTEGER<br/>0-23]
        FT3[trans_date_trans_time_weekday<br/>INTEGER<br/>0-6]
        FT4[trans_date_trans_time_is_weekend<br/>BOOLEAN<br/>0/1]
    end
    
    subgraph "Features Catégorielles"
        FC1[category<br/>CATEGORICAL<br/>OneHot Encoded]
        FC2[gender<br/>CATEGORICAL<br/>OneHot Encoded]
        FC3[job<br/>CATEGORICAL<br/>OneHot Encoded]
    end
    
    subgraph "Features Numériques"
        FN1[amount<br/>FLOAT<br/>StandardScaler]
        FN2[city_pop<br/>INTEGER<br/>StandardScaler]
    end
    
    subgraph "Target"
        TG[is_fraud<br/>BOOLEAN<br/>0/1]
    end
    
    FT1 --> TG
    FT2 --> TG
    FT3 --> TG
    FT4 --> TG
    FC1 --> TG
    FC2 --> TG
    FC3 --> TG
    FN1 --> TG
    FN2 --> TG
    
    style FT1 fill:#e1f5ff
    style FC1 fill:#fff4e1
    style FN1 fill:#e1ffe1
    style TG fill:#ffe1e1
```

### Pipeline de Prétraitement des Features

```mermaid
graph TD
    subgraph "Input Features"
        IF1[Raw DataFrame]
    end
    
    subgraph "Date Features"
        DF1[Extract Month]
        DF2[Extract Hour]
        DF3[Extract Weekday]
        DF4[Is Weekend]
    end
    
    subgraph "Categorical Features"
        CF1[category<br/>OneHotEncoder]
        CF2[gender<br/>OneHotEncoder]
        CF3[job<br/>OneHotEncoder]
    end
    
    subgraph "Numeric Features"
        NF1[amount<br/>SimpleImputer<br/>+ StandardScaler]
        NF2[city_pop<br/>SimpleImputer<br/>+ StandardScaler]
    end
    
    subgraph "Output Features"
        OF[Feature Vector<br/>Array]
    end
    
    IF1 --> DF1
    IF1 --> CF1
    IF1 --> NF1
    DF1 --> OF
    DF2 --> OF
    DF3 --> OF
    DF4 --> OF
    CF1 --> OF
    CF2 --> OF
    CF3 --> OF
    NF1 --> OF
    NF2 --> OF
    
    style IF1 fill:#e1f5ff
    style DF1 fill:#fff4e1
    style CF1 fill:#e1ffe1
    style NF1 fill:#ffe1e1
    style OF fill:#e1f5ff
```

## 📊 Schéma de Monitoring

### Métriques de Performance

```mermaid
graph TD
    subgraph "ML Metrics"
        ML1[accuracy<br/>FLOAT]
        ML2[precision<br/>FLOAT]
        ML3[recall<br/>FLOAT]
        ML4[f1_score<br/>FLOAT]
        ML5[roc_auc<br/>FLOAT]
    end
    
    subgraph "Data Quality Metrics"
        DQ1[missing_values_ratio<br/>FLOAT]
        DQ2[duplicate_rows_ratio<br/>FLOAT]
        DQ3[feature_drift_score<br/>FLOAT]
        DQ4[target_drift_score<br/>FLOAT]
    end
    
    subgraph "System Metrics"
        SM1[prediction_latency_ms<br/>FLOAT]
        SM2[kafka_consumer_lag<br/>INTEGER]
        SM3[db_query_time_ms<br/>FLOAT]
        SM4[throughput_per_sec<br/>FLOAT]
    end
    
    subgraph "Business Metrics"
        BM1[fraud_detection_rate<br/>FLOAT]
        BM2[false_positive_rate<br/>FLOAT]
        BM3[alert_response_time_ms<br/>FLOAT]
        BM4[daily_fraud_count<br/>INTEGER]
    end
    
    style ML1 fill:#e1f5ff
    style DQ1 fill:#fff4e1
    style SM1 fill:#e1ffe1
    style BM1 fill:#ffe1e1
```

## 🔐 Schéma de Configuration

### Structure du Config YAML

```mermaid
graph TD
    subgraph "config.yaml"
        ROOT[Root Configuration]
        
        subgraph "data"
            D1[raw_path<br/>STRING]
            D2[processed_path<br/>STRING]
            D3[drop_columns<br/>LIST<br/>STRING]
            D4[target_column<br/>STRING]
        end
        
        subgraph "model"
            M1[test_size<br/>FLOAT]
            M2[random_state<br/>INTEGER]
            M3[model_type<br/>STRING]
        end
        
        subgraph "training"
            T1[epochs<br/>INTEGER]
            T2[batch_size<br/>INTEGER]
            T3[learning_rate<br/>FLOAT]
        end
        
        subgraph "mlflow"
            L1[tracking_uri<br/>STRING]
            L2[experiment_name<br/>STRING]
            L3[model_name<br/>STRING]
            L4[prod_alias<br/>STRING]
        end
        
        subgraph "monitoring"
            O1[reference_data_path<br/>STRING]
            O2[dashboard_path<br/>STRING]
            O3[report_path<br/>STRING]
        end
    end
    
    ROOT --> D1
    ROOT --> M1
    ROOT --> T1
    ROOT --> L1
    ROOT --> O1
    
    style ROOT fill:#f3e1ff
    style D1 fill:#e1f5ff
    style M1 fill:#fff4e1
    style L1 fill:#e1ffe1
    style O1 fill:#ffe1e1
```

## 📝 Index et Contraintes

### Index de Performance

```mermaid
graph TD
    subgraph "TRANSACTION Indexes"
        TI1[PRIMARY KEY<br/>trans_num]
        TI2[INDEX<br/>trans_date_trans_time]
        TI3[INDEX<br/>is_fraud]
        TI4[INDEX<br/>created_at]
    end
    
    subgraph "PREDICTION Indexes"
        PI1[PRIMARY KEY<br/>id]
        PI2[INDEX<br/>trans_num]
        PI3[INDEX<br/>prediction_time]
        PI4[INDEX<br/>is_fraud_prediction]
        PI5[INDEX<br/>model_version_id]
    end
    
    subgraph "MODEL_VERSION Indexes"
        MI1[PRIMARY KEY<br/>version_id]
        MI2[UNIQUE<br/>model_name + version_number]
        MI3[INDEX<br/>alias]
    end
    
    subgraph "MONITORING_METRIC Indexes"
        OI1[PRIMARY KEY<br/>id]
        OI2[INDEX<br/>metric_time]
    end
    
    style TI1 fill:#ffe1e1
    style PI1 fill:#e1f5ff
    style MI1 fill:#fff4e1
    style OI1 fill:#e1ffe1
```
