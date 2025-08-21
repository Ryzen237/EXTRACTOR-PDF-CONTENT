import logging
import sys
from pathlib import Path
from datetime import datetime
import os

def setup_logger(name: str = "cv_processing_api") -> logging.Logger:
    """
    Configure et retourne un logger configuré
    
    Args:
        name (str): Nom du logger
        
    Returns:
        logging.Logger: Logger configuré
    """
    
    # Création du dossier logs s'il n'existe pas
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configuration du logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Éviter la duplication des handlers
    if logger.handlers:
        return logger
    
    # Handler pour la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # Handler pour les fichiers
    log_file = log_dir / f"cv_processing_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Ajout des handlers au logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Configuration des autres loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    return logger

def get_logger(name: str = None) -> logging.Logger:
    """
    Retourne un logger existant ou en crée un nouveau
    
    Args:
        name (str): Nom du logger
        
    Returns:
        logging.Logger: Logger
    """
    if name:
        return logging.getLogger(name)
    else:
        return logging.getLogger("cv_processing_api")

def log_function_call(func):
    """
    Décorateur pour logger les appels de fonctions
    
    Args:
        func: Fonction à décorer
        
    Returns:
        Fonction décorée
    """
    def wrapper(*args, **kwargs):
        logger = get_logger()
        logger.info(f"Appel de la fonction: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Fonction {func.__name__} exécutée avec succès")
            return result
        except Exception as e:
            logger.error(f"Erreur dans la fonction {func.__name__}: {str(e)}")
            raise
    return wrapper

def log_async_function_call(func):
    """
    Décorateur pour logger les appels de fonctions asynchrones
    
    Args:
        func: Fonction asynchrone à décorer
        
    Returns:
        Fonction asynchrone décorée
    """
    async def wrapper(*args, **kwargs):
        logger = get_logger()
        logger.info(f"Appel de la fonction asynchrone: {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"Fonction asynchrone {func.__name__} exécutée avec succès")
            return result
        except Exception as e:
            logger.error(f"Erreur dans la fonction asynchrone {func.__name__}: {str(e)}")
            raise
    return wrapper

class LoggerMixin:
    """
    Mixin pour ajouter facilement des capacités de logging aux classes
    """
    
    @property
    def logger(self):
        """Retourne le logger de la classe"""
        return logging.getLogger(self.__class__.__name__)
    
    def log_info(self, message: str):
        """Log un message d'information"""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log un message d'avertissement"""
        self.logger.warning(message)
    
    def log_error(self, message: str):
        """Log un message d'erreur"""
        self.logger.error(message)
    
    def log_debug(self, message: str):
        """Log un message de debug"""
        self.logger.debug(message)
    
    def log_exception(self, message: str, exc_info=True):
        """Log une exception avec traceback"""
        self.logger.exception(message, exc_info=exc_info)

