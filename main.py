#!/usr/bin/env python3
"""
API FastAPI pour le traitement des CVs PDF
Point d'entrée principal de l'application
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import logging
from pathlib import Path
from datetime import datetime
import json

# Import des services
from services.cv_processor_simple import CVProcessorSimple
from services.ai_extractor_improved import AIExtractorImproved
from utils.file_handler import FileHandler
from utils.logger import setup_logger

# Configuration du logger
logger = setup_logger("cv_processing_api")

# Création de l'application FastAPI
app = FastAPI(
    title="CV Processing API",
    description="API pour l'extraction et le traitement des informations de CVs PDF",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez vos domaines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration des dossiers
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")

# Création des dossiers s'ils n'existent pas
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialisation des services
cv_processor = CVProcessorSimple()
ai_extractor = AIExtractorImproved()
file_handler = FileHandler()

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "CV Processing API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "upload": "/upload-cv",
            "process": "/process-cv",
            "process_from_path": "/process-cv-from-path",
            "download": "/download-result/{filename}",
            "list_results": "/list-results",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "cv_processor": "available",
            "ai_extractor": "available",
            "file_handler": "available"
        }
    }

@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    """
    Upload d'un fichier CV PDF
    """
    try:
        logger.info(f"Upload de fichier: {file.filename}")
        
        # Vérification du type de fichier
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés")
        
        # Vérification de la taille du fichier (max 10MB)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="Le fichier est trop volumineux (max 10MB)")
        
        # Génération d'un nom de fichier unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"cv_{timestamp}_{file.filename}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Sauvegarde du fichier
        await file_handler.save_uploaded_file(file, str(file_path))
        
        logger.info(f"Fichier sauvegardé: {file_path}")
        
        return {
            "message": "Fichier uploadé avec succès",
            "filename": unique_filename,
            "file_path": str(file_path),
            "size": file_path.stat().st_size if file_path.exists() else 0
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'upload: {str(e)}")

@app.post("/process-cv")
async def process_cv(file_path: str = Form(...)):
    """
    Traitement d'un CV uploadé
    """
    try:
        logger.info(f"Traitement du CV: {file_path}")
        
        # Vérification de l'existence du fichier
        if not Path(file_path).exists():
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
        
        # Vérification que c'est bien un fichier PDF
        if not file_path.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Le fichier doit être un PDF")
        
        # Extraction du texte
        extracted_text = await cv_processor.extract_text_from_pdf(file_path)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Impossible d'extraire le texte du PDF")
        
        # Extraction des informations
        cv_info = await ai_extractor.extract_cv_information(extracted_text)
        
        # Génération du nom de fichier de sortie
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"cv_extracted_{timestamp}.json"
        output_path = OUTPUT_DIR / output_filename
        
        # Sauvegarde du résultat
        await file_handler.save_json_result(cv_info, str(output_path))
        
        logger.info(f"Traitement terminé: {output_path}")
        
        return {
            "message": "CV traité avec succès",
            "input_file": file_path,
            "output_file": output_filename,
            "extracted_info": {
                "personal_info": cv_info.get('personal_info', {}),
                "contact_info": cv_info.get('contact_info', {}),
                "skills_count": len(cv_info.get('skills', [])),
                "experience_count": len(cv_info.get('work_experience', [])),
                "education_count": len(cv_info.get('education', []))
            },
            "metadata": cv_info.get('extraction_metadata', {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@app.post("/process-cv-from-path")
async def process_cv_from_path(pdf_path: str = Form(...)):
    """
    Traitement d'un CV depuis un chemin de fichier
    """
    try:
        logger.info(f"Traitement du CV depuis le chemin: {pdf_path}")
        
        # Vérification de l'existence du fichier
        if not Path(pdf_path).exists():
            raise HTTPException(status_code=404, detail="Fichier non trouvé")
        
        # Extraction du texte
        extracted_text = await cv_processor.extract_text_from_pdf(pdf_path)
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Impossible d'extraire le texte du PDF")
        
        # Extraction des informations
        cv_info = await ai_extractor.extract_cv_information(extracted_text)
        
        # Génération du nom de fichier de sortie
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"cv_extracted_{timestamp}.json"
        output_path = OUTPUT_DIR / output_filename
        
        # Sauvegarde du résultat
        await file_handler.save_json_result(cv_info, str(output_path))
        
        logger.info(f"Traitement terminé: {output_path}")
        
        return {
            "message": "CV traité avec succès",
            "input_file": pdf_path,
            "output_file": output_filename,
            "extracted_info": {
                "personal_info": cv_info.get('personal_info', {}),
                "contact_info": cv_info.get('contact_info', {}),
                "skills_count": len(cv_info.get('skills', [])),
                "experience_count": len(cv_info.get('work_experience', [])),
                "education_count": len(cv_info.get('education', []))
            },
            "metadata": cv_info.get('extraction_metadata', {})
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@app.get("/download-result/{filename}")
async def download_result(filename: str):
    """
    Téléchargement d'un fichier de résultat
    """
    try:
        file_path = OUTPUT_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Fichier de résultat non trouvé")
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type='application/json'
        )
        
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors du téléchargement: {str(e)}")

@app.get("/list-results")
async def list_results():
    """
    Liste des fichiers de résultats disponibles
    """
    try:
        results = []
        
        for file_path in OUTPUT_DIR.glob("*.json"):
            results.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "created": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })
        
        # Tri par date de modification (plus récent en premier)
        results.sort(key=lambda x: x["modified"], reverse=True)
        
        return {
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la liste des résultats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la liste des résultats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
