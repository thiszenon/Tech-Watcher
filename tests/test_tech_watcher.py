
"""
Tests pour le TechWatcher
"""
import os
import sys
import time
from pathlib import Path
from test_runner import TestRunner

# Ajouter src au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tech_watcher.core.watcher import TechWatcher

class TestTechWatcher:
    """Tests pour le TechWatcher principal"""
    
    def __init__(self):
        self.watcher = TechWatcher()
        self.results = {}
    #End __init__

    def test_watcher_initialization(self):
        """Test que le TechWatcher s'initialise correctement"""
        print("\n TEST 1: Initialisation du TechWatcher...")
        try:
            # Vérifie que les attributs sont définis
            assert hasattr(self.watcher, 'config_manager'), "config_manager manquant"
            assert hasattr(self.watcher, 'github_client'), "github_client manquant"
            assert hasattr(self.watcher, 'notifier'), "notifier manquant"
            assert hasattr(self.watcher, 'config'), "config manquant"
            assert hasattr(self.watcher, 'is_running'), "is_running manquant"

            # Vérifier l'état initial
            assert self.watcher.is_running == False, "Doit être arrêté au départ"
            assert self.watcher.config is not None, "Config doit être chargée"

            print("✅ TechWatcher initialisé correctement")
            print(f"   - Config chargée: {bool(self.watcher.config)}")
            print(f"   - GitHub client: {type(self.watcher.github_client).__name__}")
            print(f"   - Notifier: {type(self.watcher.notifier).__name__}")
            print(f"   - En cours d'exécution: {self.watcher.is_running}")
            
            return True
        
        except Exception as ex:
            print(f"❌ Erreur initialisation: {ex}")
            return False
    #End test_watcher_initialization

    def test_config_loading(self):
        """Teste le chargement de la configuration"""
        print("\n TEST 2: Chargement de la configuration...")
        try:
            config = self.watcher.config
            
            # Vérifier la structure de base
            assert isinstance(config, dict), "Config doit être un dictionnaire"
            assert 'sources' in config, "Section 'sources' manquante"
            assert 'github' in config['sources'], "Section 'github' manquante"
            assert 'notifications' in config, "Section 'notifications' manquante"

            # Vérifier les valeurs importantes
            github_enabled = config['sources']['github']['enabled']
            notifications_enabled = config['notifications']['enabled']
            
            print("✅ Configuration chargée correctement")
            print(f"   - GitHub enabled: {github_enabled}")
            print(f"   - Notifications enabled: {notifications_enabled}")
            print(f"   - Check interval: {config['sources']['github'].get('check_interval', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur chargement config: {e}")
            return False
    #End test_config_loading

    def test_collect_tech_news(self):
        """Teste la collecte des nouvelles technologies"""
        print("\n TEST 3: Collecte des nouvelles technologies...")
        try:
            start_time = time.time()
            news = self.watcher.collect_tech_news()
            response_time = time.time() - start_time
            
            print(f"⏱️  Temps de collecte: {response_time:.2f}s")

            # Vérifications de base
            assert isinstance(news, list), "Doit retourner une liste"
            print(f"📊 {len(news)} éléments collectés")

            if len(news) > 0:
                # Vérifier la structure des données
                first_item = news[0]
                expected_keys = ['name', 'description', 'url', 'stars', 'language', 'source']
                
                for key in expected_keys:
                    assert key in first_item, f"Clé manquante: {key}"
                
                print("✅ Structure des données correcte")
                print(f"   Exemple: {first_item['name']} ({first_item['stars']} ⭐)")
                
                # Afficher tous les éléments
                for i, item in enumerate(news, 1):
                    print(f"   {i}. {item['name']} - {item['stars']} stars - {item['language']}")
                    
            else:
                print("ℹ️  Aucune donnée collectée (peut être normal si API limitée)")
                
            return True
                
        except Exception as e:
            print(f"❌ Erreur collecte: {e}")
            import traceback
            traceback.print_exc()
            return False
    #End test_collect_tech_news

    def test_collect_with_github_disabled(self):
        """Teste la collecte quand GitHub est désactivé"""
        print("\n TEST 4: Collecte avec GitHub désactivé...")
        try:
            # Sauvegarder l'état original
            original_setting = self.watcher.config['sources']['github']['enabled']
            
            # Désactiver GitHub
            self.watcher.config['sources']['github']['enabled'] = False
            
            news = self.watcher.collect_tech_news()
            
            # Remettre l'état original
            self.watcher.config['sources']['github']['enabled'] = original_setting
            
            assert isinstance(news, list), "Doit retourner une liste"
            print(f"✅ Collecte avec GitHub désactivé: {len(news)} éléments")
            
            # Normalement devrait être 0 puisque GitHub est la seule source pour l'instant
            if len(news) == 0:
                print("   ✅ Aucune donnée (comportement attendu)")
            else:
                print("   ⚠️  Données trouvées (inattendu)")
                
            return True
            
        except Exception as e:
            print(f"❌ Erreur collecte GitHub désactivé: {e}")
            # S'assurer de remettre l'état original même en cas d'erreur
            self.watcher.config['sources']['github']['enabled'] = True
            return False
    #End test_collect_with_github_disabled

    def test_stop_method(self):
        """Teste la méthode stop"""
        print("\n TEST 5: Test de la méthode stop...")
        try:
            # S'assurer qu'il n'est pas en cours d'exécution
            self.watcher.is_running = False
            
            # Appeler stop() (ne devrait rien faire car pas en cours d'exécution)
            self.watcher.stop()
            
            # Vérifier qu'il est toujours arrêté
            assert self.watcher.is_running == False, "Doit rester arrêté"
            
            print("✅ Méthode stop fonctionne correctement")
            print("   - État après stop: arrêté")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur méthode stop: {e}")
            return False
    #End test_stop_method

    def test_get_status_method(self):
        """Teste la méthode get_status si elle existe"""
        print("\n TEST 6: Test de la méthode get_status...")
        try:
            # Vérifier si la méthode existe
            if hasattr(self.watcher, 'get_status') and callable(self.watcher.get_status):
                status = self.watcher.get_status()
                
                assert isinstance(status, dict), "Doit retourner un dictionnaire"
                print("✅ Méthode get_status fonctionne")
                print(f"   - Statut: {status}")
            else:
                print("ℹ️  Méthode get_status non implémentée (optionnel)")
                
            return True
            
        except Exception as e:
            print(f"❌ Erreur méthode get_status: {e}")
            return False
    #End test_get_status_method

if __name__ == "__main__":
    test_watcher = TestTechWatcher()
    test_runner = TestRunner(test_watcher)
    
    # Menu simple pour choisir quel test exécuter
    print("🚀 TEST TECH WATCHER")
    print("=" * 50)
    
    tests = {
        "1": "test_watcher_initialization",
        "2": "test_config_loading", 
        "3": "test_collect_tech_news",
        "4": "test_collect_with_github_disabled",
        "5": "test_stop_method",
        "6": "test_get_status_method",
        "7": "TOUS LES TESTS"
    }
    
    for key, value in tests.items():
        print(f"{key}. {value}")
    
    choice = input("\nChoisissez un test (1-7): ").strip()
    
    if choice in ["1", "2", "3", "4", "5", "6"]:
        test_name = tests[choice]
        test_runner.run_single_test(test_name)
    elif choice == "7":
        test_runner.run_all_tests()
    else:
        print("❌ Choix invalide")
    
    # Résumé
    test_runner.print_summary()
from test_runner import TestRunner

#Ajouter src au path python
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','src'))

from tech_watcher.core.watcher import TechWatcher

