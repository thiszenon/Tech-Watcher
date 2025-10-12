"""
Tests complets pour DesktopNotifier - Développement et test simultané
"""

import os
import sys
import time
import logging
from test_runner import TestRunner

# Ajoute src au path Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tech_watcher.notification.desktop_notifier import DesktopNotifier

class TestDesktopNotifier:
    """Tests pour le système de notifications desktop"""
    
    def __init__(self):
        self.notifier = DesktopNotifier()
        self.test_count = 0
        
    def test_initialization(self):
        """Test que le notifier s'initialise correctement"""
        print("\n🧪 TEST 1: Initialisation...")
        self.test_count += 1
        
        try:
            # Vérifie les attributs de base
            assert hasattr(self.notifier, 'enabled'), "Attribut 'enabled' manquant"
            assert hasattr(self.notifier, 'system'), "Attribut 'system' manquant"
            
            # Vérifie les valeurs par défaut
            assert self.notifier.enabled == True, "Notifications devraient être activées par défaut"
            assert self.notifier.system in ['Windows', 'Darwin', 'Linux'], f"OS non reconnu: {self.notifier.system}"
            
            print(f"✅ Notifier initialisé pour {self.notifier.system}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur initialisation: {e}")
            return False

    def test_basic_notification(self):
        """Test d'envoi d'une notification basique"""
        print("\n🧪 TEST 2: Notification basique...")
        self.test_count += 1
        
        try:
            # Envoie une notification de test
            success = self.notifier.send(
                title="🔔 Test Tech Watcher",
                message="Ceci est un test de notification!",
                timeout=3
            )
            
            assert success == True, "La notification devrait retourner True"
            print("✅ Notification basique envoyée avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur notification basique: {e}")
            return False

    def test_github_scenario_notification(self):
        """Test d'une notification réaliste type GitHub"""
        print("\n🧪 TEST 3: Scénario GitHub réel...")
        self.test_count += 1
        
        try:
            # Simulation d'un repo trending
            success = self.notifier.send(
                title="🚀 Nouveau Repo Trending",
                message="fastapi: Modern Python web framework\n⭐ 58,420 stars | 🐍 Python",
                timeout=5
            )
            
            assert success == True, "La notification GitHub devrait retourner True"
            print("✅ Notification GitHub scenario envoyée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur notification GitHub: {e}")
            return False

    def test_notification_toggle(self):
        """Test activation/désactivation des notifications"""
        print("\n🧪 TEST 4: Toggle notifications...")
        self.test_count += 1
        
        try:
            # Test désactivation
            self.notifier.disable()
            assert self.notifier.enabled == False, "Notifications devraient être désactivées"
            
            # Essayer d'envoyer une notification (devrait échouer)
            success_when_disabled = self.notifier.send(
                title="Ne devrait pas apparaître",
                message="Notifications désactivées",
                timeout=2
            )
            assert success_when_disabled == False, "Devrait retourner False quand désactivé"
            
            # Réactivation
            self.notifier.enable()
            assert self.notifier.enabled == True, "Notifications devraient être réactivées"
            
            # Vérifier que ça marche à nouveau
            success_when_enabled = self.notifier.send(
                title="✅ De retour!",
                message="Notifications réactivées avec succès",
                timeout=3
            )
            assert success_when_enabled == True, "Devrait retourner True quand réactivé"
            
            print("✅ Toggle notifications fonctionnel")
            return True
            
        except Exception as e:
            print(f"❌ Erreur toggle: {e}")
            return False

    def test_error_handling(self):
        """Test la gestion des erreurs"""
        print("\n🧪 TEST 5: Gestion d'erreurs...")
        self.test_count += 1
        
        try:
            # Test avec des paramètres extrêmes
            success = self.notifier.send(
                title="",  # Titre vide
                message="Test de résilience", 
                timeout=0  # Timeout 0
            )
            
            # Même avec des paramètres bizarres, ça ne devrait pas crasher
            print("✅ Gestion d'erreurs robuste")
            return True
            
        except Exception as e:
            print(f"❌ Le système a crashé: {e}")
            return False

    def run_interactive_test(self):
        """Test interactif - tu vois les vraies notifications"""
        print("\n🎯 TEST INTERACTIF - Regarde tes notifications!")
        print("=" * 50)
        
        tests = [
            ("🔔 Notification simple", "Hello Tech Watcher!"),
            ("🚀 Projet GitHub", "pandas: Data analysis library\n⭐ 45,000 stars"),
            ("🐛 Bug détecté", "Nouvelle CVE dans une de tes dépendances"),
            ("📈 Trend émergente", "Rust gagne 25% en adoption ce mois")
        ]
        
        for i, (title, message) in enumerate(tests, 1):
            print(f"\n{i}. {title}")
            print(f"   Message: {message}")
            input("   Appuye sur Entrée pour envoyer cette notification...")
            
            self.notifier.send(title, message, timeout=5)
            print("   ✅ Notification envoyée!")
        
        print("\n🎉 Test interactif terminé!")

# EXÉCUTION
if __name__ == "__main__":
    # Configure le logging pour voir les messages
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    notifier_tests = TestDesktopNotifier()
    runner = TestRunner(notifier_tests)
    
    print("🚀 DÉVELOPPEMENT & TEST - DESKTOP NOTIFIER")
    print("=" * 50)
    
    # Mode 1: Tests automatisés
    print("1. 🧪 TESTS AUTOMATISÉS")
    runner.run_all_tests()
    runner.print_summary()
    
    # Mode 2: Test interactif  
    print("\n2. 🎯 TEST INTERACTIF")
    notifier_tests.run_interactive_test()
    
    print(f"\n🎉 DÉVELOPPEMENT TERMINÉ - {notifier_tests.test_count} tests réalisés")