"""
Chargement et préparation des données
"""
import pandas as pd
import numpy as np
from pathlib import Path

from fraud_detection.configuration import load_config


def load_data(file_path):
    """Charge les données depuis un fichier CSV"""
    data = pd.read_csv(file_path, sep=",", lineterminator="\n", encoding="utf-8")
    try:
        data = pd.read_csv(file_path, sep=",", lineterminator="\n", encoding="utf-8")
        # data = pd.read_csv(file_path, sep=None, engine="python")
        print(f"Données chargées avec succès_: {file_path}")
        print(f"Forme des données: {data.shape}")
        print(f"Colonnes: {list(data.columns)}")
        print(f"Types: {data.dtypes.to_dict()}")
        print(f"Head: {data.head(5)}")
        print("Attention: Moins de 2 colonnes détectées, vérifier le séparateur")
        # Vérifier les données
        if data.empty:
            print("Attention: Le fichier est vide")

        if data.isnull().sum().sum() > 0:
            print(f"Attention: {data.isnull().sum().sum()} valeurs manquantes détectées")
        
        return data
    except FileNotFoundError:
        print(f"Erreur: Fichier non trouvé - {file_path}")
        return None
    except Exception as e:
        print(f"Erreur lors du chargement: {e}")
        return None





def save_data(data, file_path):
    """Sauvegarde les données dans un fichier CSV"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(file_path, index=False)
    print(f"Données sauvegardées: {file_path}")
