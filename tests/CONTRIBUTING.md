# Guide de Contribution 
## Structure des branches
- `main`: Code stable
- `develop`: Développement en cours
- `feature/non-fonctionalié` : Nouvelles features

## Processus
1. Créer une branche feature depuis `develop`
2. Développer et tester
3. Faire une Pull Request vers `develop`
4. Après review , merge dans `develop`
5. Quand stable, merge `develop` dans `main`

## Installation
```bash
git clone [ton-repo]
cd Tech-Watcher
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
