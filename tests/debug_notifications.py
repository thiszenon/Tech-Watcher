"""
Debug des notifications - Comprendre pourquoi plyer échoue
"""

import os
import sys
import platform
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def debug_environment():
    """Analyse l'environnement pour comprendre le problème"""
    print("🐛 DEBUG ENVIRONNEMENT NOTIFICATIONS")
    print("=" * 50)
    
    # 1. Informations système
    print("1. 📋 INFORMATIONS SYSTÈME:")
    print(f"   OS: {platform.system()}")
    print(f"   Version: {platform.version()}")
    print(f"   Release: {platform.release()}")
    print(f"   Machine: {platform.machine()}")
    
    # 2. Test Plyer directement
    print("\n2. 🔧 TEST PLYER DIRECT:")
    try:
        from plyer import notification
        print("   ✅ Plyer importé avec succès")
        
        # Essayer d'envoyer une notification
        notification.notify(
            title="Test Direct Plyer",
            message="Ceci est un test direct",
            timeout=5,
            app_name="Tech Watcher Debug"
        )
        print("   ✅ Notification Plyer envoyée (si tu la vois!)")
        
    except Exception as e:
        print(f"   ❌ Erreur Plyer: {e}")
        print(f"   💡 Plyer ne trouve pas d'implémentation pour ton OS")
    
    # 3. Test des commandes système natives
    print("\n3. 🖥️  TEST COMMANDES SYSTÈME:")
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("   🍎 Test commande macOS...")
        try:
            result = subprocess.run([
                'osascript', '-e', 
                'display notification "Test macOS" with title "Tech Watcher"'
            ], capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ Commande macOS fonctionne")
            else:
                print(f"   ❌ Commande macOS échoue: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Impossible d'exécuter commande macOS: {e}")
    
    elif system == "Linux":
        print("   🐧 Test commande Linux...")
        try:
            result = subprocess.run([
                'notify-send', 'Tech Watcher', 'Test Linux notification'
            ], capture_output=True, text=True)
            if result.returncode == 0:
                print("   ✅ Commande Linux fonctionne")
            else:
                print(f"   ❌ Commande Linux échoue: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Impossible d'exécuter commande Linux: {e}")
            print("   💡 Essaye: sudo apt install libnotify-bin")
    
    elif system == "Windows":
        print("   🪟 Test Windows...")
        # Windows a généralement une implémentation
        print("   ℹ️  Windows devrait normalement fonctionner avec plyer")
    
    # 4. Solutions possibles
    print("\n4. 🛠️  SOLUTIONS POSSIBLES:")
    print("   • Vérifier que ton OS supporte les notifications")
    print("   • Sur Linux: installer libnotify-bin")
    print("   • Sur certains environnements: notifications désactivées")
    print("   • Utiliser le fallback console (ce qu'on fait déjà)")

if __name__ == "__main__":
    debug_environment()