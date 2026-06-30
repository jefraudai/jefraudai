# Configuration

## ⚙️ Vue d'ensemble de la Configuration

Le projet utilise un fichier YAML centralisé pour la configuration, avec possibilité de surcharge via variables d'environnement.

## 📁 Structure de Configuration

### Arborescence des Configs

```mermaid
graph TD
    subgraph "Configuration Files"
        CF1[config.yaml<br/>src/configs/]
        CF2[.env<br/>Root]
        CF3[.env.example<br/>Root]
        CF4[.env.secrets<br/>Root]
    end
    
    subgraph "Environment Variables"
        EV1[MLFLOW_TRACKING_URI]
        EV2[MLFLOW_EXPERIMENT_NAME]
        EV3[MLFLOW_MODEL_NAME]
        EV4[MLFLOW_PROD_ALIAS]
        EV5[DATABASE_URI]
    end
    
    subgraph "Configuration Loader"
        CL1[load_config]
        CL2[get_config_value]
        CL3[env_name_for_key]
        CL4[get_nested]
    end
    
    CF1 --> CL1
    CF2 --> CL1
    EV1 --> CL2
    CL2 --> CL3
    CL3 --> CL4
    
    style CF1 fill:#e1f5ff
    style EV1 fill:#fff4e1
    style CL1 fill:#e1ffe1
```

## 📄 config.yaml

### Structure Complète

```mermaid
graph TD
    subgraph "config.yaml"
        ROOT[Root Configuration]
        
        subgraph "data"
            D1[raw_path<br/>STRING]
            D2[processed_path<br/>STRING]
            D3[drop_columns<br/>LIST]
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
            L5[artifact_location<br/>STRING]
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

### Contenu du Fichier

```yaml
# Chemins données
data:
  raw_path: "data/raw/"
  processed_path: "data/processed/"
  # Colonnes à supprimer avant split / prétraitement
  drop_columns: [cc_num, merchant, first, last, street, trans_num, unix_time, dob, city, state, lat, long, merch_lat, merch_long]
  target_column: "is_fraud"

# Paramètres modèle
model:
  test_size: 0.2
  random_state: 42
  model_type: "auto_gluon"
  
# Paramètres entraînement
training:
  epochs: 100
  batch_size: 32
  learning_rate: 0.001

# MLflow
mlflow:
  tracking_uri: "https://jefraudai-mlflow.hf.space/"
  experiment_name: "Fraud_Detection"
  model_name: "fraud_detection_model"
  prod_alias: "prod"
  artifact_location: "jefraudai/mlflow"
  
# Evidently AI
monitoring:
  reference_data_path: "data/processed/reference.csv"
  dashboard_path: "outputs/evidently_dashboard.html"
  report_path: "outputs/evidently_report.html"
```

## 🔧 Configuration Loader

### Fonctions de Configuration

```mermaid
graph TD
    subgraph "Configuration Functions"
        F1[load_config]
        F2[get_nested]
        F3[env_name_for_key]
        F4[get_config_value]
        F5[get_mlflow_config]
    end
    
    subgraph "load_config"
        LC1[Read YAML File]
        LC2[Parse with yaml.safe_load]
        LC3[Return Dict or Empty]
    end
    
    subgraph "get_nested"
        GN1[Split Key by '.']
        GN2[Traverse Dict]
        GN3[Return Value or Default]
    end
    
    subgraph "env_name_for_key"
        EN1[Replace '.' with '_']
        EN2[Convert to Uppercase]
        EN3[Return Env Var Name]
    end
    
    subgraph "get_config_value"
        GC1[Get Env Var Name]
        GC2[Check os.getenv]
        GC3[Return Env or Config]
    end
    
    subgraph "get_mlflow_config"
        GM1[Load Config]
        GM2[Build MLflow Dict]
        GM3[Apply Env Overrides]
    end
    
    F1 --> LC1
    F2 --> GN1
    F3 --> EN1
    F4 --> GC1
    F5 --> GM1
    
    style F1 fill:#e1f5ff
    style LC1 fill:#fff4e1
    style GN1 fill:#e1ffe1
