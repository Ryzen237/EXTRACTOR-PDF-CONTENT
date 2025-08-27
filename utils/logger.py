import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
import os

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Configure le système de logging pour l'application
    
    Args:
        name (str): Nom du logger
        level (str): Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: Logger configuré
    """
    
    # Création du dossier logs s'il n'existe pas
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configuration du logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Éviter les handlers dupliqués
    if logger.handlers:
        return logger
    
    # Format du log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler pour le fichier (rotation quotidienne)
    log_file = logs_dir / f"cv_processing_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler pour les erreurs (fichier séparé)
    error_log_file = logs_dir / f"cv_processing_errors_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Récupère un logger existant ou en crée un nouveau
    
    Args:
        name (str): Nom du logger
        
    Returns:
        logging.Logger: Logger
    """
    return logging.getLogger(name)

def log_function_call(func):
    """
    Décorateur pour logger les appels de fonction
    
    Args:
        func: Fonction à décorer
        
    Returns:
        Fonction décorée
    """
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Appel de {func.__name__} avec args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Fonction {func.__name__} terminée avec succès")
            return result
        except Exception as e:
            logger.error(f"Erreur dans {func.__name__}: {str(e)}")
            raise
    
    return wrapper

def log_async_function_call(func):
    """
    Décorateur pour logger les appels de fonction asynchrone
    
    Args:
        func: Fonction asynchrone à décorer
        
    Returns:
        Fonction asynchrone décorée
    """
    async def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Appel asynchrone de {func.__name__} avec args={args}, kwargs={kwargs}")
        
        try:
            result = await func(*args, **kwargs)
            logger.debug(f"Fonction asynchrone {func.__name__} terminée avec succès")
            return result
        except Exception as e:
            logger.error(f"Erreur dans {func.__name__}: {str(e)}")
            raise
    
    return wrapper



