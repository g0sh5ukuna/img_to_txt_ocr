"""
Serializers pour l'API REST
"""
from rest_framework import serializers
from documents.models import Document, OCRResult
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer pour les utilisateurs"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class OCRResultSerializer(serializers.ModelSerializer):
    """Serializer pour les résultats OCR"""
    
    class Meta:
        model = OCRResult
        fields = [
            'id',
            'raw_text',
            'cleaned_text',
            'confidence_score',
            'language_detected',
            'engine_used',
            'word_count',
            'character_count',
            'processing_time',
            'created_at',
        ]
        read_only_fields = fields


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer pour les documents"""
    user = UserSerializer(read_only=True)
    ocr_result = OCRResultSerializer(read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id',
            'user',
            'file_name',
            'file_size',
            'mime_type',
            'file_url',
            'language_detected',
            'pages_count',
            'engine_used',
            'extracted_text',
            'confidence_score',
            'status',
            'error_message',
            'uploaded_at',
            'processed_at',
            'ocr_result',
        ]
        read_only_fields = [
            'id',
            'user',
            'file_name',
            'file_size',
            'mime_type',
            'language_detected',
            'pages_count',
            'engine_used',
            'extracted_text',
            'confidence_score',
            'status',
            'error_message',
            'uploaded_at',
            'processed_at',
            'ocr_result',
        ]
    
    def get_file_url(self, obj):
        """Retourne l'URL du fichier"""
        if obj.original_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.original_file.url)
            return obj.original_file.url
        return None


class DocumentUploadSerializer(serializers.Serializer):
    """Serializer pour l'upload de documents"""
    file = serializers.FileField(required=True)
    language = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text="Code langue ISO 639-2 (ex: fra, eng). Laissé vide pour auto-détection."
    )
    engine = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default='tesseract',
        help_text="Nom du moteur OCR à utiliser (ex: tesseract). Par défaut: tesseract"
    )


class DocumentListSerializer(serializers.ModelSerializer):
    """Serializer simplifié pour la liste des documents"""
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id',
            'user',
            'file_name',
            'file_size',
            'mime_type',
            'status',
            'confidence_score',
            'uploaded_at',
            'processed_at',
        ]
        read_only_fields = fields
