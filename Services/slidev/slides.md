---
theme: default
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## JefraudAI - Détection de Fraudes en Temps Réel
  Présentation du projet MLOps
drawings:
  persist: false
transition: slide-left
title: JefraudAI
mdc: true
---

# JefraudAI

## Système de Détection de Fraudes en Temps Réel

### Pipelines MLOps & Architecture Event-Driven

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Appuyez sur Espace pour la suite <carbon:arrow-right class="inline"/>
  </span>
</div>

<div class="abs-br m-6 flex gap-2">
  <a href="https://github.com/Jenedai/jefraudai" target="_blank" alt="GitHub"
    class="text-xl icon-btn opacity-50 !border-none !hover:text-white">
    <carbon-logo-github />
  </a>
</div>

---
transition: fade-out
---

# Objectifs Pédagogiques

Concevoir et mettre en œuvre des pipelines de données pour l'IA

<v-clicks>

- **Gestion de données temps réel** : Adapter le système pour gérer efficacement la vélocité, le volume et la typologie des données
- **Pipeline ETL/ELT** : Établir un pipeline de données pour le transfert et la transformation entre différentes bases
- **Automatisation** : Optimiser les performances de l'infrastructure de données par l'automatisation des flux
- **Surveillance** : Assurer la qualité et le respect de la politique de gouvernance des données
- **Contrôle qualité** : Développer des procédures de contrôle qualité et de correction des erreurs

</v-clicks>

---
transition: fade-out
---

# Besoin du Projet

<v-clicks>

## Alertes en temps réel
Être averti dès qu'une fraude est détectée

## Rapport quotidien
Pouvoir vérifier chaque matin tous les paiements et fraudes intervenus la veille

</v-clicks>

---
transition: slide-left
---

# Architecture Générale

```mermaid
flowchart LR
    A[Payment API] --> B[Kafka Producer]
    B --> C[Kafka Topic]
    C --> D[Fraud Consumer]
    D --> E[ML Prediction]
    E --> F[PostgreSQL]
    F --> G[Grafana Monitoring]
    F --> H[Email Notification]
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#ffe1e1
    style D fill:#e1ffe1
    style E fill:#f0e1ff
    style F fill:#e1f5ff
    style G fill:#ffe1f0
    style H fill:#f0ffe1
```

---
transition: slide-left
---

# Technologies Utilisées

<div class="grid grid-cols-2 gap-4 pt-4">

<div>

## Infrastructure Cloud
- **Kafka (Redpanda)** : Streaming de messages
- **PostgreSQL (Neon)** : Base de données
- **MLflow (HF Spaces)** : Tracking ML
- **Grafana** : Monitoring
- **Resend** : Emails

</div>

<div>

## Machine Learning
- **AutoGluon** : AutoML
- **Scikit-learn** : ML classique
- **Evidently AI** : Monitoring
- **Pandas/NumPy** : Data

</div>

</div>

---
transition: slide-left
---

# Flux de Données Temps Réel

```mermaid
flowchart LR
    subgraph Source["Source de Données"]
        API[Payment API]
    end
    
    subgraph Ingestion["Ingestion"]
        Producer[Kafka Producer]
    end
    
    subgraph Streaming["Streaming Layer"]
        Topic[Kafka Topic<br/>real-time-payments]
    end
    
    subgraph Processing["Traitement"]
        Consumer[Kafka Consumer]
        ML[ML Prediction Model]
    end
    
    subgraph Storage["Stockage"]
        DB[(PostgreSQL)]
    end
    
    subgraph Monitoring["Monitoring & Alertes"]
        Grafana[Grafana Dashboard]
        Email[Email Notifications]
    end
    
    API --> Producer
    Producer --> Topic
    Topic --> Consumer
    Consumer --> ML
    ML --> DB
    DB --> Grafana
    DB --> Email
```

---
transition: slide-left
---

# Pipeline d'Entraînement ML

```mermaid
flowchart LR
    Load[Chargement] --> Validate[Validation]
    Validate --> Transform[Transformation]
    Transform --> Prep[Préparation]
    Prep --> Train[Entraînement]
    Train --> Eval[Évaluation]
    Eval --> Monitor[Monitoring]
    Monitor --> MLflow[Logging MLflow]
    MLflow --> Staging[Staging]
    Staging --> Prod[Production]
    
    style Load fill:#e1f5ff
    style Validate fill:#fff4e1
    style Transform fill:#ffe1e1
    style Prep fill:#ffe1e1
    style Train fill:#e1ffe1
    style Eval fill:#e1ffe1
    style Monitor fill:#f0e1ff
    style MLflow fill:#f0e1ff
    style Staging fill:#ffe1f0
    style Prod fill:#ffe1f0
```

---
transition: slide-left
---

# Étapes du Pipeline d'Entraînement

<v-clicks>

