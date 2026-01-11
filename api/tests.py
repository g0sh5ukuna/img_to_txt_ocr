"""
Tests pour l'API REST
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from documents.models import Document, OCRResult


class DocumentAPITest(TestCase):
    """Tests pour l'API REST des documents"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_list_documents_authenticated(self):
        """Test la liste des documents pour un utilisateur authentifié"""
        response = self.client.get('/api/v1/documents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data or [])
    
    def test_list_documents_unauthenticated(self):
        """Test que la liste des documents nécessite une authentification"""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/v1/documents/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_document_requires_file(self):
        """Test que la création d'un document nécessite un fichier"""
        response = self.client.post('/api/v1/documents/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_document_detail(self):
        """Test la récupération du détail d'un document"""
        from django.core.files.uploadedfile import SimpleUploadedFile
        
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
            status=Document.Status.COMPLETED
        )
        
        response = self.client.get(f'/api/v1/documents/{document.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], document.id)
        self.assertEqual(response.data['file_name'], document.file_name)
    
    def test_get_document_text(self):
        """Test la récupération du texte extrait d'un document"""
        from django.core.files.uploadedfile import SimpleUploadedFile
        
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
            status=Document.Status.COMPLETED,
            extracted_text="Test extracted text"
        )
        
        response = self.client.get(f'/api/v1/documents/{document.id}/text/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], "Test extracted text")
    
    def test_delete_document(self):
        """Test la suppression d'un document"""
        from django.core.files.uploadedfile import SimpleUploadedFile
        
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
        
        response = self.client.delete(f'/api/v1/documents/{document.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Document.objects.filter(id=document.id).exists())