```

### Fonction: load_config

```python
def load_config(config_path=None):
    """Charge la configuration YAML depuis le dépôt."""
    path = Path(config_path or DEFAULT_CONFIG_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config or {}
```

### Fonction: get_nested

```python
def get_nested(config, key_path, default=None):
    """Récupère une valeur imbriquée à partir d'une clé de type 'a.b.c'."""
    if config is None:
        return default

    current = config
    for key in key_path.split("."):
        if not isinstance(current, dict):
            return default
        current = current.get(key)
        if current is None:
            return default
    return current
```

### Fonction: get_config_value

```python
def get_config_value(config, key_path, env_var=None, default=None):
    """Retourne la valeur d'une config avec override par variable d'environnement."""
    env_var = env_var or env_name_for_key(key_path)
    env_value = os.getenv(env_var)
    if env_value is not None:
        return env_value
    return get_nested(config, key_path, default)
```

### Fonction: get_mlflow_config

```python
def get_mlflow_config(config=None, config_path=None):
    """Retourne la configuration MLflow en appliquant les overrides d'environnement."""
    if config is None:
        config = load_config(config_path)

    return {
        "tracking_uri": get_config_value(config, "mlflow.tracking_uri", env_var="MLFLOW_TRACKING_URI"),
        "experiment_name": get_config_value(config, "mlflow.experiment_name", env_var="MLFLOW_EXPERIMENT_NAME", default="experiment"),
        "model_name": get_config_value(config, "mlflow.model_name", env_var="MLFLOW_MODEL_NAME", default="model"),
        "prod_alias": get_config_value(config, "mlflow.prod_alias", env_var="MLFLOW_PROD_ALIAS", default="prod"),
        "artifact_location": get_config_value(config, "mlflow.artifact_location", env_var="MLFLOW_ARTIFACT_LOCATION", default="jefraudai/mlflow"),
    }
```

## 🔐 Variables d'Environnement

### Mapping Config → Env Var

```mermaid
graph TD
    subgraph "Config Keys"
        CK1[mlflow.tracking_uri]
        CK2[mlflow.experiment_name]
        CK3[mlflow.model_name]
        CK4[mlflow.prod_alias]
        CK5[mlflow.artifact_location]
    end
    
    subgraph "Environment Variables"
        EV1[MLFLOW_TRACKING_URI]
        EV2[MLFLOW_EXPERIMENT_NAME]
        EV3[MLFLOW_MODEL_NAME]
        EV4[MLFLOW_PROD_ALIAS]
        EV5[MLFLOW_ARTIFACT_LOCATION]
    end
    
    CK1 --> EV1
    CK2 --> EV2
    CK3 --> EV3
    CK4 --> EV4
    CK5 --> EV5
    
    style CK1 fill:#e1f5ff
    style EV1 fill:#fff4e1
```

### Priorité de Configuration

```mermaid
graph TD
    subgraph "Priority Order"
        P1[1. Environment Variable<br/>Highest Priority]
        P2[2. config.yaml]
        P3[3. Default Value<br/>Lowest Priority]
    end
    
    P1 --> P2
    P2 --> P3
    
    style P1 fill:#ffe1e1
    style P2 fill:#fff4e1
    style P3 fill:#e1ffe1
```

## 📝 Sections de Configuration

### Section: data

```mermaid
graph TD
    subgraph "data Configuration"
        D1[raw_path<br/>data/raw/]
        D2[processed_path<br/>data/processed/]
        D3[drop_columns<br/>LIST of STRING]
        D4[target_column<br/>is_fraud]
    end
    
    subgraph "Drop Columns Details"
        DC1[cc_num<br/>Numéro de carte]
        DC2[merchant<br/>Nom marchand]
        DC3[first/last<br/>Nom client]
        DC4[street<br/>Adresse]
        DC5[trans_num<br/>ID transaction]
        DC6[unix_time<br/>Timestamp Unix]
        DC7[dob<br/>Date de naissance]
        DC8[city/state<br/>Localisation]
        DC9[lat/long<br/>Coordonnées]
        DC10[merch_lat/long<br/>Coordonnées marchand]
    end
    
    D3 --> DC1
    D3 --> DC2
    D3 --> DC3
    D3 --> DC4
    D3 --> DC5
    D3 --> DC6
    D3 --> DC7
    D3 --> DC8
    D3 --> DC9
    D3 --> DC10
    
    style D1 fill:#e1f5ff
    style DC1 fill:#fff4e1
```

### Section: model

```mermaid
graph TD
    subgraph "model Configuration"
        M1[test_size<br/>0.2]
        M2[random_state<br/>42]
        M3[model_type<br/>auto_gluon]
    end
    
    subgraph "Model Types"
        MT1[auto_gluon<br/>AutoML]
        MT2[random_forest<br/>Sklearn]
        MT3[linear_regression<br/>Sklearn]
    end
    
    M3 --> MT1
    M3 --> MT2
    M3 --> MT3
    
    style M1 fill:#e1f5ff
    style MT1 fill:#fff4e1
```

### Section: mlflow

```mermaid
graph TD
    subgraph "mlflow Configuration"
        L1[tracking_uri<br/>https://jefraudai-mlflow.hf.space/]
        L2[experiment_name<br/>Fraud_Detection]
        L3[model_name<br/>fraud_detection_model]
        L4[prod_alias<br/>prod]
        L5[artifact_location<br/>jefraudai/mlflow]
    end
    
    subgraph "MLflow Aliases"
        A1[staging<br/>Modèles en test]
        A2[prod<br/>Modèles en production]
        A3[archived<br/>Modèles archivés]
    end
    
    L4 --> A1
    L4 --> A2
    L4 --> A3
    
    style L1 fill:#e1f5ff
    style A1 fill:#fff4e1
```

### Section: monitoring

```mermaid
graph TD
    subgraph "monitoring Configuration"
        O1[reference_data_path<br/>data/processed/reference.csv]
        O2[dashboard_path<br/>outputs/evidently_dashboard.html]
        O3[report_path<br/>outputs/evidently_report.html]
    end
    
    subgraph "Evidently AI"
        E1[Data Drift Detection]
        E2[Data Quality Reports]
        E3[Performance Monitoring]
    end
    
    O2 --> E1
    O3 --> E2
    O1 --> E3
    
    style O1 fill:#e1f5ff
    style E1 fill:#fff4e1
```

## 🔒 Secrets Management

### .env File Structure

```mermaid
graph TD
    subgraph ".env File"
        E1[Database Credentials]
        E2[MLflow Credentials]
        E3[Kafka Credentials]
        E4[API Keys]
    end
    
    subgraph "Database"
        DB1[DATABASE_URI]
        DB2[DB_USER]
        DB3[DB_PASSWORD]
    end
    
    subgraph "MLflow"
        ML1[MLFLOW_TRACKING_URI]
        ML2[MLFLOW_USERNAME]
        ML3[MLFLOW_PASSWORD]
    end
    
    subgraph "Kafka"
        K1[KAFKA_BOOTSTRAP_SERVERS]
        K2[KAFKA_API_KEY]
        K3[KAFKA_API_SECRET]
    end
    
    subgraph "Email"
        EM1[RESEND_API_KEY]
        EM2[ALERT_EMAIL]
    end
    
    E1 --> DB1
    E2 --> ML1
    E3 --> K1
    E4 --> EM1
    
    style E1 fill:#e1f5ff
    style DB1 fill:#fff4e1
```

### .env.example

```bash
# Database
DATABASE_URI=postgresql://user:password@host:port/database
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# MLflow
MLFLOW_TRACKING_URI=https://jefraudai-mlflow.hf.space/
MLFLOW_EXPERIMENT_NAME=Fraud_Detection
MLFLOW_MODEL_NAME=fraud_detection_model
MLFLOW_PROD_ALIAS=prod

# Kafka
KAFKA_BOOTSTRAP_SERVERS=your-kafka-server:9092
KAFKA_API_KEY=your_api_key
KAFKA_API_SECRET=your_api_secret
KAFKA_TOPIC=real-time-payments

# Email
RESEND_API_KEY=your_resend_api_key
ALERT_EMAIL=alert@example.com
```

## 🎯 Utilisation de la Configuration

### Exemple d'Utilisation

```python
from fraud_detection.configuration import load_config, get_config_value, get_mlflow_config

# Charger la configuration
config = load_config()

# Récupérer une valeur simple
test_size = get_config_value(config, "model.test_size")

# Récupérer une valeur imbriquée
raw_path = get_nested(config, "data.raw_path")

# Récupérer la configuration MLflow
mlflow_config = get_mlflow_config()
print(mlflow_config['tracking_uri'])
```

### Override par Variable d'Environnement

```python
import os

# Définir une variable d'environnement
os.environ['MLFLOW_TRACKING_URI'] = 'https://custom-mlflow.example.com/'

# La fonction get_config_value utilisera la variable d'environnement
tracking_uri = get_config_value(config, "mlflow.tracking_uri")
# Retourne: 'https://custom-mlflow.example.com/'
```

## 📊 Validation de Configuration

### Schéma de Validation

```mermaid
graph TD
    subgraph "Validation Checks"
        V1[Check File Exists]
        V2[Check YAML Valid]
        V3[Check Required Keys]
        V4[Check Value Types]
        V5[Check Value Ranges]
    end
    
    subgraph "Required Keys"
        RK1[data.target_column]
        RK2[model.test_size]
        RK3[model.random_state]
        RK4[model.model_type]
        RK5[mlflow.tracking_uri]
    end
    
    V1 --> V2
    V2 --> V3
    V3 --> RK1
    V4 --> RK2
    V5 --> RK3
    
    style V1 fill:#e1f5ff
    style RK1 fill:#fff4e1
```

## 🔧 Configuration par Environnement

### Développement

```yaml
data:
  raw_path: "data/raw/"
  processed_path: "data/processed/"

model:
  test_size: 0.2
  random_state: 42
  model_type: "random_forest"  # Plus rapide pour le dev

mlflow:
  tracking_uri: "http://localhost:5000"
  experiment_name: "Fraud_Detection_Dev"
```

### Production

```yaml
data:
  raw_path: "s3://jefraudai/data/raw/"
  processed_path: "s3://jefraudai/data/processed/"

model:
  test_size: 0.2
  random_state: 42
  model_type: "auto_gluon"  # Meilleure performance

mlflow:
  tracking_uri: "https://jefraudai-mlflow.hf.space/"
  experiment_name: "Fraud_Detection_Prod"
```
