
def test_imports():
    """Test les imports """
    print("Test les Imports")

    try:
        #Import depuis les sous-packages
        from tech_watcher.core import ConfigManager
        from tech_watcher.data_sources import GitHubClient
        print("Import depuis sous-packages réussi")
        return True
    except ImportError as exImp:
        print(f"Erreur import: {exImp}")
        return False
    
if __name__ == "__main__":
    test_imports()
    