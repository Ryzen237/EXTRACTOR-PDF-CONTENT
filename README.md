# CV Processing API

Une API FastAPI robuste pour l'extraction et le traitement automatique d'informations depuis des CVs PDF.

## 🚀 Fonctionnalités

- **Upload de CVs PDF** via interface REST
- **Extraction de texte** avec PyPDF2
- **Extraction d'informations structurées** :
  - Informations personnelles (nom, etc.)
  - Coordonnées (email, téléphone, LinkedIn, GitHub)
  - Adresse
  - Résumé professionnel
  - Expérience professionnelle
  - Formation/Éducation
  - Compétences techniques
  - Langues
  - Certifications
  - Projets
  - Hobbies
- **Sauvegarde des résultats** en JSON
- **API RESTful complète** avec documentation interactive
- **Gestion d'erreurs robuste**
- **Logging détaillé**

## 📋 Prérequis

- Python 3.8+
- pip
- Un fichier PDF de CV pour tester

## 🛠️ Installation

### Installation automatique (Recommandée)

```bash
# 1. Cloner ou télécharger le projet
# 2. Exécuter le script d'installation
python install-final.py
```

### Installation manuelle

```bash
# 1. Créer un environnement virtuel
python -m venv venv

# 2. Activer l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements-minimal-working.txt
```

## 🚀 Démarrage

### Démarrage automatique

```bash
# Activer l'environnement virtuel
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Démarrer l'API
python run-simple.py
```

### Démarrage manuel

```bash
# Activer l'environnement virtuel
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Démarrer avec uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📖 Utilisation

### 1. Accès à l'API

- **Interface Swagger** : http://localhost:8000/docs
- **Page d'accueil** : http://localhost:8000/
- **Test de santé** : http://localhost:8000/health

### 2. Upload et traitement d'un CV

#### Via l'interface Swagger :
1. Ouvrir http://localhost:8000/docs
2. Cliquer sur `/upload-cv`
3. Cliquer sur "Try it out"
4. Sélectionner un fichier PDF
5. Cliquer sur "Execute"

#### Via curl :
```bash
# Upload du CV
curl -X POST "http://localhost:8000/upload-cv" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@votre_cv.pdf"

