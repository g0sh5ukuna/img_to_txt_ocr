"""
Tâches Celery pour le traitement OCR asynchrone
"""
from celery import shared_task
from django.utils import timezone
from documents.models import Document
from documents.services.document_service import DocumentService


@shared_task(bind=True, name='documents.process_document_ocr')
def process_document_ocr_task(self, document_id, language=None, engine_name=None):
    """
    Tâche Celery pour traiter un document avec OCR de manière asynchrone
    
    Args:
        document_id: ID du document à traiter
        language: Langue pour l'OCR (optionnel)
        engine_name: Nom du moteur OCR (optionnel)
    
    Returns:
        ID du OCRResult créé
    """
    try:
        document = Document.objects.get(id=document_id)
        
        # Vérification que le document est en attente ou en erreur
        if document.status not in [Document.Status.PENDING, Document.Status.FAILED]:
            return {
                'status': 'error',
                'message': f'Document déjà traité ou en cours (statut: {document.status})',
                'document_id': document_id
            }
        
        # Traitement OCR
        service = DocumentService()
        ocr_result = service.process_document_ocr(
            document=document,
            language=language,
            engine_name=engine_name or 'tesseract'
        )
        
        return {
            'status': 'success',
            'document_id': document_id,
            'ocr_result_id': ocr_result.id,
            'confidence_score': ocr_result.confidence_score,
            'word_count': ocr_result.word_count,
            'character_count': ocr_result.character_count,
        }
        
    except Document.DoesNotExist:
        return {
            'status': 'error',
            'message': f'Document {document_id} non trouvé',
            'document_id': document_id
        }
    except Exception as e:
        # Mise à jour du statut d'erreur
        try:
            document = Document.objects.get(id=document_id)
            document.status = Document.Status.FAILED
            document.error_message = str(e)
            document.save()
        except:
            pass
        
        # Relancer l'exception pour Celery retry
        raise self.retry(exc=e, countdown=60, max_retries=3)
