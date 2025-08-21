from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
from datetime import datetime
from pathlib import Path

from services.cv_processor_simple import CVProcessorSimple
from services.ai_extractor_improved import AIExtractorImproved
from utils.file_handler import FileHandler
from utils.logger import setup_logger

# Configuration
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
ALLOWED_EXTENSIONS = {".pdf"}

# Création des dossiers nécessaires
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuration du logger
logger = setup_logger()

app = FastAPI(
    title="CV Processing API",
    description="API pour traiter et extraire les informations des CVs PDF",
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

# Initialisation des services
cv_processor = CVProcessorSimple()
ai_extractor = AIExtractorImproved()
file_handler = FileHandler()

@app.get("/")
async def root():
    """Endpoint racine de l'API"""
    return {"message": "CV Processing API - Prêt à traiter vos CVs!"}

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "cv_processor": "ready",
            "ai_extractor": "ready",
            "file_handler": "ready"
        }
    }

@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    """
    Upload d'un fichier CV PDF
    """
    try:
        # Vérification du type de fichier
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="Seuls les fichiers PDF sont acceptés"
            )
        
        # Sauvegarde du fichier
        file_path = await file_handler.save_uploaded_file(file, UPLOAD_DIR)
        logger.info(f"Fichier PDF uploadé: {file_path}")
        
        return {
            "message": "Fichier uploadé avec succès",
            "filename": file.filename,
            "file_path": str(file_path),
            "status": "ready_for_processing"
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de l'upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-cv")
async def process_cv(
    file_path: str = Form(...),
    output_format: str = Form(default="json")
):
    """
    Traitement d'un CV PDF avec extraction des informations
    """
    try:
        # Vérification de l'existence du fichier
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, 
                detail="Fichier non trouvé"
            )
        
        logger.info(f"Début du traitement du CV: {file_path}")
        
        # Extraction du texte du PDF
        extracted_text = await cv_processor.extract_text_from_pdf(file_path)
        
        # Traitement avec l'IA
        cv_data = await ai_extractor.extract_cv_information(extracted_text)
        
        # Génération du fichier de sortie
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"cv_extracted_{timestamp}.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Sauvegarde du JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cv_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"CV traité avec succès. Fichier de sortie: {output_path}")
        
        return {
            "message": "CV traité avec succès",
            "input_file": file_path,
            "output_file": output_path,
            "extracted_data": cv_data,
            "processing_time": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-cv-from-path")
async def process_cv_from_path(
    pdf_path: str = Form(...),
    output_format: str = Form(default="json")
):
    """
    Traitement d'un CV PDF à partir de son chemin d'accès
    """
    try:
        # Vérification de l'existence du fichier
        if not os.path.exists(pdf_path):
            raise HTTPException(
                status_code=404, 
                detail="Fichier PDF non trouvé"
            )
        
        if not pdf_path.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="Le fichier doit être au format PDF"
            )
        
        logger.info(f"Début du traitement du CV depuis le chemin: {pdf_path}")
        
        # Extraction du texte du PDF
        extracted_text = await cv_processor.extract_text_from_pdf(pdf_path)
        
        # Traitement avec l'IA
        cv_data = await ai_extractor.extract_cv_information(extracted_text)
        
        # Génération du fichier de sortie
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"cv_extracted_{timestamp}.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Sauvegarde du JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cv_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"CV traité avec succès. Fichier de sortie: {output_path}")
        
        return {
            "message": "CV traité avec succès",
            "input_file": pdf_path,
            "output_file": output_path,
            "extracted_data": cv_data,
            "processing_time": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-result/{filename}")
async def download_result(filename: str):
    """
    Téléchargement d'un fichier de résultat
    """
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404, 
                detail="Fichier de résultat non trouvé"
            )
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/json'
        )
        
    except Exception as e:
        logger.error(f"Erreur lors du téléchargement: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-results")
async def list_results():
    """
    Liste des fichiers de résultats disponibles
    """
    try:
        results = []
        for filename in os.listdir(OUTPUT_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(OUTPUT_DIR, filename)
                file_stat = os.stat(file_path)
                results.append({
                    "filename": filename,
                    "size": file_stat.st_size,
                    "created": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                })
        
        return {
            "results": results,
            "total_count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la liste des résultats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
