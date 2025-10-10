""" 
TOUS LES TESTS DE LA CLASSE config_manager.py
[o] TOUJOURS TESTER AVANT DE PASSER A AUTRE CHOSE 
"""
import sys
import os
#Ajouter le dossier src au chemin Python

sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))

from tech_watcher.core.config_manager import ConfigManager

def test_config_manager():
    print("Test du ConfigManager...")

    config = ConfigManager()
    print("GitHub enabled:", config.get('sources.github.enabled'))

    default_value = config.get('inexistant.chemin','VALEUR PAR DEFAUT')
    print("Valeur par defaut:",default_value)

if __name__ == "__main__":
    test_config_manager()
