"""
Tests pour les services de l'app documents
"""
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from documents.models import Document, OCRResult
from documents.services.document_service import DocumentService
from documents.services.document_service import DocumentService
import os


class DocumentServiceTest(TestCase):
    """Tests pour le service DocumentService"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.service = DocumentService()
    
    def _create_test_image_file(self, filename="test_image.jpg"):
        """Crée un fichier image de test en mémoire"""
        img = Image.new('RGB', (100, 100), color='white')
        img_io = BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        return SimpleUploadedFile(
            filename,
            img_io.read(),
            content_type='image/jpeg'
        )
    
    def test_create_document_valid_file(self):
        """Test la création d'un document avec un fichier valide"""
        uploaded_file = self._create_test_image_file()
        
        document = self.service.create_document(
            user=self.user,
            uploaded_file=uploaded_file,
            language=None
        )
        
        self.assertIsNotNone(document)
        self.assertEqual(document.user, self.user)
        self.assertEqual(document.file_name, "test_image.jpg")
        self.assertEqual(document.status, Document.Status.PENDING)
        self.assertIsNotNone(document.uploaded_at)
    
    def test_create_document_invalid_file_size(self):
        """Test la création d'un document avec un fichier trop volumineux"""
        # Créer un fichier trop volumineux (simulé)
        large_content = b'x' * (100 * 1024 * 1024)  # 100MB
        uploaded_file = SimpleUploadedFile(
            "large_file.jpg",
            large_content,
            content_type='image/jpeg'
        )
        
        with self.assertRaises(ValueError):
            self.service.create_document(
                user=self.user,
                uploaded_file=uploaded_file,
                language=None
            )
    
    def test_create_document_invalid_mime_type(self):
        """Test la création d'un document avec un type MIME invalide"""
        uploaded_file = SimpleUploadedFile(
            "test_file.exe",
            b'fake executable content',
            content_type='application/x-msdownload'
        )
        
        with self.assertRaises(ValueError):
            self.service.create_document(
                user=self.user,
                uploaded_file=uploaded_file,
                language=None
            )
    
    @override_settings(CELERY_ENABLED=False)
    def test_service_initialization(self):
        """Test l'initialisation du service"""
        service = DocumentService()
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.validator)
    
    def test_document_creation_sets_correct_fields(self):
        """Test que la création d'un document définit correctement les champs"""
        uploaded_file = self._create_test_image_file("test.png")
        
        document = self.service.create_document(
            user=self.user,
            uploaded_file=uploaded_file,
            language="fra"
        )
        
        # Vérifier les champs de base
        self.assertEqual(document.user, self.user)
        self.assertEqual(document.file_name, "test.png")
        self.assertEqual(document.status, Document.Status.PENDING)
        
        # Vérifier que le fichier est sauvegardé
        self.assertTrue(document.original_file)
        self.assertTrue(os.path.exists(document.original_file.path))
        
        # Vérifier le type MIME
        self.assertIn(document.mime_type, ['image/png', 'image/jpeg'])
