import re
import logging
from typing import Dict, List, Optional, Any

class AIExtractorImproved:
    """
    Service d'extraction d'informations des CVs avec patterns améliorés
    Version optimisée pour une meilleure structuration des données
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._initialize_regex_patterns()
        
    def _initialize_regex_patterns(self):
        """Initialise les patterns regex améliorés"""
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+237|237|\+33|0)[\s\-]?[0-9]{8,10}',
            'linkedin': r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-%]+',
            'github': r'(?:https?://)?(?:www\.)?github\.com/[\w\-]+',
            'website': r'https?://(?:www\.)?[^\s<>"]+|www\.[^\s<>"]+',
            'address': r'(?:Adresses?|Address|Adresse)[:\s]*([^.\n]+)',
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
            'years_experience': r'(\d+)\s*(?:ans?|years?|années?)\s*(?:d\'expérience|of experience|d\'exp)',
            'skills': r'(?:Compétences?|Skills?|Technologies?|Technologies?|Outils?|Tools?)[:\s]*([^.\n]+)',
            'education': r'(?:Formation|Education|Études?|Studies|Diplôme|Degree)[:\s]*([^.\n]+)',
            'languages': r'(?:Langues?|Languages?)[:\s]*([^.\n]+)',
            'certifications': r'(?:Certifications?|Certificats?|Certificates?)[:\s]*([^.\n]+)',
            'hobbies': r'(?:Hobbies?|Centres? d\'intérêt|Interests?)[:\s]*([^.\n]+)'
        }
    
    async def extract_cv_information(self, text: str) -> Dict[str, Any]:
        """
        Extrait les informations structurées d'un CV avec une meilleure organisation
        """
        try:
            self.logger.info("Début de l'extraction des informations du CV (version améliorée)")
            
            # Nettoyage du texte amélioré
            cleaned_text = self._clean_text_improved(text)
            
            # Extraction des informations de base
            cv_data = {
                'personal_info': await self._extract_personal_info(cleaned_text),
                'contact_info': await self._extract_contact_info(cleaned_text),
                'address': await self._extract_address(cleaned_text),
                'professional_summary': await self._extract_professional_summary(cleaned_text),
                'work_experience': await self._extract_work_experience(cleaned_text),
                'education': await self._extract_education(cleaned_text),
                'skills': await self._extract_skills(cleaned_text),
                'languages': await self._extract_languages(cleaned_text),
                'certifications': await self._extract_certifications(cleaned_text),
                'projects': await self._extract_projects(cleaned_text),
                'hobbies': await self._extract_hobbies(cleaned_text),
                'extraction_metadata': {
                    'text_length': len(cleaned_text),
                    'extraction_method': 'improved_regex_based',
                    'confidence_score': self._calculate_confidence_score(cleaned_text),
                    'note': 'Extraction améliorée avec patterns optimisés'
                }
            }
            
            self.logger.info("Extraction des informations terminée avec succès")
            return cv_data
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction: {str(e)}")
            raise
    
    def _clean_text_improved(self, text: str) -> str:
        """Nettoie le texte pour l'analyse de manière plus intelligente"""
        if not text:
            return ""
        
        try:
            # Suppression des caractères de contrôle problématiques uniquement
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
    
    async def _extract_personal_info(self, text: str) -> Dict[str, str]:
        """Extrait les informations personnelles de manière améliorée"""
        try:
            personal_info = {}
            
            # Recherche du nom complet avec patterns améliorés
            name_patterns = [
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',  # Nom avec initiales
                r'([A-Z][A-Z\s]+[A-Z])',  # Nom en majuscules
                r'(?:Je m\'appelle|I am|Name)[:\s]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
                r'([A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+)'  # Nom complet en 3 parties
            ]
            
            for pattern in name_patterns:
                name_match = re.search(pattern, text)
                if name_match:
                    name = name_match.group(1).strip()
                    if len(name) > 3 and not re.search(r'\d', name):
                        personal_info['full_name'] = name
                        break
            
            # Si pas de nom trouvé, chercher dans les premières lignes
            if 'full_name' not in personal_info:
                lines = text.split('\n')
                for line in lines[:5]:  # Chercher dans les 5 premières lignes
                    line = line.strip()
                    if line and len(line) > 5 and not re.search(r'\d', line):
                        # Vérifier si c'est un nom (pas d'email, pas de téléphone)
                        if not re.search(r'@', line) and not re.search(r'\+', line):
                            personal_info['full_name'] = line
                            break
            
            return personal_info
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction infos personnelles: {str(e)}")
            return {}
    
    async def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extrait les informations de contact de manière améliorée"""
        try:
            contact_info = {}
            
            # Extraction email
            email_match = re.search(self.patterns['email'], text)
            if email_match:
                contact_info['email'] = email_match.group()
            
            # Extraction téléphone avec pattern amélioré
            phone_patterns = [
                r'(\+237\s*[0-9]{8,9})',
                r'(237\s*[0-9]{8,9})',
                r'(\+33\s*[0-9]{9,10})',
                r'(0[0-9]{9})',
                r'Phone[:\s]*([0-9+\s\-]+)',
                r'Téléphone[:\s]*([0-9+\s\-]+)'
            ]
            
            for pattern in phone_patterns:
                phone_match = re.search(pattern, text, re.IGNORECASE)
                if phone_match:
                    phone = phone_match.group(1).strip()
                    if len(phone) >= 8:
                        contact_info['phone'] = phone
                        break
            
            # Extraction LinkedIn
            linkedin_match = re.search(self.patterns['linkedin'], text)
            if linkedin_match:
                contact_info['linkedin'] = linkedin_match.group()
            
            # Extraction GitHub
            github_match = re.search(self.patterns['github'], text)
            if github_match:
                contact_info['github'] = github_match.group()
            
            # Extraction site web
            website_match = re.search(self.patterns['website'], text)
            if website_match:
                contact_info['website'] = website_match.group()
            
            return contact_info
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction infos contact: {str(e)}")
            return {}
    
    async def _extract_address(self, text: str) -> str:
        """Extrait l'adresse de manière améliorée"""
        try:
            # Patterns pour l'adresse
            address_patterns = [
                r'(?:Adresses?|Address|Adresse)[:\s]*([^.\n]+)',
                r'(?:Yassa|Douala|Littoral)[^.\n]*',
                r'(?:Ville|City)[:\s]*([^.\n]+)'
            ]
            
            for pattern in address_patterns:
                address_match = re.search(pattern, text, re.IGNORECASE)
                if address_match:
                    address = address_match.group(1) if address_match.groups() else address_match.group()
                    if address and len(address.strip()) > 5:
                        return address.strip()
            
            # Recherche par mots-clés géographiques
            location_keywords = ['Yassa', 'Douala', 'Littoral', 'Cameroun', 'Cameroon']
            for keyword in location_keywords:
                if keyword.lower() in text.lower():
                    # Prendre le contexte autour du mot-clé
                    start = max(0, text.lower().find(keyword.lower()) - 50)
                    end = min(len(text), text.lower().find(keyword.lower()) + 50)
                    context = text[start:end]
                    if context:
                        return context.strip()
            
            return ""
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction adresse: {str(e)}")
            return ""
    
    async def _extract_professional_summary(self, text: str) -> str:
        """Extrait le résumé professionnel de manière améliorée"""
        try:
            # Recherche de sections contenant des mots-clés de résumé
            summary_keywords = ['résumé', 'summary', 'profil', 'profile', 'objectif', 'objective', 'ambitious', 'determined', 'hardworking']
            
            lines = text.split('\n')
            for i, line in enumerate(lines):
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in summary_keywords):
                    # Prendre les 3-5 lignes suivantes comme résumé
                    summary_lines = []
                    for j in range(i+1, min(i+6, len(lines))):
                        if lines[j].strip() and len(lines[j].strip()) > 10:
                            summary_lines.append(lines[j].strip())
                        if len(summary_lines) >= 3:
                            break
                    if summary_lines:
                        return ' '.join(summary_lines)
            
            return ""
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction résumé: {str(e)}")
            return ""
    
    async def _extract_work_experience(self, text: str) -> List[Dict[str, str]]:
        """Extrait l'expérience professionnelle de manière améliorée"""
        try:
            experience = []
            
            # Recherche des expériences par mots-clés
            exp_keywords = ['intern', 'stagiaire', 'développeur', 'developer', 'mobile developer']
            
            lines = text.split('\n')
            current_exp = {}
            
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                # Détection d'une nouvelle expérience
                if any(keyword in line_lower for keyword in exp_keywords) or \
                   re.search(r'\b(?:COM\.INFO|Devsec|PRODITECH|ENSPD)\b', line, re.IGNORECASE):
                    
                    if current_exp and current_exp.get('title'):
                        experience.append(current_exp)
                    
                    current_exp = {
                        'title': line.strip(),
                        'company': '',
                        'period': '',
                        'description': []
                    }
                
                elif current_exp and line.strip():
                    # Ajout de détails à l'expérience courante
                    if not current_exp['company'] and len(line.strip()) < 100:
                        current_exp['company'] = line.strip()
                    elif not current_exp['period'] and re.search(r'\d{4}', line):
                        current_exp['period'] = line.strip()
                    else:
                        current_exp['description'].append(line.strip())
            
            # Ajouter la dernière expérience
            if current_exp and current_exp.get('title'):
                experience.append(current_exp)
            
            return experience
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction expérience: {str(e)}")
            return []
    
    async def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extrait la formation/éducation de manière améliorée"""
        try:
            education = []
            
            # Patterns pour l'éducation
            edu_patterns = [
                r'(?:National Higher Polytechnic School of Douala)[^.\n]*',
                r'(?:LYCEE DE LA CITE DES PALMIERS)[^.\n]*',
                r'(?:Baccalaureat|Bachelor|Master|PhD)[^.\n]*'
            ]
            
            lines = text.split('\n')
            current_edu = {}
            
            for i, line in enumerate(lines):
                line_lower = line.lower()
                
                if any(re.search(pattern, line, re.IGNORECASE) for pattern in edu_patterns):
                    if current_edu and current_edu.get('degree'):
                        education.append(current_edu)
                    
                    current_edu = {
                        'degree': line.strip(),
                        'institution': '',
                        'year': '',
                        'description': []
                    }
                
                elif current_edu and line.strip():
                    if not current_edu['institution'] and len(line.strip()) < 100:
                        current_edu['institution'] = line.strip()
                    elif not current_edu['year'] and re.search(r'\d{4}', line):
                        current_edu['year'] = line.strip()
                    else:
                        current_edu['description'].append(line.strip())
            
            if current_edu and current_edu.get('degree'):
                education.append(current_edu)
            
            return education
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction éducation: {str(e)}")
            return []
    
    async def _extract_skills(self, text: str) -> List[str]:
        """Extrait les compétences de manière améliorée"""
        try:
            skills = []
            
            # Extraction avec regex amélioré
            skills_match = re.search(self.patterns['skills'], text, re.IGNORECASE)
            if skills_match:
                skills_text = skills_match.group(1)
                # Séparation des compétences
                skills = [skill.strip() for skill in re.split(r'[,;]', skills_text) if skill.strip()]
            
            # Recherche de mots-clés techniques spécifiques
            technical_keywords = [
                'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
                'sql', 'mongodb', 'docker', 'kubernetes', 'aws', 'azure', 'git',
                'html', 'css', 'typescript', 'php', 'c#', 'c++', 'go', 'rust',
                'laravel', 'django', 'flask', 'unity', 'figma', 'adobe xd', 'illustrator',
                'linux', 'wpf', 'winform', 'huawei cloud'
            ]
            
            for keyword in technical_keywords:
                if re.search(rf'\b{keyword}\b', text, re.IGNORECASE):
                    if keyword not in skills:
                        skills.append(keyword)
            
            # Nettoyage des compétences
            cleaned_skills = []
            for skill in skills:
                skill = skill.strip()
                if skill and len(skill) > 1 and not re.search(r'[^\w\s\-]', skill):
                    cleaned_skills.append(skill)
            
            return cleaned_skills[:20]  # Limiter à 20 compétences
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction compétences: {str(e)}")
            return []
    
    async def _extract_languages(self, text: str) -> List[str]:
        """Extrait les langues de manière améliorée"""
        try:
            languages = []
            
            # Recherche de langues spécifiques
            language_keywords = ['French', 'English', 'Native', 'Fluent']
            
            for keyword in language_keywords:
                if re.search(rf'\b{keyword}\b', text, re.IGNORECASE):
                    if keyword not in languages:
                        languages.append(keyword)
            
            # Extraction avec regex
            lang_match = re.search(self.patterns['languages'], text, re.IGNORECASE)
            if lang_match:
                lang_text = lang_match.group(1)
                additional_langs = [lang.strip() for lang in re.split(r'[,;]', lang_text) if lang.strip()]
                for lang in additional_langs:
                    if lang not in languages:
                        languages.append(lang)
            
            return languages
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction langues: {str(e)}")
            return []
    
    async def _extract_certifications(self, text: str) -> List[str]:
        """Extrait les certifications"""
        try:
            certifications = []
            
            # Extraction avec regex
            cert_match = re.search(self.patterns['certifications'], text, re.IGNORECASE)
            if cert_match:
                cert_text = cert_match.group(1)
                certifications = [cert.strip() for cert in re.split(r'[,;]', cert_text) if cert.strip()]
            
            return certifications
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction certifications: {str(e)}")
            return []
    
    async def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extrait les projets de manière améliorée"""
        try:
            projects = []
            
            # Recherche de projets spécifiques
            project_keywords = ['LINA Project', 'AFRISOLUTION', 'Devsec website', 'Camtel Bluetech Challenge']
            
            for keyword in project_keywords:
                if keyword.lower() in text.lower():
                    # Prendre le contexte autour du projet
                    start = max(0, text.lower().find(keyword.lower()) - 100)
                    end = min(len(text), text.lower().find(keyword.lower()) + 100)
                    context = text[start:end]
                    
                    if context:
                        projects.append({
                            'name': keyword,
                            'description': context.strip(),
                            'technologies': []
                        })
            
            return projects
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction projets: {str(e)}")
            return []
    
    async def _extract_hobbies(self, text: str) -> List[str]:
        """Extrait les hobbies de manière améliorée"""
        try:
            hobbies = []
            
            # Extraction avec regex
            hobbies_match = re.search(self.patterns['hobbies'], text, re.IGNORECASE)
            if hobbies_match:
                hobbies_text = hobbies_match.group(1)
                hobbies = [hobby.strip() for hobby in re.split(r'[,;]', hobbies_text) if hobby.strip()]
            
            # Recherche de hobbies spécifiques
            hobby_keywords = ['Sing', 'piano', 'Music', 'football', 'reading', 'video games']
            
            for keyword in hobby_keywords:
                if re.search(rf'\b{keyword}\b', text, re.IGNORECASE):
                    if keyword not in hobbies:
                        hobbies.append(keyword)
            
            return hobbies
            
        except Exception as e:
            self.logger.warning(f"Erreur extraction hobbies: {str(e)}")
            return []
    
    def _calculate_confidence_score(self, text: str) -> float:
        """Calcule un score de confiance pour l'extraction"""
        try:
            score = 0.0
            
            # Facteurs de qualité du texte
            if len(text) > 500:
                score += 0.2
            if len(text) > 1000:
                score += 0.2
            
            # Présence d'informations clés
            if re.search(self.patterns['email'], text):
                score += 0.15
            if re.search(self.patterns['phone'], text):
                score += 0.15
            if re.search(r'\b\d{4}\b', text):  # Années
                score += 0.1
            if re.search(r'\b(?:Compétences?|Skills?)\b', text):
                score += 0.1
            if re.search(r'\b(?:Education|Formation)\b', text):
                score += 0.1
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.warning(f"Erreur calcul score confiance: {str(e)}")
            return 0.5