1. **Chargement des données** : Import depuis CSV, validation du format
2. **Validation qualité** : Evidently AI, détection d'outliers
3. **Transformation** : Nettoyage, imputation, encoding, scaling
4. **Entraînement** : AutoGluon avec auto-tuning
5. **Évaluation** : Accuracy, Precision, Recall, F1, ROC-AUC
6. **Monitoring** : Data drift, concept drift
7. **Logging MLflow** : Métriques, paramètres, artefacts
8. **Gestion des stages** : Promotion Staging → Production

</v-clicks>

---
transition: slide-left
---

# Pipeline de Prédiction

```mermaid
flowchart LR
    Data[Transaction] --> Clean[Nettoyage]
    Clean --> Features[Extraction]
    Features --> Load[Chargement Modèle]
    Load --> Predict[Prédiction]
    Predict --> Score[Score]
    Predict --> Pred[Prediction]
    Score --> DB[PostgreSQL]
    Pred --> DB
    Pred --> Email[Email Alert]
    
    style Data fill:#e1f5ff
    style Clean fill:#fff4e1
    style Features fill:#fff4e1
    style Load fill:#e1ffe1
    style Predict fill:#e1ffe1
    style Score fill:#f0e1ff
    style Pred fill:#f0e1ff
    style DB fill:#e1f5ff
    style Email fill:#f0ffe1
```

---
transition: slide-left
---

# Kafka Producer

```mermaid
flowchart LR
    API[Payment API] --> Fetch[Fetch Transaction]
    Fetch --> Process[Process Data]
    Process --> Serialize[Serialize JSON]
    Serialize --> Publish[Publish to Kafka]
    Publish --> Topic[Topic real-time-payments]
    
    style API fill:#e1f5ff
    style Fetch fill:#fff4e1
    style Process fill:#fff4e1
    style Serialize fill:#fff4e1
    style Publish fill:#fff4e1
    style Topic fill:#ffe1e1
```

**Fonctionnalités** :
- Polling de l'API Payment
- Sécurité SASL_SSL avec SCRAM-SHA-256
- Clé : `trans_num`
- Callbacks succès/erreur

---
transition: slide-left
---

# Kafka Consumer

```mermaid
flowchart LR
    Topic[Topic] --> Consume[Consume Message]
    Consume --> Deserialize[Deserialize JSON]
    Deserialize --> Preprocess[Preprocess Data]
    Preprocess --> Predict[ML Prediction]
    Predict --> Decide[Decision]
    Decide --> DB[PostgreSQL]
    Decide --> Email[Email Service]
    
    style Topic fill:#ffe1e1
    style Consume fill:#e1ffe1
    style Deserialize fill:#e1ffe1
    style Preprocess fill:#e1ffe1
    style Predict fill:#f0e1ff
    style Decide fill:#f0e1ff
    style DB fill:#e1f5ff
    style Email fill:#f0ffe1
```

**Fonctionnalités** :
- Consommation temps réel
- Prétraitement des données
- Inférence ML
- Stockage PostgreSQL
- Alertes email si fraude

---
transition: slide-left
---

# MLflow Tracking & Registry

```mermaid
flowchart LR
    Pipeline[ML Pipeline] --> Tracking[Tracking Server]
    Metrics[Métriques] --> Tracking
    Params[Paramètres] --> Tracking
    Tracking --> Registry[Model Registry]
    Registry --> Artifacts[Artifact Store]
    Registry --> Staging[Staging Alias]
    Staging --> Prod[Production Alias]
    
    style Pipeline fill:#e1ffe1
    style Metrics fill:#fff4e1
    style Params fill:#fff4e1
    style Tracking fill:#f0e1ff
    style Registry fill:#f0e1ff
    style Artifacts fill:#f0e1ff
    style Staging fill:#ffe1f0
    style Prod fill:#ffe1f0
```

**Fonctionnalités** :
- Tracking des expériences
- Model Registry avec aliases
- Artifact Store sur Supabase S3
- Promotion automatique

---
transition: slide-left
---

# Séquence de Détection de Fraude

```mermaid
sequenceDiagram
    participant API as Payment API
    participant Prod as Kafka Producer
    participant Kafka as Kafka Topic
    participant Cons as Kafka Consumer
    participant ML as ML Model
    participant DB as PostgreSQL
    participant Email as Email Service
    
    API->>Prod: Transaction JSON
    Prod->>Prod: Fetch transaction
    Prod->>Kafka: Publish message
    Kafka->>Cons: Consume message
    Cons->>Cons: Preprocess data
    Cons->>ML: Predict
    ML->>Cons: Prediction + Score
    Cons->>DB: Store prediction
    alt Fraud detected
        Cons->>Email: Send alert
        Email->>Email: Deliver notification
    end
```

---
transition: slide-left
---

# Architecture de Déploiement

