#!/usr/bin/env python3
"""
Script d'installation final pour CV Processing API
Résout tous les problèmes de dépendances
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Exécute une commande et affiche le résultat"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Succès")
            return True
        else:
            print(f"❌ {description} - Échec")
            print(f"Erreur: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Erreur: {str(e)}")
        return False

def check_python_version():
    """Vérifie la version de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ est requis")
        print(f"Version actuelle: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def clean_environment():
    """Nettoie l'environnement existant"""
    if os.path.exists("venv"):
        print("🗑️ Suppression de l'environnement virtuel existant...")
        try:
            if platform.system() == "Windows":
                subprocess.run("rmdir /s /q venv", shell=True, check=True)
            else:
                subprocess.run("rm -rf venv", shell=True, check=True)
            print("✅ Ancien environnement supprimé")
        except Exception as e:
            print(f"⚠️ Erreur lors de la suppression: {str(e)}")

def create_virtual_environment():
    """Crée un environnement virtuel"""
    return run_command("python -m venv venv", "Création de l'environnement virtuel")

def install_dependencies():
    """Installe les dépendances minimales"""
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    print("🔄 Installation des outils de base...")
    
    # Installation de setuptools et wheel en premier
    basic_packages = ["setuptools", "wheel"]
    for package in basic_packages:
        if not run_command(f"{python_cmd} -m pip install --upgrade {package}", f"Installation de {package}"):
            print(f"⚠️ Échec de l'installation de {package}, continuation...")
    
    # Mise à jour de pip
    print("🔄 Mise à jour de pip...")
    try:
        subprocess.run(f"{python_cmd} -m pip install --upgrade pip", shell=True, check=True)
        print("✅ Mise à jour de pip - Succès")
    except subprocess.CalledProcessError:
        print("⚠️ Mise à jour de pip échouée, continuation...")
    
    # Installation des dépendances par petits groupes
    dependency_groups = [
        ["fastapi==0.104.1"],
        ["uvicorn[standard]==0.24.0"],
        ["python-multipart==0.0.6"],
        ["PyPDF2==3.0.1"],
        ["Pillow==10.1.0"],
        ["python-json-logger==2.0.7"],
        ["python-dotenv==1.0.0"],
        ["aiofiles==23.2.1"]
    ]
    
    for group in dependency_groups:
        group_str = " ".join(group)
        if not run_command(f"{pip_cmd} install {' '.join(group)}", f"Installation de {group_str}"):
            print(f"❌ Impossible d'installer {group_str}")
            return False
    
    return True

def create_directories():
    """Crée les dossiers nécessaires"""
    directories = ["uploads", "outputs", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Dossier créé: {directory}")

def test_installation():
    """Teste l'installation"""
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python.exe"
    else:
        python_cmd = "venv/bin/python"
    
    print("🧪 Test de l'installation...")
    
    # Test d'import des modules
    test_imports = [
        "import fastapi",
        "import uvicorn",
        "import PyPDF2",
        "import PIL",
        "import aiofiles"
    ]
    
    for import_cmd in test_imports:
        try:
            # Utilisation du chemin absolu pour Windows
            if platform.system() == "Windows":
                python_path = os.path.abspath(python_cmd)
                result = subprocess.run([python_path, "-c", import_cmd], capture_output=True, text=True)
            else:
                result = subprocess.run([python_cmd, "-c", import_cmd], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {import_cmd} - OK")
            else:
                print(f"❌ {import_cmd} - Échec")
                if result.stderr:
                    print(f"   Erreur: {result.stderr.strip()}")
                return False
        except Exception as e:
            print(f"❌ {import_cmd} - Erreur: {str(e)}")
            return False
    
    return True

def main():
    """Fonction principale d'installation"""
    print("🚀 Installation FINALE de CV Processing API")
    print("=" * 50)
    
    # Vérifications préliminaires
    if not check_python_version():
        sys.exit(1)
    
    # Nettoyage de l'environnement
    clean_environment()
    
    # Création de l'environnement virtuel
    if not create_virtual_environment():
        print("❌ Échec de la création de l'environnement virtuel")
        sys.exit(1)
    
    print("✅ Environnement virtuel créé")
    
    # Installation des dépendances
    if not install_dependencies():
        print("❌ Échec de l'installation des dépendances")
        sys.exit(1)
    
    # Test de l'installation
    if not test_installation():
        print("❌ Échec du test d'installation")
        sys.exit(1)
    
    # Création des dossiers
    create_directories()
    
    print("\n" + "=" * 50)
    print("🎉 Installation terminée avec succès!")
    print("=" * 50)
    print("\n📋 Prochaines étapes:")
    print("1. Activer l'environnement virtuel:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("2. Démarrer l'API:")
    print("   python run-simple.py")
    print("\n3. Ouvrir votre navigateur sur:")
    print("   http://localhost:8000/docs")
    
    print("\n📝 Installation minimale fonctionnelle:")
    print("   - FastAPI + Uvicorn pour l'API REST")
    print("   - PyPDF2 pour l'extraction de texte PDF")
    print("   - Extraction d'informations avec regex intelligents")
    print("   - Gestion complète des fichiers")
    
    print("\n💡 Pour ajouter plus de fonctionnalités plus tard:")
    print("   pip install pdfplumber pytesseract opencv-python")
    print("   pip install spacy transformers torch")
    
    print("\n📖 Consultez le README.md pour plus d'informations")
    print("🆘 En cas de problème, vérifiez les logs et la documentation")

if __name__ == "__main__":
    main()



