# CV Processing API

Une API FastAPI robuste pour traiter et extraire les informations des CVs PDF en utilisant des modèles d'IA open source.

## 🚀 Fonctionnalités

- **Upload de CVs PDF** : Interface simple pour uploader des fichiers
- **Extraction intelligente** : Utilisation de multiples modèles d'IA pour l'extraction
- **Traitement OCR** : Support des PDFs scannés avec Tesseract
- **Extraction structurée** : Informations organisées en JSON structuré
- **API RESTful** : Endpoints clairs et documentés
- **Logging avancé** : Traçabilité complète des opérations
- **Gestion des fichiers** : Sauvegarde et organisation automatique

## 🏗️ Architecture

```
cv-processing-api/
├── main.py                           # Point d'entrée FastAPI
├── run-simple.py                     # Script de démarrage simplifié
├── install-final.py                  # Script d'installation automatique
├── requirements-minimal-working.txt  # Dépendances Python minimales
├── test-improved-extraction.py       # Test de l'extracteur amélioré
├── services/                         # Services métier
│   ├── ai_extractor_improved.py     # Extracteur d'informations amélioré
│   └── cv_processor_simple.py       # Traitement des PDFs simplifié
├── utils/                            # Utilitaires
│   ├── file_handler.py              # Gestion des fichiers
│   └── logger.py                    # Configuration du logging
├── uploads/                          # CVs uploadés (créé automatiquement)
├── outputs/                          # Fichiers JSON générés (créé automatiquement)
└── logs/                             # Fichiers de logs (créé automatiquement)
```

## 🛠️ Installation

### Prérequis

