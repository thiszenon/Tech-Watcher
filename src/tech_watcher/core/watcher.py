
"""
Moteur principal de Tech watcher 

"""

import time
import schedule
from typing import List, Dict, Any
import logging
from .config_manager import ConfigManager
from ..data_sources.github_client import GitHubClient
from ..notification.desktop_notifier import DesktopNotifier

logger = logging.getLogger(__name__)

class TechWatcher:
    """
    Classe principale qui orchestre la veille technologique

    """

    def __init__(self,config_path: str = None):
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config
        self.github_client = GitHubClient() # classe GitHuClient
        self.notifier = DesktopNotifier() # classe DesktopNotifier
        self.is_running = False 
        self._setup_logging()
        logger.info("Initialisation TechWatcher")

    #End __init__

    def _setup_logging(self):
        """Configuration du système de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s -%(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
    #End _setup_logging

    def collect_tech_news(self) -> List[Dict[str,Any]]:
        """Collecte les nouvelles technologies depuis toutes les sources,
        Pour l'instant github repositories
        """
        logger.info("début de la collecte des technologies...")

        all_news = [] # pour stocker toutes les nouvelles technos

        #1. GitHub trends !!! vérifier si github est activé dans defautl_config.yaml
        if self.config.get('sources', {}).get('github',{}).get('enabled',True):
            github_news = self.github_client.get_trending_repos() # voir détails dans la classe GitHubClient
            all_news.extend(github_news) # !== append
            logger.info(f"{len(github_news)} repos Github collectés")
        else:
            logger.info("Github désactivé dans la configuration")

        return all_news
    #End collect_tech_news
    
    def analyze_and_notify(self):
        """Analyse les données et envoie les notifications"""
        try:
            news_items = self.collect_tech_news() # recuperations des données collectées
            if not news_items:
                logger.info("Aucune nouvelle technologie trouvée")
                return 
            logger.info(f" {len(news_items)} élements à analyser")
            for item in news_items:
                #TODO :Tout notifier et Filtrer apres avec NLP !!!
                sucess = self.notifier.send(
                    title="Nouvelle tech detecté !",
                    message=f"{item.get('name','Unknown')}\n{item.get('description','')}",
                    timeout=10
                )
                if sucess:
                    logger.info(f"Notification envoyée pour :{item.get('name')}")
                else:
                    logger.warning(f"Echec notification pour:{item.get('name')}")
                #Mettre une pause entre les notifications
                time.sleep(10) #secondes  
        except Exception as ex:
            logger.error(f"Erreur lors de l'analyse: {ex}")

            #Notification d'erreur
            self.notifier.send(
                title=" Tech Watcher - Erreur",
                message = f"Erreur lors de la collecte:{str(ex)}",
                timeout=5
            )
    #End analyze_and_notify

    def start(self,interval_minutes: int=None):
        """Démarre le watcher en mode planning"""
        
        if interval_minutes is None:
            interval_minutes = self.config.get('sources',{}).get('github',{}).get('check_interval',60)
        logger.info(f"Tech Watcher démarré - Verification toutes les {interval_minutes} minutes")
        self.is_running = True # Mettre le watcher en marche 

        #Planification de l'execution regulière 
        schedule.every(interval_minutes).minutes.do(self.analyze_and_notify)

        #Première execution de collecte
        logger.info("Premiere verification immédiate...")
        self.analyze_and_notify()

        #Boucle principale du démarrage 
        while self.is_running:
            try:
                ...
            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as ex:
                logger.error(f"Erreur dans la boucle principale: {ex}")
                time.sleep(60) # Attendre avant de reéesayer
    #End start


    ####METHODES DES STATUS
    def stop(self):
        """Arreter le watcher"""
        self.is_running =False
        logger.info("Tech watcher arrêté")
    #End stop

    def get_status(self) -> Dict[str,Any]:
        """Retourne le statut actuel du watcher"""
        return {
            'running':self.is_running,
            'config_loaded': bool(self.config),
            'notifications_enabled': self.notifier.enabled
        }
    #End get_status

### POINT D'entrée Principal pour la commande tech-watcher à personnaliser 
def main():
    watcher = TechWatcher() 

    try:
        print("Tech watcher - Démarrage...")
        print("Conseil: Les notifications desktop apparaîtront pour les nouvelles technologies")
        print("Configuration chargée depuis :", watcher.config_manager.config_path)

        #demerrage
        watcher.start()
    except KeyboardInterrupt:
        watcher.stop() # Arreter le watcher peu importe le clavier .
        print("\n Tech Watcher arreté par l'utilisateur")
    except Exception as ex:
        print(f"Erreur : {ex}")
#End main()

if __name__ == "__main__":
    main()




        

