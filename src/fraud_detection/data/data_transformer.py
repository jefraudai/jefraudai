"""
Transformation des données avant entraînement
Permet de supprimer les colonnes configurées dans le YAML.
"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def drop_columns(data: pd.DataFrame, columns_to_drop):
    """Supprime les colonnes listées dans la configuration.

    Args:
        data: DataFrame à transformer
        columns_to_drop: liste des colonnes à supprimer

    Returns:
        DataFrame avec les colonnes supprimées
    """
    if data is None:
        raise ValueError("Aucune donnée fournie pour la suppression des colonnes")

    unnamed_columns = [col for col in data.columns if str(col).strip() == "" or str(col).startswith("Unnamed")]
    if unnamed_columns:
        logger.info(f"Détection de colonnes sans nom: {unnamed_columns}")

    if columns_to_drop is None:
        columns_to_drop = []

    if not isinstance(columns_to_drop, (list, tuple)):
        raise ValueError("drop_columns attend une liste de noms de colonnes")

    missing_columns = [col for col in columns_to_drop if col not in data.columns]
    columns_to_drop = [col for col in columns_to_drop if col in data.columns]

    if missing_columns:
        logger.warning(f"Colonnes à supprimer non trouvées dans les données: {missing_columns}")

    all_columns_to_drop = unnamed_columns + columns_to_drop
    if not all_columns_to_drop:
        logger.info("Aucune colonne valide à supprimer après vérification")
        return data.copy()

    transformed = data.drop(columns=all_columns_to_drop)
    logger.info(f"Supprimé {len(all_columns_to_drop)} colonne(s): {all_columns_to_drop}")
    return transformed
