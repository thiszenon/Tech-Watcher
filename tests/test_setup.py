
"""
[o] -> Tests pour le setup.py et la configuration du package
"""

import os
import sys 
import subprocess
import importlib
from pathlib import Path
from run_single_test_method import run_single_test


## Class TestSetup
class TestSetup:
    """Classe de tests pour le setup """
    def __init__(self):
        self.results = {}

    #End __init__

    def test_package_import(self):
        """Test que le package est importé """
        try:
            # Essayer d'importer le package
            import tech_watcher
            assert tech_watcher.__version__ == "0.1.0"
            print("Import du package réussi")
            print(f" Version: {tech_watcher.__version__}")
            print(f" Auteur: {tech_watcher.__author__}")
            return True
        
        except ImportError as exImp:
            print(f" Erreur import package: {exImp}")
            return False
        except AssertionError:
            print(f"Version incorrecte")
            return False
    #End test_package_import

    def test_config_manager(self):
        """ Test que ConfigManager fonctionne"""
        print("\n TEST 2: ConfigMnager...")
        
        try:
            from tech_watcher.core.config_manager import ConfigManager
            config = ConfigManager()
            github_enabled = config.get("sources.github.enabled")
            print(f" Github enabled :{github_enabled}")
            return True
        except Exception as ex:
            print(f" Erreur ConfigManager: {ex}")
            return False
    #End test_config_manager

    def test_commands_availability(self):
        """Test que les commandes sont disponibles """
        print("\n TEST 3: Commandes système...")
        try:
            #Test de la commande tech-watcher
            result = subprocess.run(
                ["tech-watcher", "--help"],
                capture_output=True, text=True, timeout=10   
            )
            print("Commande 'tech-watcher' disponible")
            return True
        except Exception as ex:
            print(f" Commande 'tech-watcher': {ex}")
            return False
        


##EEXECUTION TEST
if __name__ == "__main__":
    # Ajouter src au path Python
    sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))

    test_runner = TestSetup()

    test_runner.run_single_test("test_commands_availability")


    

