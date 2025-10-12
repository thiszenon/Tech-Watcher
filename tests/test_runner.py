"""
Test Runner réutilisable pour tous les tests
"""

import time
from typing import Callable, Dict, List

class TestRunner:
    """
    Classe pour exécuter des tests de manière flexible
    Peut tester une méthode unique ou plusieurs méthodes
    """
    
    def __init__(self, test_class_instance):
        """
        Initialise le TestRunner avec une instance de classe de test
        
        Args:
            test_class_instance: Instance d'une classe contenant des méthodes de test
        """
        self.test_instance = test_class_instance
        self.results = {}
        self.execution_times = {}
    
    def run_single_test(self, test_name: str) -> bool:
        """
        Exécute une méthode de test spécifique
        
        Args:
            test_name: Nom de la méthode de test à exécuter
            
        Returns:
            bool: True si le test passe, False sinon
        """
        test_method = getattr(self.test_instance, test_name, None)
        
        if not test_method:
            print(f" Test '{test_name}' non trouvé")
            return False
        
        if not callable(test_method):
            print(f" '{test_name}' n'est pas une méthode appelable")
            return False
        
        print(f"\n EXECUTION du Test: {test_name}")
        print("-" * 40)
        
        try:
            start_time = time.time()
            result = test_method()
            execution_time = time.time() - start_time
            
            self.execution_times[test_name] = execution_time
            self.results[test_name] = result
            
            status = " RÉUSSI" if result else " ÉCHOUÉ"
            print(f"Résultat: {status} ({execution_time:.2f}s)")
            
            return result
            
        except Exception as e:
            print(f" Exception durant le test: {e}")
            import traceback
            traceback.print_exc()
            
            self.results[test_name] = False
            self.execution_times[test_name] = 0
            return False
    #End run_single_test

    
    def run_multiple_tests(self, test_names: List[str]) -> Dict[str, bool]:
        """
        Exécute plusieurs tests dans l'ordre spécifié
        
        Args:
            test_names: Liste des noms de méthodes à exécuter
            
        Returns:
            Dict[str, bool]: Résultats de chaque test
        """
        print(f"LANCEMENT DE {len(test_names)} TESTS")
        print("=" * 50)
        
        for test_name in test_names:
            self.run_single_test(test_name)# application de test_single_test sur chaque méthode
        
        return self.results
    #End run_multiple_test

    
    def run_all_tests(self) -> Dict[str, bool]:
        """
        Exécute toutes les méthodes qui commencent par 'test_'
        
        Returns:
            Dict[str, bool]: Résultats de tous les tests
        """
        # Trouve toutes les méthodes qui commencent par 'test_'
        test_methods = [
            method for method in dir(self.test_instance) 
            if method.startswith('test_') and callable(getattr(self.test_instance, method))
        ]
        
        test_methods.sort()  # Pour un ordre cohérent
        
        print(f"LANCEMENT DE TOUS LES TESTS ({len(test_methods)} trouvés)")
        print("=" * 50)
        
        return self.run_multiple_tests(test_methods)
    
    def print_summary(self):
        """Affiche un résumé détaillé des tests"""
        if not self.results:
            print("Aucun test exécuté")
            return
        
        print("\n" + "=" * 50)
        print("RÉSUMUM DÉTAILLÉ DES TESTS")
        print("=" * 50)
        
        total = len(self.results)
        passed = sum(1 for result in self.results.values() if result)
        
        for test_name, result in self.results.items():
            status = " RÉUSSI" if result else " ÉCHOUÉ"
            execution_time = self.execution_times.get(test_name, 0)
            print(f"  {test_name}: {status} ({execution_time:.2f}s)")
        
        print(f"\n TOTAL: {passed}/{total} tests passés")
        
        if passed == total:
            print("TOUS LES TESTS SONT RÉUSSIS!")
        else:
            print(f" {total - passed} TEST(S) ONT ÉCHOUÉ")

    #A DEVELOPPER PLUTARD
    def get_success_rate(self) -> float:
        """Retourne le taux de réussite des tests"""
        if not self.results:
            return 0.0
        return sum(self.results.values()) / len(self.results)