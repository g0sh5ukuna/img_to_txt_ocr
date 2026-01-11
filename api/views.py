"""
Views pour l'API REST
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.http import Http404

from documents.models import Document, OCRResult
from documents.services.document_service import DocumentService
from .serializers import (
    DocumentSerializer,
    DocumentListSerializer,
    DocumentUploadSerializer,
)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des documents via API
    
    list: Liste tous les documents de l'utilisateur authentifié
    retrieve: Récupère un document spécifique
    create: Upload et traitement OCR d'un nouveau document
    destroy: Supprime un document
    """
    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == 'list':
            return DocumentListSerializer
        if self.action == 'create':
            return DocumentUploadSerializer
        return DocumentSerializer
    
    def get_queryset(self):
        """Filtre les documents par utilisateur authentifié"""
        return Document.objects.filter(user=self.request.user).order_by('-uploaded_at')
    
    def get_object(self):
        """Retourne un document spécifique avec vérification de propriété"""
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    
    def create(self, request, *args, **kwargs):
        """
        Upload et traitement OCR d'un nouveau document
        
        POST /api/documents/
        Content-Type: multipart/form-data
        Body:
            - file: fichier à traiter (obligatoire)
            - language: code langue ISO 639-2 (optionnel)
            - engine: nom du moteur OCR (optionnel, défaut: tesseract)
        """
        serializer = DocumentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uploaded_file = serializer.validated_data['file']
        language = serializer.validated_data.get('language') or None
        engine = serializer.validated_data.get('engine') or 'tesseract'
        
        try:
            service = DocumentService()
            
            # Création du document
            document = service.create_document(
                user=request.user,
                uploaded_file=uploaded_file,
                language=language
            )
            
            # Traitement OCR
            try:
                ocr_result = service.process_document_ocr(
                    document=document,
                    language=language,
                    engine_name=engine
                )
            except Exception as e:
                document.status = Document.Status.FAILED
                document.error_message = str(e)
                document.save()
                return Response(
                    {
                        'error': 'Erreur lors du traitement OCR',
                        'message': str(e),
                        'document_id': document.id,
                        'status': document.status,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Retour du document avec le résultat OCR
            response_serializer = DocumentSerializer(
                document,
                context={'request': request}
            )
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de l\'upload: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def text(self, request, pk=None):
        """
        Récupère le texte extrait d'un document
        
        GET /api/documents/{id}/text/
        """
        document = self.get_object()
        
        if document.status != Document.Status.COMPLETED:
            return Response(
                {'error': 'Le document n\'a pas encore été traité'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not document.extracted_text:
            return Response(
                {'error': 'Aucun texte extrait disponible'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'document_id': document.id,
            'file_name': document.file_name,
            'text': document.extracted_text,
            'confidence_score': document.confidence_score,
            'language': document.language_detected,
        })
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Télécharge le texte extrait d'un document en format TXT
        
        GET /api/documents/{id}/download/
        """
        document = self.get_object()
        
        if document.status != Document.Status.COMPLETED or not document.extracted_text:
            return Response(
                {'error': 'Le texte n\'est pas disponible pour le téléchargement'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.http import HttpResponse
        import os
        
        response = HttpResponse(document.extracted_text, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{os.path.splitext(document.file_name)[0]}.txt"'
        return response
