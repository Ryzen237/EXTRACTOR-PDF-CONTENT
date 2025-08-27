import aiofiles
import json
import logging
from pathlib import Path
from typing import Dict, Any
from fastapi import UploadFile

class FileHandler:
    """
    Gestionnaire de fichiers pour l'API CV Processing
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def save_uploaded_file(self, file: UploadFile, file_path: str) -> bool:
        """
        Sauvegarde un fichier uploadé
        
        Args:
            file (UploadFile): Fichier uploadé
            file_path (str): Chemin de destination
            
        Returns:
            bool: True si la sauvegarde a réussi
        """
        try:
            self.logger.info(f"Sauvegarde du fichier: {file_path}")
            
            # Création du dossier parent si nécessaire
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarde du fichier
            async with aiofiles.open(file_path, 'wb') as f:
                # Si le contenu a déjà été lu, on le réutilise
                if hasattr(file, '_content'):
                    content = file._content
                else:
                    content = await file.read()
                await f.write(content)
            
            self.logger.info(f"Fichier sauvegardé avec succès: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du fichier: {str(e)}")
            raise
    
    async def save_json_result(self, data: Dict[str, Any], file_path: str) -> bool:
        """
        Sauvegarde un résultat JSON
        
        Args:
            data (Dict[str, Any]): Données à sauvegarder
            file_path (str): Chemin de destination
            
        Returns:
            bool: True si la sauvegarde a réussi
        """
        try:
            self.logger.info(f"Sauvegarde du résultat JSON: {file_path}")
            
            # Création du dossier parent si nécessaire
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarde en JSON
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                json_content = json.dumps(data, ensure_ascii=False, indent=2)
                await f.write(json_content)
            
            self.logger.info(f"Résultat JSON sauvegardé avec succès: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du JSON: {str(e)}")
            raise
    
    async def read_json_file(self, file_path: str) -> Dict[str, Any]:
        """
        Lit un fichier JSON
        
        Args:
            file_path (str): Chemin du fichier
            
        Returns:
            Dict[str, Any]: Contenu du fichier JSON
        """
        try:
            self.logger.info(f"Lecture du fichier JSON: {file_path}")
            
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                data = json.loads(content)
            
            self.logger.info(f"Fichier JSON lu avec succès: {file_path}")
            return data
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la lecture du JSON: {str(e)}")
            raise
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Récupère les informations d'un fichier
        
        Args:
            file_path (str): Chemin du fichier
            
        Returns:
            Dict[str, Any]: Informations du fichier
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                raise FileNotFoundError(f"Fichier non trouvé: {file_path}")
            
            stat = path.stat()
            
            info = {
                'name': path.name,
                'size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
                'extension': path.suffix,
                'exists': True
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des infos fichier: {str(e)}")
            raise
    
    def list_files(self, directory: str, pattern: str = "*") -> list:
        """
        Liste les fichiers d'un répertoire
        
        Args:
            directory (str): Répertoire à lister
            pattern (str): Pattern de recherche
            
        Returns:
            list: Liste des fichiers
        """
        try:
            self.logger.info(f"Liste des fichiers dans: {directory}")
            
            path = Path(directory)
            if not path.exists():
                return []
            
            files = []
            for file_path in path.glob(pattern):
                if file_path.is_file():
                    files.append({
                        'name': file_path.name,
                        'path': str(file_path),
                        'size': file_path.stat().st_size,
                        'modified': file_path.stat().st_mtime
                    })
            
            self.logger.info(f"Nombre de fichiers trouvés: {len(files)}")
            return files
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la liste des fichiers: {str(e)}")
            raise
    
    def delete_file(self, file_path: str) -> bool:
        """
        Supprime un fichier
        
        Args:
            file_path (str): Chemin du fichier
            
        Returns:
            bool: True si la suppression a réussi
        """
        try:
            self.logger.info(f"Suppression du fichier: {file_path}")
            
            path = Path(file_path)
            if path.exists():
                path.unlink()
                self.logger.info(f"Fichier supprimé avec succès: {file_path}")
                return True
            else:
                self.logger.warning(f"Fichier non trouvé pour suppression: {file_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression du fichier: {str(e)}")
            raise
    
    def ensure_directory(self, directory: str) -> bool:
        """
        S'assure qu'un répertoire existe
        
        Args:
            directory (str): Chemin du répertoire
            
        Returns:
            bool: True si le répertoire existe ou a été créé
        """
        try:
            path = Path(directory)
            path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Répertoire vérifié/créé: {directory}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du répertoire: {str(e)}")
            raise
