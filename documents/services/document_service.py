import os
from typing import Optional
from PIL import Image
from django.core.files.uploadedfile import UploadedFile
from django.conf import settings
from documents.models import Document, OCRResult
from ocr.engines.factory import OCREngineFactory
from ocr.validators.file_validator import FileValidator

# Détection MIME optionnelle avec python-magic
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False


class DocumentService:
    """Service pour gérer les documents et le traitement OCR"""
    
    def __init__(self):
        self.validator = FileValidator()
    
    def create_document(
        self,
        user,
        uploaded_file: UploadedFile,
        language: Optional[str] = None
    ) -> Document:
        """
        Crée un document à partir d'un fichier uploadé
        
        Args:
            user: Utilisateur Django
            uploaded_file: Fichier uploadé
            language: Langue pour l'OCR (optionnel)
        
        Returns:
            Instance de Document créée
        """
        # Validation
        is_valid, error_message = self.validator.validate_file(uploaded_file)
        if not is_valid:
            raise ValueError(error_message)
        
        # Détection du type MIME réel (optionnel)
        if MAGIC_AVAILABLE:
            try:
                uploaded_file.seek(0)
                mime_type = magic.from_buffer(uploaded_file.read(1024), mime=True)
                uploaded_file.seek(0)
            except Exception:
                mime_type = getattr(uploaded_file, 'content_type', 'application/octet-stream')
        else:
            mime_type = getattr(uploaded_file, 'content_type', 'application/octet-stream')
        
        # Création du document
        document = Document.objects.create(
            user=user,
            original_file=uploaded_file,
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
            mime_type=mime_type,
            status=Document.Status.PENDING,
        )
        
        return document
    
    def process_document_ocr(
        self,
        document: Document,
        language: Optional[str] = None,
        engine_name: Optional[str] = None
    ) -> OCRResult:
        """
        Traite un document avec OCR
        
        Args:
            document: Instance de Document
            language: Langue pour l'OCR (optionnel)
            engine_name: Nom du moteur OCR (optionnel, défaut: tesseract)
        
        Returns:
            Instance de OCRResult créée
        """
        import time
        start_time = time.time()
        
        # Mise à jour du statut
        document.status = Document.Status.PROCESSING
        document.save()
        
        try:
            # Chargement de l'image
            image = self._load_image(document.original_file.path, document.mime_type)
            
            # Obtention du moteur OCR
            engine = OCREngineFactory.get_engine(engine_name or 'tesseract')
            
            # Traitement OCR
            result = engine.extract_text(image, language=language)
            
            # Nettoyage du texte
            cleaned_text = self._clean_text(result['text'])
            
            # Calcul des statistiques
            word_count = len(cleaned_text.split())
            character_count = len(cleaned_text)
            processing_time = time.time() - start_time
            
            # Création du résultat OCR
            ocr_result = OCRResult.objects.create(
                document=document,
                raw_text=result['text'],
                cleaned_text=cleaned_text,
                confidence_score=result['confidence'],
                language_detected=result['language'],
                engine_used=engine.name,
                word_count=word_count,
                character_count=character_count,
                processing_time=processing_time,
            )
            
            # Mise à jour du document
            document.status = Document.Status.COMPLETED
            document.extracted_text = cleaned_text
            document.confidence_score = result['confidence']
            document.language_detected = result['language']
            document.engine_used = engine.name
            document.processed_at = ocr_result.created_at
            document.save()
            
            return ocr_result
            
        except Exception as e:
            # Gestion des erreurs
            document.status = Document.Status.FAILED
            document.error_message = str(e)
            document.save()
            raise
    
    def _load_image(self, file_path: str, mime_type: str) -> Image.Image:
        """
        Charge une image depuis un fichier (support PDF via pdf2image)
        
        Args:
            file_path: Chemin vers le fichier
            mime_type: Type MIME du fichier
        
        Returns:
            Image PIL
        """
        if mime_type == 'application/pdf':
            # Conversion PDF en image
            try:
                from pdf2image import convert_from_path
                images = convert_from_path(file_path)
                if images:
                    return images[0]  # Retourne la première page
                else:
                    raise ValueError("Le PDF ne contient aucune page")
            except ImportError:
                raise ValueError("pdf2image n'est pas installé pour traiter les PDF")
            except Exception as e:
                raise ValueError(f"Erreur lors de la conversion PDF: {str(e)}")
        else:
            # Image classique
            try:
                return Image.open(file_path)
            except Exception as e:
                raise ValueError(f"Erreur lors de l'ouverture de l'image: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Nettoie le texte extrait
        
        Args:
            text: Texte brut
        
        Returns:
            Texte nettoyé
        """
        if not text:
            return ""
        
        # Supprime les espaces multiples
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            cleaned_line = ' '.join(line.split())
            if cleaned_line:  # Ignore les lignes vides
                cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
