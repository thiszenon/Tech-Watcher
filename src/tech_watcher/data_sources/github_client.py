
"""
Client pour l'API GitHub trends
"""

import requests
import time
from typing import List, Dict,Any
import logging

logger = logging.getLogger(__name__)

class GitHubClient:
    """
    Client pour récuperer les trending repositories GitHub
    """

    def __init__(self):
        """Initialisation de la session """
        self.base_url = "https://api.github.com"
        self.session =  requests.Session()
        self.session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Tech-Watcher-App'
        })
    #End __init__

    def get_trending_repos(self, language: str = "python")->List[Dict[str,Any]]:
        """
        Récuperer les repositories populaires GitHub avec 100 étoiles sans filtre de date pour l'instant 
        """
        try:
            #Utilisation de l'API de recherche GitHub.
            from datetime import datetime, timedelta
            
            #Que les trends de moins de 30 jours pour la nouveauté
            date_30_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

            url = f"{self.base_url}/search/repositories"
            params = {
                'q':f'language:{language} created:>={date_30_days_ago} stars:>20', #que les repos avec comme lang : PYTHON et qui ont plus de 20 étoils i.e populaire
                'sort': 'stars',
                'order': 'desc',
                'per_page':10 #nombre de repos à renvoyer 

            }#modification ulterieur voir fonctionnement

            response = self.session.get(url,params=params,timeout=10)
            response.raise_for_status()
            repos_data = response.json()['items'] #les données reçu de la reponse 

            #formatter les données
            formatted_repos = []
            for repo in repos_data:
                formatted_repos.append({
                    'name': repo['name'],
                    'description': repo['description'] or 'No description',
                    'url': repo['html_url'],
                    'stars':repo['stargazers_count'],
                    'language':repo['language'],
                    'topics':repo.get('topics',[]),
                    'source':'github',
                    'collected_at':time.time()
                })
            logger.info(f" {len(formatted_repos)} repositories GitHub récuperés")
            return formatted_repos
        
        except requests.RequestException as exReq:
            logger.error(f" Erreur API GitHub: {exReq}")
            return []
        except Exception as ex:
            logger.error(f"Erreur inattendue GitHub: {ex}")
            return []
    #End get_trending_repos

    
        





