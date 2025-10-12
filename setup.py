"""
[o]-> Packaging de l'application
[o]->
"""

from setuptools import setup, find_packages
import os


#Lecture du fichier README pour la description longue.
with open("README.md","r", encoding="utf-8") as file_r:
    long_description = file_r.read()

#Lecture du fichier requirements.txt
with open("requirements.txt","r",encoding="utf-8") as file_r:
    requirements = [line.strip() for line in file_r if line.strip() and not line.startswith("#")]

# Version dynamique
def get_version():
    """Retourne la version du package """
    version_file = os.path.join("src","tech_watcher","__init__.py") # pas encore créer
    try:
        with open(version_file,"r",encoding="utf-8") as file_r:
            for line in file_r:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"\'')
    except FileNotFoundError:
        print("Probleme Fichier __init__.py non trouvé, utilisation version par défaut ")
        return "0.1.0"
    

#Definition du SETUP
setup(
    name="tech-watcher",
    version=get_version(), # méthode definie au-dessus
    author= "Jonathan KABONGA NYATA",
    author_email="jonathan.nyata@gmail.com",
    description="Outil de veille technologique Intelligent avec NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",

    #Packages 
    packages=find_packages(where="src"),
    package_dir= {"": "src"},

    #Inclure les fichiers de données 
    package_data={
        "tech_watcher": ["../config/default_config.yaml"],
    },

    #Metadonnées pour l'utilisation de PyPI

    url="https://github.com/thiszenon/tech-watcher",
    project_urls = {
        "Bug Tracker": "https://github.com/thiszenon/tech-watcher/issues",
        "Documentation": "https://github.com/thiszenon/tech-watcher#readme",
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],

    keywords="technology, monitoring,nlp,automation,data-engineering",

    python_requires = ">=3.8",
    install_requires = requirements,

    #Les points d'entrées et commandes systèmes
    entry_points = {
        "console_scripts": [
            "tech-watcher=tech_watcher.core.watcher:main",
            "tech-watcher-config=tech_watcher.core.config_manager:main",
        ],
    },
    zip_safe = False,
    include_package_data=True,
    ##Autres Options à rajouter si besoin.

)

    