# Traitement du CV uploadé
curl -X POST "http://localhost:8000/process-cv" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "file_path=uploads/cv_20250101_120000_votre_cv.pdf"
```

### 3. Test de l'extraction

```bash
# Tester l'extraction avec un CV existant
python test-improved-extraction.py
```

## 📁 Structure du projet

```
cv-processing-api/
├── main.py                      # Application FastAPI principale
├── run-simple.py                # Script de démarrage simplifié
├── install-final.py             # Script d'installation automatique
├── test-improved-extraction.py  # Script de test de l'extraction
├── requirements-minimal-working.txt  # Dépendances Python
├── README.md                    # Documentation
├── .gitignore                   # Fichiers ignorés par Git
├── services/                    # Services métier
│   ├── __init__.py
│   ├── cv_processor_simple.py   # Traitement des PDFs
│   └── ai_extractor_improved.py # Extraction d'informations
├── utils/                       # Utilitaires
│   ├── __init__.py
│   ├── file_handler.py          # Gestion des fichiers
│   └── logger.py                # Configuration du logging
├── uploads/                     # CVs uploadés
├── outputs/                     # Résultats JSON
└── logs/                        # Fichiers de logs
```

## 🔧 Endpoints API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Page d'accueil avec liste des endpoints |
| `/health` | GET | Vérification de l'état de l'API |
| `/upload-cv` | POST | Upload d'un fichier CV PDF |
| `/process-cv` | POST | Traitement d'un CV uploadé |
| `/process-cv-from-path` | POST | Traitement d'un CV depuis un chemin |
| `/download-result/{filename}` | GET | Téléchargement d'un résultat |
| `/list-results` | GET | Liste des résultats disponibles |
| `/docs` | GET | Documentation interactive Swagger |

## 🧪 Test de l'extraction

Pour tester l'extraction d'informations :

1. **Placer un CV PDF** dans le dossier `uploads/`
2. **Exécuter le test** :
   ```bash
   python test-improved-extraction.py
   ```
3. **Vérifier les résultats** dans le dossier `outputs/`

## 🔍 Exemple de sortie JSON

```json
{
  "personal_info": {
    "full_name": "Jean Claude Itiel BOUMBISAI"
  },
  "contact_info": {
    "email": "boumbisaiitiel@gmail.com",
    "phone": "+237 650 973 231",
    "linkedin": "https://www.linkedin.com/in/jean-claude-itiel-boumbisaï",
    "github": "https://github.com/Ryzen237"
  },
  "address": "Yassa, Douala, Littoral",
  "professional_summary": "Étudiant en 4ème année à l'ENSPD...",
  "work_experience": [
    {
      "title": "Intern COM.INFO",
      "company": "Douala",
      "period": "August - September 2022",
      "description": ["Manage tickets and analyze faults", "..."]
    }
  ],
  "education": [
    {
      "degree": "Software Engineering",
      "institution": "National Higher Polytechnic School of Douala",
      "year": "2021-2026",
      "description": ["Computer Science and Telecommunications"]
    }
  ],
  "skills": ["Python", "Java", "JavaScript", "React", "Laravel", "Django"],
  "languages": ["French", "English"],
  "projects": [
    {
      "name": "LINA Project",
      "description": "Solution for Camtel Bluetech Challenge...",
      "technologies": []
    }
  ],
  "hobbies": ["Sing", "piano", "Music", "football", "reading"],
  "extraction_metadata": {
    "text_length": 1875,
    "extraction_method": "improved_regex_based",
    "confidence_score": 0.85,
    "note": "Extraction améliorée avec patterns optimisés"
  }
}
```

## 🐛 Résolution de problèmes

### Problème : "No module named 'PyPDF2'"
**Solution** : Activer l'environnement virtuel
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

### Problème : "Port 8000 already in use"
**Solution** : Changer le port ou arrêter le processus
```bash
# Changer le port dans run-simple.py
PORT = 8001
```

### Problème : "Fichier PDF non trouvé"
**Solution** : Vérifier que le fichier existe dans `uploads/`

### Problème : "Aucun texte extrait"
**Solution** : Le PDF peut être protégé ou en image. Utiliser un PDF avec du texte sélectionnable.

## 🔧 Configuration avancée

### Variables d'environnement

Créer un fichier `.env` :
```env
HOST=0.0.0.0
PORT=8000
DEBUG=true
LOG_LEVEL=info
MAX_FILE_SIZE=10485760  # 10MB
```

### Logs

Les logs sont disponibles dans :
- `logs/cv_processing_YYYYMMDD.log` - Logs généraux
- `logs/cv_processing_errors_YYYYMMDD.log` - Logs d'erreurs

## 🚀 Déploiement

### Production avec Gunicorn

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (optionnel)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements-minimal-working.txt .
RUN pip install -r requirements-minimal-working.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Améliorations récentes

### Version 1.1.0 (Corrections majeures)
- ✅ **Extraction d'informations améliorée** : Patterns regex optimisés
- ✅ **Nettoyage de texte intelligent** : Préservation des informations importantes
- ✅ **Gestion d'erreurs robuste** : Validation des fichiers et gestion des exceptions
- ✅ **Patterns téléphone améliorés** : Support des formats internationaux
- ✅ **Test amélioré** : Affichage détaillé des résultats
- ✅ **Validation des fichiers** : Vérification de la taille et du type

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

En cas de problème :
1. Vérifier les logs dans `logs/`
2. Tester avec `python test-improved-extraction.py`
3. Vérifier que l'environnement virtuel est activé
4. Consulter la documentation Swagger sur http://localhost:8000/docs

---

**Développé avec ❤️ pour l'extraction automatique d'informations de CVs**