```mermaid
flowchart LR
    Dev[Code Python] --> GitHub[GitHub Actions]
    Poetry[Poetry] --> Dev
    GitHub --> HF[HuggingFace Spaces]
    HF --> Redpanda[Redpanda Cloud]
    HF --> Neon[Neon PostgreSQL]
    HF --> Supabase[Supabase S3]
    Neon --> GrafanaCloud[Grafana Cloud]
    HF --> Resend[Resend Email]
    
    style Dev fill:#e1f5ff
    style Poetry fill:#fff4e1
    style GitHub fill:#e1ffe1
    style HF fill:#f0e1ff
    style Redpanda fill:#ffe1e1
    style Neon fill:#e1f5ff
    style Supabase fill:#fff4e1
    style GrafanaCloud fill:#ffe1f0
    style Resend fill:#f0ffe1
```

---
transition: slide-left
---

# Services de Production

<div class="grid grid-cols-2 gap-4 pt-4">

<div>

## Déployés sur HuggingFace Spaces
- **API** : https://sdacelo-real-time-fraud-detection.hf.space/
- **MLflow** : https://jefraudai-mlflow.hf.space/#/models
- **Producer** : https://huggingface.co/spaces/jefraudai/Producer
- **Consumer** : https://huggingface.co/spaces/jefraudai/consumer

</div>

<div>

## Cloud Services
- **Kafka** : Redpanda Cloud
- **PostgreSQL** : Neon (serverless)
- **S3** : Supabase Storage
- **Monitoring** : Grafana Cloud
- **Email** : Resend API

</div>

</div>

---
transition: slide-left
---

# Monitoring & Observabilité

<v-clicks>

## Grafana Dashboard
- Visualisation des prédictions en temps réel
- Statistiques de fraudes
- Métriques de performance

## Evidently AI
- Data Quality Reports
- Data Drift Detection
- Model Performance Monitoring

## MLflow Tracking
- Expériences ML
- Model Registry
- Artefacts et logs

</v-clicks>

---
transition: slide-left
---

# Sécurité

<v-clicks>

## Authentification Kafka
- Protocole : SASL_SSL
- Mécanisme : SCRAM-SHA-256
- Credentials : Variables d'environnement

## Base de données
- Connection string sécurisée
- SSL/TLS activé

## Secrets Management
- GitHub Secrets pour production
- `.env` pour développement local
- `.env.secrets` non versionné

</v-clicks>

---
transition: slide-left
---

# Scalabilité & Résilience

<v-clicks>

## Horizontal Scaling
- Kafka Consumer : Plusieurs instances
- Kafka Producer : Distribué

## Vertical Scaling
- ML Model : Cache en mémoire
- PostgreSQL : Auto-scaling Neon

## Gestion des erreurs
- Retry automatique API
- Gestion offsets Kafka
- Logs structurés

</v-clicks>

---
transition: slide-left
---

# Structure du Projet

```
jefraudai/
├── src/
│   └── fraud_detection/
│       ├── data/              # Chargement et préparation
│       ├── models/            # Modèles ML et MLflow
│       ├── monitoring/        # Monitoring performance
│       └── pipelines/         # Pipelines ML
├── Services/
│   ├── Producer/              # Kafka Producer
│   ├── consumer/              # Kafka Consumer
│   └── MLflow/                # MLflow Service
├── notebooks/                 # Jupyter Notebooks
├── infra/                     # Infrastructure
└── docs/                      # Documentation
```

---
transition: slide-left
---

# Configuration

```yaml
data:
  target_column: is_fraud
  drop_columns: []

model:
  model_type: auto_gluon
  test_size: 0.2
  random_state: 42

mlflow:
  tracking_uri: "https://jefraudai-mlflow.hf.space"
  experiment_name: "fraud_detection"
  model_name: "fraud_model"
  prod_alias: "prod"
  artifact_location: "jefraudai/mlflow"

monitoring:
  report_path: "reports"
```

---
transition: slide-left
---

# Améliorations Futures

<v-clicks>

## À faire
- Vérifier que les fraudes sont détectées

## Améliorations fonctionnelles
- Orchestrateur pour relancer les services

## Améliorations QA
- Nettoyer le code
- Tests unitaires
- Tests d'intégration

## Améliorations infra
- Gérer les variables GitHub
- Docker Compose
- Kubernetes / Helm

## Améliorations ML
- Pipeline de réentraînement automatique

</v-clicks>

---
transition: slide-left
---

# Conclusion

<v-clicks>

## Réalisations
- ✅ Pipeline temps réel avec Kafka
- ✅ Pipeline ML complet avec MLflow
- ✅ Monitoring avec Grafana et Evidently
- ✅ Déploiement sur HuggingFace Spaces
- ✅ Alertes email en temps réel

## Objectifs pédagogiques atteints
- ✅ Gestion de données temps réel
- ✅ Pipeline ETL/ELT
- ✅ Automatisation des flux
- ✅ Surveillance de la qualité
- ✅ Contrôle qualité

</v-clicks>

---
transition: fade-out
---

# Merci de votre attention

<div class="pt-12">
  <span class="text-center">
    Questions ?
  </span>
</div>

<div class="abs-br m-6 flex gap-2">
  <a href="https://github.com/Jenedai/jefraudai" target="_blank" alt="GitHub"
    class="text-xl icon-btn opacity-50 !border-none !hover:text-white">
    <carbon-logo-github />
  </a>
</div>
