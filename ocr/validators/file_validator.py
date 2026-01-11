from django.core.exceptions import ValidationError
from django.conf import settings
from typing import Tuple


class FileValidator:
    """Validateur pour les fichiers uploadés"""
    
    def __init__(self):
        self.max_size = getattr(settings, 'MAX_FILE_SIZE', 50 * 1024 * 1024)  # 50MB par défaut
        self.allowed_mime_types = getattr(settings, 'ALLOWED_MIME_TYPES', [
            'image/jpeg',
            'image/png',
            'image/tiff',
            'image/bmp',
            'image/webp',
            'application/pdf',
        ])
    
    def validate_file(self, uploaded_file) -> Tuple[bool, str]:
        """
        Valide un fichier uploadé
        
        Args:
            uploaded_file: Fichier uploadé (django.core.files.uploadedfile.UploadedFile)
        
        Returns:
            Tuple (is_valid, error_message)
        """
        # Vérifie la taille
        if uploaded_file.size > self.max_size:
            max_size_mb = self.max_size / (1024 * 1024)
            return False, f"Le fichier est trop volumineux. Taille maximum: {max_size_mb:.1f} MB"
        
        # Vérifie le type MIME
        content_type = getattr(uploaded_file, 'content_type', None)
        if content_type and content_type not in self.allowed_mime_types:
            return False, f"Type de fichier non autorisé: {content_type}"
        
        # Vérifie l'extension
        file_name = getattr(uploaded_file, 'name', '')
        if file_name:
            ext = file_name.split('.')[-1].lower()
            allowed_extensions = ['jpg', 'jpeg', 'png', 'tiff', 'tif', 'bmp', 'webp', 'pdf']
            if ext not in allowed_extensions:
                return False, f"Extension de fichier non autorisée: .{ext}"
        
        return True, ""
