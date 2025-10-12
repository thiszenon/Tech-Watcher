
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
    def get_trending_repos(self, language: str = "python")->List[Dict[str,Any]]:
        """
        Récuperer les repositories populaires GitHub
        """
        try:
            #Utilisation de l'API de recherche GitHub.
            url = f"{self.base_url}/search/repositories"
            params = {
                'q':f'language:{language} stars:>100',
                'sort': 'stars',
                'order': 'desc',
                'per_page':10
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
        





