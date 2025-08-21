#!/usr/bin/env python3
"""
Script de test de l'extracteur amélioré
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

async def test_improved_extraction():
    """Teste l'extraction améliorée"""
    print("🚀 Test de l'extracteur amélioré")
    print("=" * 50)
    
    try:
        # Import des services
        from services.cv_processor_simple import CVProcessorSimple
        from services.ai_extractor_improved import AIExtractorImproved
        
        # Initialisation
        cv_processor = CVProcessorSimple()
        ai_extractor = AIExtractorImproved()
        
        # Vérification des fichiers PDF
        uploads_dir = Path("uploads")
        pdf_files = list(uploads_dir.glob('*.pdf'))
        
        if not pdf_files:
            print("❌ Aucun fichier PDF trouvé dans uploads/")
            return
        
        # Traitement du premier PDF
        test_pdf = str(pdf_files[0])
        print(f"📄 Traitement de: {test_pdf}")
        
        # Extraction du texte
        print("1️⃣ Extraction du texte...")
        extracted_text = await cv_processor.extract_text_from_pdf(test_pdf)
        
        if not extracted_text:
            print("❌ Aucun texte extrait")
            return
        
        print(f"   ✅ Texte extrait: {len(extracted_text)} caractères")
        
        # Extraction des informations
        print("2️⃣ Extraction des informations...")
        cv_info = await ai_extractor.extract_cv_information(extracted_text)
        
        print(f"   ✅ Informations extraites: {len(cv_info)} sections")
        
        # Affichage des informations clés
        print("\n📊 Informations extraites:")
        print("-" * 30)
        
        # Informations personnelles
        if cv_info.get('personal_info'):
            personal = cv_info['personal_info']
            if personal.get('full_name'):
                print(f"👤 Nom: {personal['full_name']}")
        
        # Informations de contact
        if cv_info.get('contact_info'):
            contact = cv_info['contact_info']
            if contact.get('email'):
                print(f"📧 Email: {contact['email']}")
            if contact.get('phone'):
                print(f"📱 Téléphone: {contact['phone']}")
            if contact.get('linkedin'):
                print(f"💼 LinkedIn: {contact['linkedin']}")
            if contact.get('github'):
                print(f"🐙 GitHub: {contact['github']}")
        
        # Adresse
        if cv_info.get('address'):
            print(f"📍 Adresse: {cv_info['address']}")
        
        # Résumé professionnel
        if cv_info.get('professional_summary'):
            summary = cv_info['professional_summary'][:100] + "..." if len(cv_info['professional_summary']) > 100 else cv_info['professional_summary']
            print(f"📝 Résumé: {summary}")
        
        # Expérience
        if cv_info.get('work_experience'):
            print(f"💼 Expériences: {len(cv_info['work_experience'])} postes")
            for i, exp in enumerate(cv_info['work_experience'][:3]):  # Afficher les 3 premières
                print(f"   {i+1}. {exp.get('title', 'N/A')} - {exp.get('company', 'N/A')}")
        
        # Éducation
        if cv_info.get('education'):
            print(f"🎓 Formation: {len(cv_info['education'])} diplômes")
            for i, edu in enumerate(cv_info['education'][:3]):  # Afficher les 3 premières
                print(f"   {i+1}. {edu.get('degree', 'N/A')} - {edu.get('institution', 'N/A')}")
        
        # Compétences
        if cv_info.get('skills'):
            print(f"🛠️ Compétences: {len(cv_info['skills'])} technologies")
            skills_display = ', '.join(cv_info['skills'][:10])  # Afficher les 10 premières
            print(f"   {skills_display}")
        
        # Langues
        if cv_info.get('languages'):
            print(f"🌍 Langues: {', '.join(cv_info['languages'])}")
        
        # Projets
        if cv_info.get('projects'):
            print(f"🚀 Projets: {len(cv_info['projects'])} réalisations")
            for i, project in enumerate(cv_info['projects'][:3]):  # Afficher les 3 premiers
                print(f"   {i+1}. {project.get('name', 'N/A')}")
        
        # Hobbies
        if cv_info.get('hobbies'):
            print(f"🎯 Hobbies: {', '.join(cv_info['hobbies'])}")
        
        # Sauvegarde des résultats
        print("\n3️⃣ Sauvegarde des résultats...")
        outputs_dir = Path("outputs")
        output_filename = f"cv_improved_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = outputs_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cv_info, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ Résultats sauvegardés: {output_path}")
        
        # Métadonnées d'extraction
        if cv_info.get('extraction_metadata'):
            metadata = cv_info['extraction_metadata']
            print(f"\n📈 Métadonnées d'extraction:")
            print(f"   - Méthode: {metadata.get('extraction_method', 'N/A')}")
            print(f"   - Score de confiance: {metadata.get('confidence_score', 'N/A')}")
            print(f"   - Longueur du texte: {metadata.get('text_length', 'N/A')} caractères")
        
        print("\n" + "=" * 50)
        print("🎉 Extraction améliorée terminée avec succès!")
        print(f"📁 Fichier généré: {output_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_improved_extraction())
