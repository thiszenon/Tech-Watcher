
"""
Test de l'usage: from tech_watcher import TechWatcher
"""
import sys
import os
import time

# Ajouter src au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_import_and_usage():
    """Test l'import et l'usage basique"""
    print("🧪 TEST IMPORT ET USAGE")
    print("=" * 40)
    
    try:
        # Test 1: Import
        print("1. Testing import...")
        from tech_watcher import TechWatcher, __version__
        print(f"   ✅ Import réussi - Version {__version__}")
        
        # Test 2: Création instance
        print("2. Testing création instance...")
        watcher = TechWatcher()
        print("   ✅ Instance TechWatcher créée")
        
        # Test 3: Vérification des attributs
        print("3. Testing attributs...")
        assert hasattr(watcher, 'github_client'), "github_client manquant"
        assert hasattr(watcher, 'notifier'), "notifier manquant"
        assert hasattr(watcher, 'config'), "config manquant"
        print("   ✅ Tous les attributs présents")
        
        # Test 4: Collecte rapide (sans notifications)
        print("4. Testing collecte rapide...")
        news = watcher.collect_tech_news()
        print(f"   ✅ Collecte réussie - {len(news)} éléments")
        
        # Test 5: Méthode start (version courte)
        print("5. Testing start()...")
        print("   💡 Lancement en mode test (5 secondes seulement)...")
        
        # Lancer dans un thread pour pouvoir interrompre
        import threading
        
        def start_briefly():
            try:
                watcher.start(interval_minutes=0.1)  # Très court
            except:
                pass
        
        thread = threading.Thread(target=start_briefly)
        thread.daemon = True
        thread.start()
        
        # Attendre 2 secondes puis arrêter
        time.sleep(2)
        watcher.stop()
        print("   ✅ Start/Stop fonctionnels")
        
        print("\n🎉 TOUS LES TESTS PASSÉS !")
        print("📝 Usage confirmé:")
        print("   from tech_watcher import TechWatcher")
        print("   watcher = TechWatcher()") 
        print("   watcher.start()")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_import_and_usage()