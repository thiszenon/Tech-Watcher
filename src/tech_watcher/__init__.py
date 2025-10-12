
"""
Tech Watcher - Outil de veille technologique intelligent avec NLP
"""

__version__ = "0.1.0"
__author__ = "Jonathan KABONGA NYATA"
__email__ = "jonathan.nyata@gmail.com"

## Import des classes principales (Pas encore developpé)
try:
    from .core.watcher import TechWatcher
    from .core.config_manager import ConfigManager
except ImportError:
    ...
    pass

__all__ = ["TechWatcher", "ConfigManager", "__version__"]