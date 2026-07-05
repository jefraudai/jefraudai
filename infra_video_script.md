# Infrastructure de Production - Détection de Fraude en Temps Réel

## Introduction

Bienvenue dans cette présentation de l'infrastructure de détection de fraude en temps réel. Je vais vous montrer l'architecture complète de notre solution déployée en production.

## Architecture Générale

Le système de détection de fraude est basé sur une architecture événementielle distribuée avec les composants suivants :

### Composants Principaux

**1. Kafka (Aiven Cloud)**
- Producer Service : Récupère les transactions depuis l'API HuggingFace
- Consumer Service : Traite les messages et applique le modèle ML
- Topic : `real-time-payments`
- Sécurité : SASL_SSL avec authentification PLAIN
- Rate limiting : 12 secondes entre chaque appel API (5 appels/minute max)

**2. MLflow (HuggingFace Spaces)**
- Tracking URI : https://mlflai-mlflow.hf.space/
- Modèle en production : `fraud_detection_model` (alias `prod`)
- Type : AutoGluon TabularPredictor
- Version : v5
- Gestion centralisée des runs et modèles

**3. PostgreSQL (Supabase)**
- Base de données pour stockage des prédictions
- Table principale : `predictions`
- Schéma :
  - `trans_num` (PK) : Identifiant transaction
  - `cc_num` : Numéro de carte
  - `merchant`, `category`, `amt`, `city`, `state` : Détails
  - `is_fraud_true` : Étiquette réelle
  - `is_fraud_pred` : Prédiction modèle (0/1)
  - `fraud_score` : Score probabilité
  - `predicted_at` : Timestamp prédiction

**4. API Transactions (HuggingFace Spaces)**
- Endpoint : https://sdacelo-real-time-fraud-detection.hf.space/current-transactions
- Fournit transactions de test en temps réel
- Rate limit : 5 appels/minute

## Flux de Données

```
API HuggingFace → Producer Kafka → Topic Kafka → Consumer Kafka → MLflow Model → PostgreSQL
```

**Étape 1** : Producer interroge l'API toutes les 12 secondes
**Étape 2** : Transactions sérialisées en JSON et publiées sur Kafka
**Étape 3** : Consumer consomme les messages, prétraite les données
**Étape 4** : Modèle AutoGluon appliqué via MLflow
**Étape 5** : Prédictions stockées dans PostgreSQL

## Déploiement

**Containerisation**
- Producer : Docker avec librdkafka
- Consumer : Docker avec librdkafka et dépendances ML
- Orchestration : GitHub Actions vers HuggingFace Spaces

**Configuration**
- Secrets via GitHub Secrets
- Config centralisée dans `src/configs/config.yaml`
- Certificats SSL pour Kafka Aiven

## Monitoring

**Logs**
- Structurés avec timestamps
- Diagnostics connectivité Kafka
- Logging prédictions et erreurs

**Alertes**
- Resend pour notifications email (fraudes détectées)
- SMTP configuré pour alertes temps réel

## Sécurité

- Kafka : SASL_SSL
- PostgreSQL : Connection string sécurisée
- Secrets : GitHub Secrets et variables d'environnement
- SSL/TLS : Certificats communications sécurisées

## Performances

- Latence : < 1 seconde bout en bout
- Débit : Centaines de transactions/seconde
- Scalabilité : Partitionnement Kafka possible

## Conclusion

Cette infrastructure permet une détection de fraude en temps réel avec une architecture événementielle résiliente, un modèle ML géré via MLflow, un stockage persistant pour analyse, et un déploiement cloud-native sur HuggingFace Spaces et Aiven.

---
*Infrastructure de production pour détection de fraude en temps réel*
