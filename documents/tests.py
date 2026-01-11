"""
Tests pour l'app documents
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from documents.models import Document, OCRResult


class DocumentModelTest(TestCase):
    """Tests pour le modèle Document"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_document_creation(self):
        """Test la création d'un document"""
        file_content = b'fake image content'
        uploaded_file = SimpleUploadedFile(
            "test_image.jpg",
            file_content,
            content_type="image/jpeg"
        )
        
        document = Document.objects.create(
            user=self.user,
            original_file=uploaded_file,
            file_name="test_image.jpg",
            file_size=len(file_content),
            mime_type="image/jpeg",
            status=Document.Status.PENDING
        )
        
        self.assertEqual(document.user, self.user)
        self.assertEqual(document.file_name, "test_image.jpg")
        self.assertEqual(document.status, Document.Status.PENDING)
        self.assertIsNotNone(document.uploaded_at)
    
    def test_document_str(self):
        """Test la représentation string d'un document"""
        file_content = b'fake image content'
        uploaded_file = SimpleUploadedFile(
            "test_image.jpg",
            file_content,
            content_type="image/jpeg"
        )
        
        document = Document.objects.create(
            user=self.user,
            original_file=uploaded_file,
            file_name="test_image.jpg",
            file_size=len(file_content),
            mime_type="image/jpeg"
        )
        
        expected_str = f"test_image.jpg ({self.user.username})"
        self.assertEqual(str(document), expected_str)
    
    def test_document_get_file_extension(self):
        """Test la méthode get_file_extension"""
        file_content = b'fake image content'
        uploaded_file = SimpleUploadedFile(
            "test_image.jpg",
            file_content,
            content_type="image/jpeg"
        )
        
        document = Document.objects.create(
            user=self.user,
            original_file=uploaded_file,
            file_name="test_image.jpg",
            file_size=len(file_content),
            mime_type="image/jpeg"
        )
        
        self.assertEqual(document.get_file_extension(), '.jpg')
    
    def test_document_status_choices(self):
        """Test les choix de statut"""
        self.assertEqual(Document.Status.PENDING, 'pending')
        self.assertEqual(Document.Status.PROCESSING, 'processing')
        self.assertEqual(Document.Status.COMPLETED, 'completed')
        self.assertEqual(Document.Status.FAILED, 'failed')


class OCRResultModelTest(TestCase):
    """Tests pour le modèle OCRResult"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        file_content = b'fake image content'
        uploaded_file = SimpleUploadedFile(
            "test_image.jpg",
            file_content,
            content_type="image/jpeg"
        )
        
        self.document = Document.objects.create(
            user=self.user,
            original_file=uploaded_file,
            file_name="test_image.jpg",
            file_size=len(file_content),
            mime_type="image/jpeg",
            status=Document.Status.COMPLETED
        )
    
    def test_ocr_result_creation(self):
        """Test la création d'un résultat OCR"""
        ocr_result = OCRResult.objects.create(
            document=self.document,
            raw_text="Test raw text",
            cleaned_text="Test cleaned text",
            confidence_score=0.95,
            language_detected="fra",
            engine_used="tesseract",
            word_count=2,
            character_count=18
        )
        
        self.assertEqual(ocr_result.document, self.document)
        self.assertEqual(ocr_result.raw_text, "Test raw text")
        self.assertEqual(ocr_result.cleaned_text, "Test cleaned text")
        self.assertEqual(ocr_result.confidence_score, 0.95)
        self.assertEqual(ocr_result.language_detected, "fra")
        self.assertEqual(ocr_result.engine_used, "tesseract")
        self.assertIsNotNone(ocr_result.created_at)
    
    def test_ocr_result_str(self):
        """Test la représentation string d'un résultat OCR"""
        ocr_result = OCRResult.objects.create(
            document=self.document,
            raw_text="Test raw text",
            cleaned_text="Test cleaned text",
            confidence_score=0.95,
            language_detected="fra",
            engine_used="tesseract"
        )
        
        expected_str = f"OCR Result for {self.document.file_name}"
        self.assertEqual(str(ocr_result), expected_str)
    
    def test_ocr_result_one_to_one_relation(self):
        """Test la relation OneToOne entre Document et OCRResult"""
        ocr_result = OCRResult.objects.create(
            document=self.document,
            raw_text="Test raw text",
            cleaned_text="Test cleaned text",
            confidence_score=0.95,
            language_detected="fra",
            engine_used="tesseract"
        )
        
        # Vérifier que l'accès via related_name fonctionne
        self.assertEqual(self.document.ocr_result, ocr_result)
        
        # Vérifier que l'accès inverse fonctionne
        self.assertEqual(ocr_result.document, self.document)
