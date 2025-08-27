import logging
import PyPDF2
from typing import Optional
from pathlib import Path
import re

class CVProcessorSimple:
    """
    Service de traitement des CVs PDF utilisant uniquement PyPDF2
    Version simplifiée sans dépendances lourdes
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extrait le texte d'un fichier PDF en utilisant PyPDF2
        
        Args:
            pdf_path (str): Chemin vers le fichier PDF
            
        Returns:
            str: Texte extrait du PDF
        """
        try:
            self.logger.info(f"Début de l'extraction de texte depuis: {pdf_path}")
            
            # Vérification de l'existence du fichier
            if not Path(pdf_path).exists():
                raise FileNotFoundError(f"Fichier PDF non trouvé: {pdf_path}")
            
            # Extraction avec PyPDF2
            extracted_text = self._extract_with_pypdf2(pdf_path)
            
            if not extracted_text or extracted_text.strip() == "":
                self.logger.warning("Aucun texte extrait avec PyPDF2")
                return ""
            
            # Nettoyage du texte extrait
            cleaned_text = self._clean_extracted_text(extracted_text)
            
            self.logger.info(f"Extraction terminée. Longueur du texte: {len(cleaned_text)} caractères")
            return cleaned_text
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction du texte: {str(e)}")
            raise
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Extrait le texte avec PyPDF2"""
        try:
            text_content = []
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Vérification du nombre de pages
                num_pages = len(pdf_reader.pages)
                self.logger.info(f"Nombre de pages détectées: {num_pages}")
                
                # Extraction du texte de chaque page
                for page_num in range(num_pages):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        
                        if page_text:
                            text_content.append(page_text)
                            self.logger.debug(f"Page {page_num + 1}: {len(page_text)} caractères extraits")
                        else:
                            self.logger.warning(f"Page {page_num + 1}: Aucun texte extrait")
                            
                    except Exception as e:
                        self.logger.warning(f"Erreur lors de l'extraction de la page {page_num + 1}: {str(e)}")
                        continue
            
            return '\n'.join(text_content)
            
        except Exception as e:
            self.logger.error(f"Erreur PyPDF2: {str(e)}")
            raise
    
    def _clean_extracted_text(self, text: str) -> str:
        """
        Nettoie le texte extrait pour améliorer la qualité
        
        Args:
            text (str): Texte brut extrait
            
        Returns:
            str: Texte nettoyé
        """
        if not text:
            return ""
        
        try:
            # Suppression des caractères de contrôle (sauf retours à la ligne et tabulations)
            text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
            
            # Normalisation des espaces multiples (mais pas trop agressive)
            text = re.sub(r' {2,}', ' ', text)
            
            # Normalisation des retours à la ligne multiples
            text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
            
            # Suppression des espaces en début et fin de ligne
            lines = text.split('\n')
            cleaned_lines = []
            for line in lines:
                line = line.strip()
                if line:  # Garder les lignes non vides
                    cleaned_lines.append(line)
            
            # Reconstitution du texte
            cleaned_text = '\n'.join(cleaned_lines)
            
            return cleaned_text.strip()
            
        except Exception as e:
            self.logger.warning(f"Erreur lors du nettoyage du texte: {str(e)}")
            return text.strip()
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        Récupère les informations de base d'un PDF
        
        Args:
            pdf_path (str): Chemin vers le fichier PDF
            
        Returns:
            dict: Informations du PDF
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                info = {
                    'num_pages': len(pdf_reader.pages),
                    'file_size': Path(pdf_path).stat().st_size,
                    'file_path': pdf_path,
                    'extraction_method': 'PyPDF2'
                }
                
                # Tentative d'extraction des métadonnées
                try:
                    if pdf_reader.metadata:
                        info['metadata'] = {
                            'title': pdf_reader.metadata.get('/Title', ''),
                            'author': pdf_reader.metadata.get('/Author', ''),
                            'subject': pdf_reader.metadata.get('/Subject', ''),
                            'creator': pdf_reader.metadata.get('/Creator', ''),
                            'producer': pdf_reader.metadata.get('/Producer', ''),
                            'creation_date': pdf_reader.metadata.get('/CreationDate', ''),
                            'modification_date': pdf_reader.metadata.get('/ModDate', '')
                        }
                except Exception as e:
                    self.logger.warning(f"Impossible d'extraire les métadonnées: {str(e)}")
                    info['metadata'] = {}
                
                return info
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des infos PDF: {str(e)}")
            raise
    
    def is_pdf_readable(self, pdf_path: str) -> bool:
        """
        Vérifie si un PDF est lisible avec PyPDF2
        
        Args:
            pdf_path (str): Chemin vers le fichier PDF
            
        Returns:
            bool: True si le PDF est lisible
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                # Test d'extraction de la première page
                if num_pages > 0:
                    first_page = pdf_reader.pages[0]
                    test_text = first_page.extract_text()
                    return len(test_text) > 0
                
                return False
                
        except Exception as e:
            self.logger.warning(f"PDF non lisible: {str(e)}")
            return False
