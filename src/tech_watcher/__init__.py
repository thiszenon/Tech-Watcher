
"""
Tech Watcher - Outil de veille technologique intelligent avec NLP
"""

__version__ = "1.0.0" 
__author__ = "Jonathan KABONGA NYATA"
__email__ = "jonathan.nyata@gmail.com"
__description__ = "Outil de monitoring tech avec notifications desktop mdrr va falloir que je sois plus explicite"

## Import des classes principales (Pas encore developpé)
try:
    from .core.watcher import TechWatcher
    from .core.config_manager import ConfigManager
    from .data_sources.github_client import GitHubClient
    from .notification.desktop_notifier import DesktopNotifier
except ImportError as ex:
    print(f"Erreur Import : {ex}")
    

__all__ = [
    "TechWatcher", 
    "ConfigManager",
    "__version__",
    "GitHubClient",
    "DesktopNotifier"
]