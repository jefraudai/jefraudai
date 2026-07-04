# Objectif pedagogique du projet
    
Concevoir et mettre en oeuvre des pipelines de données (pour l'IA)

Concevoir un système de gestion de données temps réel adapté aux contraintes et normes opérationnelles de l'entreprise, pour gérer efficacement la vélocité, le volume des flux, et la typologie des données.
Établir un pipeline de données à travers des processus ETL/ELT pour le transfert et la transformation des données entre différentes bases, en utilisant des outils de programmation, afin de répondre aux spécifications du cahier des charges.
Automatiser les flux de données dans le pipeline, en utilisant des outils spécifiques ou de la programmation, afin d'optimiser les performances de l'infrastructure de données.
Surveiller les flux de données pour assurer la qualité et le respect de la politique de gouvernance, en vue de maintenir les normes, la sécurité et la confidentialité dans les pipelines de données.
Développer des procédures de contrôle qualité et de correction des erreurs dans les pipelines de données, afin de garantir la qualité des données.


# Nom du projet

Automatic-Fraud-Detection


# Besoin du projet

- Être averti en temps réel qu'une fraude est détectée
- Une fois chaque matin, pouvoir vérifier tous les paiements et fraudes intervenus la veille.


# Architecture choisie

                 +----------------------+
                 | Payment API          |
                 +----------------------+
                            |
                            v
                 +----------------------+
                 | Kafka Producer       |
                 +----------------------+
                            |
                            v
                 +----------------------+
                 | Kafka Topic          |
                 +----------------------+
                            |
                            v
                 +----------------------+
                 | Fraud Consumer       |
                 | ML Prediction        |
                 +----------------------+
                            |
                            v
                 +----------------------+
                 | PostgreSQL           |
                 +----------------------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
      +------------------+       +-------------------+
      | Grafana          |       | Email             |
      | Monitoring       |       | Notification      |
      +------------------+       +-------------------+





# Améliorations possibles

Amélioration de la documentation
- Adapter les Schemas pour le format présentation
- Déploiement de Docsify et Slidev
- Déploiement de Slidev en 

## Améliorer le model avec des resssources moins limitées
- Ajouter des features pour une meilleure détection

## Amélioration Fonctionalité
- Orchestrateur pour potentiellement relancer les services Producer et Consumer

## Améliorations QA
- Nettoyer le code
- Tests unitaires
- Tests d'intégration

## Améliorations de code
- Créer une classe dédiée pour Autogluon

## Amélioration Infra
- Gérer les Variables Github en plus des Secrets
- Améliorer versioning
- Docker Compose
- K8s / Helm

## Améliorations supplémentaires
- Pipeline de réentraînement






# Lien utiles

## Cloud Accounts (JefraudAi)
- DB : https://console.neon.tech/app/projects/restless-shadow-27935644
- S3: https://supabase.com/dashboard/project/xjkkzjtjgdsmemheppgl/storage/files/buckets/mlflow-artifacts
- Kafka : https://cloud.redpanda.com/clusters/d8c0ur6uk85ifvcgnlrg/topics/real-time-payments/
- Emailing : https://resend.com/ (Jenedai Account)

## Prod
- API : https://sdacelo-real-time-fraud-detection.hf.space/
- MLflow : https://mlflai-mlflow.hf.space/#/models
- Producer : https://huggingface.co/spaces/jefraudai/Producer
- Kafka : https://cloud.redpanda.com/clusters/d8c0ur6uk85ifvcgnlrg/topics/real-time-payments/
- Consumer : https://huggingface.co/spaces/jefraudai/consumer
- Dashboard : https://jefraudai.grafana.net/public-dashboards/44a8ad6003bc4887880bfcfb8ebb6598?from=2023-12-04T13:55:58.556Z&to=2028-12-03T13:55:58.556Z&timezone=browser