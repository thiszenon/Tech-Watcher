
"""
Gestionnaire de configuration pour Tech Watcher
[o]: Voir les testes dans le dossier test.

"""
import os
import yaml
from typing import Dict, Any 

class ConfigManager:
    """ Ici, on gère la configuration de l'application"""

    def __init__(self, config_path:str = None ):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()

    def _get_default_config_path(self) -> str:
        """ Retourne le chemin par defaut du fichier de configuration"""

        # chemin ABSOLU depuis la racine du projet
        current_file = os.path.dirname(__file__) # dossier depuis ce fichier

        project_root = os.path.join(current_file,'..','..','..') # remonter à la racine 

        config_path = os.path.join(project_root,'config','default_config.yaml')

        return os.path.abspath(config_path) 
    
    def _load_config(self) -> Dict[str,Any]:
        """ Ici, on charge la configuration depuis le fichier YAML"""

        try:
            with open(self.config_path, 'r',encoding='utf-8') as file:
                config = yaml.safe_load(file) or {}
            print(f"Check-succ: Configuration chargée depuis {self.config_path}") 
            return config
            
        except Exception as ex:
            print(f"Check-fall: Erreur chargement config -> {ex}")
            return self._get_default_config()
        
    def _get_default_config(self,) -> Dict[str,Any]:
        """Retourne une configuration par défaut si le fichier est introuvable """
        return{
            'sources':{'github':{'enabled':True}},
            'notifications':{'enabled':True},
            'user': {'interests': ['python']}
        }
    
    def get(self,key:str, default=None):
        """ Récupère une valeur de configuration"""
        keys = key.split('.') #revoir l'argument de split()
        value = self.config

        for k in keys:
            if isinstance(value,dict) and k in value:
                value = value[k]
            else:
                return default
        return value
        


    
        