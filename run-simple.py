#!/usr/bin/env python3
"""
Script de démarrage simplifié de l'API CV Processing
Version minimale sans vérification des modèles IA avancés
"""

import uvicorn
import os
import sys
from pathlib import Path

# Ajout du répertoire courant au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from utils.logger import setup_logger

def main():
    """Fonction principale de démarrage simplifiée"""
    
    # Configuration du logger
    logger = setup_logger("cv_processing_api")
    
    logger.info("=" * 50)
    logger.info("Démarrage de l'API CV Processing (Version Simplifiée)")
    logger.info("=" * 50)
    
    # Configuration de base
    HOST = "0.0.0.0"
    PORT = 8000
    DEBUG = True
    LOG_LEVEL = "info"
    
    # Affichage de la configuration
    logger.info(f"Version: 1.0.0")
    logger.info(f"Environnement: Développement")
    logger.info(f"Hôte: {HOST}")
    logger.info(f"Port: {PORT}")
    logger.info(f"Mode debug: {DEBUG}")
    
    # Vérification des dossiers
    logger.info("Vérification des dossiers...")
    directories = ["uploads", "outputs", "logs"]
    for directory in directories:
        dir_path = Path(directory)
        if dir_path.exists():
            logger.info(f"✓ Dossier {directory}: OK")
        else:
            logger.info(f"📁 Création du dossier {directory}...")
            dir_path.mkdir(exist_ok=True)
            logger.info(f"✓ Dossier {directory}: Créé")
    
    # Vérification des modules essentiels
    logger.info("Vérification des modules essentiels...")
    try:
        import fastapi
        logger.info("✓ FastAPI: Disponible")
    except ImportError as e:
        logger.error(f"❌ FastAPI: Erreur - {str(e)}")
        sys.exit(1)
    
    try:
        import uvicorn
        logger.info("✓ Uvicorn: Disponible")
    except ImportError as e:
        logger.error(f"❌ Uvicorn: Erreur - {str(e)}")
        sys.exit(1)
    
    try:
        import PyPDF2
        logger.info("✓ PyPDF2: Disponible")
    except ImportError as e:
        logger.error(f"❌ PyPDF2: Erreur - {str(e)}")
        sys.exit(1)
    
    try:
        import PIL
        logger.info("✓ Pillow (PIL): Disponible")
    except ImportError as e:
        logger.error(f"❌ Pillow: Erreur - {str(e)}")
        sys.exit(1)
    
    try:
        import aiofiles
        logger.info("✓ Aiofiles: Disponible")
    except ImportError as e:
        logger.error(f"❌ Aiofiles: Erreur - {str(e)}")
        sys.exit(1)
    
    # Vérification des services
    logger.info("Vérification des services...")
    try:
        from services.cv_processor_simple import CVProcessorSimple
        from services.ai_extractor_improved import AIExtractorImproved
        from utils.file_handler import FileHandler
        
        # Test d'initialisation des services
        cv_processor = CVProcessorSimple()
        ai_extractor = AIExtractorImproved()
        file_handler = FileHandler()
        
        logger.info("✓ Services: Initialisés avec succès")
    except Exception as e:
        logger.error(f"❌ Services: Erreur d'initialisation - {str(e)}")
        sys.exit(1)
    
    # Démarrage du serveur
    logger.info("Démarrage du serveur uvicorn...")
    
    try:
        uvicorn.run(
            "main:app",
            host=HOST,
            port=PORT,
            reload=DEBUG,
            log_level=LOG_LEVEL,
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("Arrêt du serveur demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du serveur: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()



