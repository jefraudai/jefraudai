"""
Gestion de l'inférence du modèle en production via MLflow
"""
import logging
import mlflow
import mlflow.sklearn
import mlflow.pyfunc
import numpy as np

from fraud_detection.configuration import get_mlflow_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InferenceModel:
    """Classe pour charger et utiliser un modèle en production"""
    
    def __init__(
        self,
        mlflow_tracking_uri=None,
        experiment_name=None,
        config_path=None,
    ):
        """
        Initialise la connexion MLflow en utilisant la configuration.
        
        Args:
            mlflow_tracking_uri: URI du serveur MLflow (optionnel)
            experiment_name: Nom de l'expérience MLflow (optionnel)
            config_path: Chemin vers le fichier de configuration YAML (optionnel)
        """
        
        mlflow_config = get_mlflow_config(config_path=config_path)

        self.mlflow_tracking_uri = mlflow_tracking_uri or mlflow_config.get("tracking_uri")
        self.experiment_name = experiment_name or mlflow_config.get("experiment_name")
        self.default_model_name = mlflow_config.get("model_name")
        self.default_prod_alias = mlflow_config.get("prod_alias") or "prod"
        self.model = None
        self.model_version = None

        if not self.mlflow_tracking_uri:
            raise ValueError(
                "Le paramètre 'mlflow_tracking_uri' est requis. "
                "Vérifiez la configuration MLflow ou fournissez-le explicitement."
            )

        mlflow.set_tracking_uri(self.mlflow_tracking_uri)
        mlflow.set_experiment(self.experiment_name)
        logger.info(f"MLflow connecté à {self.mlflow_tracking_uri}")
    
    def load_production_model(self, model_name=None, alias_prod=None):
        """
        Charge le modèle en production depuis MLflow via Alias
        
        Args:
            model_name: Nom du modèle dans MLflow (optionnel)
            alias_prod: Alias pour la production (optionnel)
            
        Returns:
            Modèle chargé ou None en cas d'erreur
        """
        model_name = model_name or self.default_model_name
        alias_prod = alias_prod or self.default_prod_alias

        if not model_name:
            logger.error("Le nom du modèle MLflow n'est pas défini.")
            return False

        try:
            # Récupérer la version avec l'alias prod
            client = mlflow.tracking.MlflowClient()
            model_version = client.get_model_version_by_alias(model_name, alias_prod)
            
            if not model_version:
                logger.error(f"Aucune version avec l'alias '{alias_prod}' pour {model_name}")
                return False
            
            self.model_version = model_version.version
            
            # Charger le modèle via alias
            model_uri = f"models:/{model_name}@{alias_prod}"
            
            # Essayer d'abord avec sklearn (compatible modèles sklearn)
            try:
                self.model = mlflow.sklearn.load_model(model_uri)
                logger.info(f"Modèle {model_name} v{self.model_version} chargé via sklearn")
            except Exception as sklearn_error:
                # Retomber sur pyfunc (pour AutoGluon et autres modèles custom)
                logger.warning(
                    f"Chargement sklearn échoué ({sklearn_error}), "
                    f"tentative chargement pyfunc pour {model_uri}"
                )
                self.model = mlflow.pyfunc.load_model(model_uri)
                logger.info(f"Modèle {model_name} v{self.model_version} chargé via pyfunc")
            
            logger.info(f"Modèle {model_name} v{self.model_version} prêt pour l'inférence")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {str(e)}")
            return False
    
    def predict(self, X_data):
        """
        Génère des prédictions
        
        Args:
            X_data: Features pour la prédiction (DataFrame ou array)
            
        Returns:
            Prédictions et scores de confiance
        """
        if self.model is None:
            logger.error("Modèle non chargé")
            return None, None
        
        try:
            predictions = self.model.predict(X_data)
            
            # Essayer de récupérer les scores de confiance
            confidence_scores = None
            if hasattr(self.model, 'predict_proba'):
                confidence_scores = self.model.predict_proba(X_data).max(axis=1)
            elif hasattr(self.model, 'decision_function'):
                confidence_scores = np.abs(self.model.decision_function(X_data))
            
            logger.info(f"Prédictions générées pour {len(X_data)} échantillons")
            return predictions, confidence_scores
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {str(e)}")
            return None, None
    
    def get_model_info(self):
        """Retourne les informations du modèle chargé"""
        if self.model is None:
            return None
        
        return {
            "model_type": type(self.model).__name__,
            "version": self.model_version,
            "n_features": getattr(self.model, 'n_features_in_', 'unknown')
        }