- Python 3.8+
- Tesseract OCR (pour l'extraction de texte des PDFs scannés)

### Installation de Tesseract

#### Windows
```bash
# Télécharger et installer depuis : https://github.com/UB-Mannheim/tesseract/wiki
# Ajouter Tesseract au PATH système
```

#### macOS
```bash
brew install tesseract
brew install tesseract-lang  # Pour les langues supplémentaires
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-fra tesseract-ocr-eng  # Langues FR/EN
```

### Installation Python

1. **Cloner le projet**
```bash
git clone <repository-url>
cd cv-processing-api
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
# Installation automatique (recommandée)
python install-final.py

# Ou installation manuelle
pip install -r requirements-minimal-working.txt
```

## 🚀 Démarrage

### Démarrage simple (recommandé)
```bash
python run-simple.py
```

### Démarrage avec uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Variables d'environnement (optionnel)
```bash
export DEBUG=True
export PORT=8000
export LOG_LEVEL=DEBUG
export SECRET_KEY="your-secret-key"
```

## 📚 API Endpoints

### Endpoints principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/` | Page d'accueil de l'API |
| `GET` | `/health` | Vérification de l'état de l'API |
| `POST` | `/upload-cv` | Upload d'un fichier CV PDF |
| `POST` | `/process-cv` | Traitement d'un CV uploadé |
| `POST` | `/process-cv-from-path` | Traitement d'un CV depuis un chemin |
| `GET` | `/download-result/{filename}` | Téléchargement d'un résultat |
| `GET` | `/list-results` | Liste des résultats disponibles |

### Documentation interactive

Une fois l'API démarrée, accédez à :
- **Swagger UI** : `http://localhost:8000/docs`
- **ReDoc** : `http://localhost:8000/redoc`

## 🔧 Utilisation

### 1. Upload et traitement d'un CV

```bash
# Upload du fichier
curl -X POST "http://localhost:8000/upload-cv" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@mon_cv.pdf"

# Traitement du CV
curl -X POST "http://localhost:8000/process-cv" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "file_path=uploads/cv_20231201_12345678_abc12345.pdf"
```

### 2. Traitement depuis un chemin

```bash
curl -X POST "http://localhost:8000/process-cv-from-path" \
  -H "accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pdf_path=/chemin/vers/mon_cv.pdf"
```

### 3. Récupération des résultats

```bash
# Liste des résultats
curl -X GET "http://localhost:8000/list-results"

# Téléchargement d'un résultat
curl -X GET "http://localhost:8000/download-result/cv_extracted_20231201_123456.json"
```

## 🤖 Modèles d'IA utilisés

### Extraction de texte
- **pdfplumber** : Extraction de texte des PDFs natifs
- **PyPDF2** : Extraction de texte (fallback)
- **Tesseract OCR** : Extraction de texte des PDFs scannés

### Traitement du langage naturel
- **spaCy** : Analyse linguistique et extraction d'entités
- **NLTK** : Traitement de texte avancé
- **Transformers** : Modèles BERT multilingues

### Patterns d'extraction
- **Regex avancés** : Extraction d'emails, téléphones, liens
- **Mots-clés techniques** : Détection automatique des compétences
- **Analyse structurelle** : Identification des sections de CV

## 📊 Format de sortie JSON

```json
{
  "personal_info": {
    "name": "Jean Dupont",
    "current_company": "TechCorp"
  },
  "contact_info": {
    "email": "jean.dupont@email.com",
    "phone": "0123456789",
    "linkedin": "linkedin.com/in/jeandupont"
  },
  "professional_summary": "Développeur full-stack avec 5 ans d'expérience...",
  "work_experience": [
    {
      "title": "Développeur Senior",
      "company": "TechCorp",
      "period": "2020-2023",
      "description": ["Gestion d'équipe de 5 développeurs..."]
    }
  ],
  "education": [
    {
      "degree": "Master en Informatique",
      "institution": "Université de Paris",
      "year": "2018"
    }
  ],
  "skills": ["Python", "React", "Docker", "AWS"],
  "languages": ["Français", "Anglais"],
  "certifications": ["AWS Certified Developer"],
  "projects": [
    {
      "name": "E-commerce Platform",
      "description": ["Développement d'une plateforme complète..."]
    }
  ],
  "extraction_metadata": {
    "text_length": 2500,
    "extraction_method": "ai_enhanced",
    "confidence_score": 0.85
  }
}
```

## 🔍 Configuration

### Modifier la configuration

Éditez `config.py` pour personnaliser :
- Ports et hôtes
- Dossiers d'upload/sortie
- Modèles IA utilisés
- Patterns d'extraction
- Seuils de confiance

### Variables d'environnement

```bash
# Configuration du serveur
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Configuration des modèles
LOG_LEVEL=INFO
SECRET_KEY=your-secret-key

# Configuration CORS
CORS_ORIGINS=http://localhost:3000,https://monapp.com
```

## 🧪 Tests

### Test manuel avec curl

```bash
# Test de santé
curl http://localhost:8000/health

# Test d'upload (remplacez par un vrai fichier PDF)
curl -X POST "http://localhost:8000/upload-cv" \
  -F "file=@test_cv.pdf"
```

### Test avec un client HTTP

Utilisez **Postman**, **Insomnia** ou **Thunder Client** pour tester l'API.

## 🚨 Dépannage

### Erreurs communes

1. **Port déjà utilisé**
   ```bash
   # Changer le port dans config.py ou utiliser un autre port
   uvicorn main:app --port 8001
   ```

2. **Tesseract non trouvé**
   ```bash
   # Vérifier l'installation et le PATH
   tesseract --version
   ```

3. **Modèles spaCy manquants**
   ```bash
   python -m spacy download fr_core_news_sm
   python -m spacy download en_core_web_sm
   ```

4. **Permissions de dossiers**
   ```bash
   # Vérifier les permissions sur uploads/, outputs/, logs/
   chmod 755 uploads/ outputs/ logs/
   ```

### Logs

Les logs sont disponibles dans :
- **Console** : Sortie directe
- **Fichiers** : `logs/cv_processing_YYYYMMDD.log`

## 🔒 Sécurité

### En production

1. **Changer la clé secrète**
   ```bash
   export SECRET_KEY="votre-clé-secrète-très-longue-et-complexe"
   ```

2. **Restreindre CORS**
   ```bash
   export CORS_ORIGINS="https://votre-domaine.com"
   ```

3. **Limiter la taille des fichiers**
   - Modifier `MAX_FILE_SIZE` dans `config.py`

4. **Authentification** (à implémenter selon vos besoins)

## 📈 Performance

### Optimisations recommandées

1. **Cache des modèles IA** : Les modèles sont chargés une seule fois au démarrage
2. **Traitement asynchrone** : Utilisation d'async/await pour les opérations I/O
3. **Nettoyage automatique** : Suppression des anciens fichiers
4. **Logs rotatifs** : Gestion automatique de la taille des logs

### Monitoring

- **Métriques** : Temps de traitement, taux de succès
- **Logs structurés** : Traçabilité complète des opérations
- **Gestion d'erreurs** : Capture et logging de toutes les exceptions

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
1. Vérifiez les logs de l'application
2. Consultez la documentation de l'API (`/docs`)
3. Ouvrez une issue sur GitHub
4. Contactez l'équipe de développement

---

**Développé avec ❤️ pour simplifier le traitement des CVs**

