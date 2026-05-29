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

- Etre averti dès qu'une fraude est détectée.
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
   | Grafana          |       | Airflow DAGs      |
   | Monitoring       |       | ETL / QA / Report |
   +------------------+       +-------------------+

