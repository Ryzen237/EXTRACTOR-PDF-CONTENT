import os
import aiofiles
import shutil
from pathlib import Path
from typing import Optional
import logging
from datetime import datetime
import uuid

class FileHandler:
    """
    Service de gestion des fichiers uploadés et des opérations de fichiers
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def save_uploaded_file(self, file, upload_dir: str) -> Path:
        """
        Sauvegarde un fichier uploadé dans le dossier spécifié
        
        Args:
            file: Fichier uploadé (UploadFile)
            upload_dir (str): Dossier de destination
            
        Returns:
            Path: Chemin du fichier sauvegardé
        """
        try:
            # Création du dossier s'il n'existe pas
            os.makedirs(upload_dir, exist_ok=True)
            
            # Génération d'un nom de fichier unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            file_extension = Path(file.filename).suffix if file.filename else '.pdf'
            
            # Nouveau nom de fichier
            new_filename = f"cv_{timestamp}_{unique_id}{file_extension}"
            file_path = Path(upload_dir) / new_filename
            
            # Sauvegarde du fichier
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            self.logger.info(f"Fichier sauvegardé: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du fichier: {str(e)}")
            raise
    
    async def delete_file(self, file_path: str) -> bool:
        """
        Supprime un fichier
        
        Args:
            file_path (str): Chemin du fichier à supprimer
            
        Returns:
            bool: True si supprimé avec succès, False sinon
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.logger.info(f"Fichier supprimé: {file_path}")
                return True
            else:
                self.logger.warning(f"Fichier non trouvé: {file_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression: {str(e)}")
            return False
    
    async def move_file(self, source_path: str, destination_path: str) -> bool:
        """
        Déplace un fichier d'un emplacement à un autre
        
        Args:
            source_path (str): Chemin source
            destination_path (str): Chemin de destination
            
        Returns:
            bool: True si déplacé avec succès, False sinon
        """
        try:
            # Création du dossier de destination s'il n'existe pas
            dest_dir = Path(destination_path).parent
            os.makedirs(dest_dir, exist_ok=True)
            
            # Déplacement du fichier
            shutil.move(source_path, destination_path)
            self.logger.info(f"Fichier déplacé: {source_path} -> {destination_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors du déplacement: {str(e)}")
            return False
    
    async def copy_file(self, source_path: str, destination_path: str) -> bool:
        """
        Copie un fichier
        
        Args:
            source_path (str): Chemin source
            destination_path (str): Chemin de destination
            
        Returns:
            bool: True si copié avec succès, False sinon
        """
        try:
            # Création du dossier de destination s'il n'existe pas
            dest_dir = Path(destination_path).parent
            os.makedirs(dest_dir, exist_ok=True)
            
            # Copie du fichier
            shutil.copy2(source_path, destination_path)
            self.logger.info(f"Fichier copié: {source_path} -> {destination_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la copie: {str(e)}")
            return False
    
    def get_file_info(self, file_path: str) -> Optional[dict]:
        """
        Récupère les informations d'un fichier
        
        Args:
            file_path (str): Chemin du fichier
            
        Returns:
            Optional[dict]: Informations du fichier ou None si erreur
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            file_info = {
                'path': file_path,
                'name': Path(file_path).name,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'extension': Path(file_path).suffix,
                'is_file': os.path.isfile(file_path),
                'is_directory': os.path.isdir(file_path)
            }
            
            return file_info
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des infos: {str(e)}")
            return None
    
    def list_directory(self, directory_path: str, file_extensions: Optional[list] = None) -> list:
        """
        Liste les fichiers d'un répertoire
        
        Args:
            directory_path (str): Chemin du répertoire
            file_extensions (Optional[list]): Extensions de fichiers à filtrer
            
        Returns:
            list: Liste des fichiers
        """
        try:
            if not os.path.exists(directory_path):
                return []
            
            files = []
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                
                if os.path.isfile(item_path):
                    # Filtrage par extension si spécifié
                    if file_extensions:
                        if Path(item).suffix.lower() in file_extensions:
                            files.append(self.get_file_info(item_path))
                    else:
                        files.append(self.get_file_info(item_path))
            
            return files
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la liste du répertoire: {str(e)}")
            return []
    
    def create_directory(self, directory_path: str) -> bool:
        """
        Crée un répertoire
        
        Args:
            directory_path (str): Chemin du répertoire à créer
            
        Returns:
            bool: True si créé avec succès, False sinon
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            self.logger.info(f"Répertoire créé: {directory_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création du répertoire: {str(e)}")
            return False
    
    def cleanup_old_files(self, directory_path: str, max_age_hours: int = 24) -> int:
        """
        Nettoie les anciens fichiers d'un répertoire
        
        Args:
            directory_path (str): Chemin du répertoire
            max_age_hours (int): Âge maximum en heures
            
        Returns:
            int: Nombre de fichiers supprimés
        """
        try:
            if not os.path.exists(directory_path):
                return 0
            
            current_time = datetime.now()
            deleted_count = 0
            
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                
                if os.path.isfile(item_path):
                    file_time = datetime.fromtimestamp(os.path.getctime(item_path))
                    age_hours = (current_time - file_time).total_seconds() / 3600
                    
                    if age_hours > max_age_hours:
                        if self.delete_file(item_path):
                            deleted_count += 1
            
            self.logger.info(f"{deleted_count} fichiers anciens supprimés de {directory_path}")
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Erreur lors du nettoyage: {str(e)}")
            return 0

