
"""
Système de notifications desktop pour Tech Watcher

"""

import logging
import platform
from typing import Optional

logger = logging.getLogger(__name__)

#Class DesktopNotifier
class DesktopNotifier:
    """ Gèrer les notifications desktop des platform"""
    def __init__(self):
        self.enabled = True
        self.system = platform.system() # pour reconnaitre le système d'exploitation
        logger.info(f" Initialisation de notifications pour {self.system}")
    #End __init__
    
    def send(self, title:str,message:str, timeout:int=10) -> bool:
        """
        Envoie une notification desktop

        Args:
            title: Titre de la notification
            message: Message de la notification
            timeout: durée d'affichage (par defaut 10 sec)

        Returns:
            bool: True si réussi, False sinon
        """
        if not self.enabled:
            return False
        try:
            #A Perfectionner pour une bonne vue 
            if self.system =="Darwin": # je ne savais pas avant aujourd'hui mdrr
                self._send_macos_notification(title,message)

            elif self.system == "Windows":
                self._send_windows_notification(title,message)

            elif self.system == "Linux":
                self._send_linux_notification(title,message)
            else:
                self._send_fallbcack_notification(title,message)
            logger.info(f" Notification envoyée: {title}")
            return True
        except Exception as exSend:
            logger.error(f"Erreur envoi notification: {exSend}")

            #Affichage Console
            print(f"{title}: {message}")
            return True #Ici on considere un fallback comme reussité à modifier 
        
    #End send

    def _send_macos_notification(self,title:str,message:str):
        """ Gestion de Notification pour le système macOs"""
        try:
            from plyer import notification
            notification.notify(
                title = title,
                message = message,
                timeout = 10,
                app_name = "Tech Watcher"
            )#notify
        except ImportError:
            #Fallback encore si plyer n'est pas installé
            import subprocess
            subprocess.run([
                'osascript', '-e',
                f'display notification "{message}" avec title "{title}"'
            ])
    #End _send_macos_notification

    def _send_windows_notification(self,title:str,message:str):
        """Notification pour windows"""
        try:
            from plyer import notification
            notification.notify(
                title = title,
                message = message,
                timeout = 10,
                app_name = "Tech Watcher"
            )
        except ImportError :
            #Fallback encore si plyer n'est pas installé
            print(f" {title}: {message}")
    #End _send_windows_notification

    def _send_rich_console_notification(self, title: str, message: str):
        """
        Notification console  pour environnements sans GUI
        Formatte les messages GitHub de manière lisible
        """
        import time
        from datetime import datetime
        
        print(f"TECH WATCHER - {datetime.now().strftime('%H:%M:%S')}")
        print(f" {title}")
        print("─" * 60)
        
        # Formatter intelligemment le message
        lines = message.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Détection du type de ligne pour un formatting intelligent
            if '⭐' in line and 'stars' in line.lower():
                # Ligne avec étoiles GitHub
                print(f"   🌟 {line}")
            elif '🐍' in line or 'python' in line.lower():
                # Ligne avec langage Python
                print(f"   🐍 {line}")
            elif any(lang in line.lower() for lang in ['rust', 'go', 'java', 'javascript']):
                # Ligne avec autre langage
                print(f"   💻 {line}")
            elif 'cve' in line.lower() or 'sécurité' in line.lower():
                # Ligne de sécurité
                print(f"   🛡️  {line}")
            elif line.startswith('http'):
                # Ligne URL
                print(f"   🔗 {line}")
            elif len(line) > 50:
                # Longue description - on la formate
                words = line.split()
                current_line = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) + 1 > 55:
                        print(f"   📝 {' '.join(current_line)}")
                        current_line = [word]
                        current_length = len(word)
                    else:
                        current_line.append(word)
                        current_length += len(word) + 1
                
                if current_line:
                    print(f"   📝 {' '.join(current_line)}")
            else:
                # Ligne normale
                print(f"   📝 {line}")
        
        print("─" * 60)
        print("💡 Conseil: En environnement local, vous verrez des popups!")
        print("🔔" * 50 + "\n")

    def _send_linux_notification(self,title:str, message:str):
        """Notification pour Linux"""
        """
        try:
            from plyer import notification
            notification.notify(
                title = title,
                message = message,
                timeout = 10,
                app_name = "Tech Watcher"
            )
        except ImportError:
            #Fallback avec notify-send
            import subprocess
            subprocess.run([
                'notify-send', title, message, '-t','10000'
            ])
        """
        self._send_rich_console_notification(title,message)
    #End _send_linux_notification


    def _send_fallbcack_notification(self,title:str,message:str):
        """ Méthode fallback Universel """
        print(f" TECH WATCHER ALERT")
        print(f"{title}")
        print(f" {message}")
        print("-"*50)
    #End _send_fallbcack_notification

    def enable(self):
        """"Activer les notifications"""
        self.enabled = True
        logger.info("Notification activées")
    #End enable
    
    def disable(self):
        """"Desactiver les notifications"""
        self.enabled = False
        logger.info("Notification désactivées")
    #End disable

    




