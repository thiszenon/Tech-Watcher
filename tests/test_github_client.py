
"""
Tests pour le GitHubClient

"""
import os
import sys
import time
from pathlib import Path
from test_runner import TestRunner

#Ajouter src au path python
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))

from tech_watcher.data_sources.github_client import  GitHubClient

class TestGitHubClient:
    """Tests pour le client GitHub"""
    def __init__(self):
        self.client = GitHubClient()
        self.results = {}
    #End __init__

    def test_client_initialization(self):
        """ Test que le client s'initialise correctement"""
        print("\n TEST 1: Initialisation du client...")
        try:
            #Verfie que les attributs sont definis
            assert hasattr(self.client, 'base_url'), "base_url manquant"
            assert hasattr(self.client, 'session'), "session manquant"
            assert self.client.base_url == "https://api.github.com"

            #Verifier les headers de la session
            headers = self.client.session.headers
            assert 'Accept' in headers
            assert 'User-Agent' in headers
            assert headers['User-Agent'] == 'Tech-Watcher-App'

            print("Client initialisé correctement")
            print(f" Base URL: {self.client.base_url}")
            print(f" Headers: {dict(headers)}")
            return True
        
        except Exception as ex:
            print(f"Erreur initialisation: {ex}")
            return False
    #End test_client_initialization

    def test_get_trending_repos(self):
        """Teste la recupération des repos trending"""
        print("\n TEST 2: Recuperation des repos Github...")
        try:
            #appel de l'API
            start_time = time.time()
            repos = self.client.get_trending_repos(language="python")
            response_time = time.time() - start_time
            print(f" Temps de réponse: {response_time:.2f}s")

            #verifications
            size_repos = len(repos)
            assert isinstance(repos,list), "Doit retourner une liste"
            print(f"{size_repos} repositories recup")

            if size_repos > 0:
                #verifier la structure des données
                first_repos = repos[0]
                required_keys = ['name','description','url','stars','language','source']
                for key in required_keys:
                    assert key in first_repos, f"Clé manquante: {key}"
                      
                print(" Structure des données correcte")
                print(f"   Exemple: {first_repos['name']} ({first_repos['stars']} ⭐)")
                
                # Affiche tous les repos
                for i, repo in enumerate(repos, 1):
                    print(f"   {i}. {repo['name']} - {repo['stars']} stars")
                    
                return True
            else:
                print("Aucun repository récupéré (peut être normal si API limitée)")
                return True  # On considère que c'est OK (rate limiting)
                
        except Exception as e:
            print(f" Erreur récupération repos: {e}")
            import traceback
            traceback.print_exc()
            return False










if __name__ == "__main__":
    test_client = TestGitHubClient()
    test_runner = TestRunner(test_client)
    test_runner.run_single_test("test_get_trending_repos")


