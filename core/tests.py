"""
Tests pour l'app core
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from documents.models import Document


class HomeViewTest(TestCase):
    """Tests pour la vue home"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_home_redirects_to_login_when_not_authenticated(self):
        """Test que home redirige vers login si non authentifié"""
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login'))
    
    def test_home_redirects_to_ocr_tools_when_authenticated(self):
        """Test que home redirige vers ocr_tools si authentifié"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('ocr_tools'))


class LoginViewTest(TestCase):
    """Tests pour la vue login"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Test l'affichage de la page de connexion"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
    
    def test_login_view_post_valid(self):
        """Test la connexion avec des identifiants valides"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('ocr_tools'))
        self.assertTrue(self.client.session['_auth_user_id'])
    
    def test_login_view_post_invalid(self):
        """Test la connexion avec des identifiants invalides"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertFalse(self.client.session.get('_auth_user_id'))


class LogoutViewTest(TestCase):
    """Tests pour la vue logout"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_logout_view(self):
        """Test la déconnexion"""
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(self.client.session.get('_auth_user_id'))


class OCRToolsViewTest(TestCase):
    """Tests pour la vue ocr_tools"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_ocr_tools_view_get(self):
        """Test l'affichage de la page OCR tools"""
        response = self.client.get(reverse('ocr_tools'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/ocr_tools.html')
        self.assertIn('form', response.context)
    
    def test_ocr_tools_view_requires_login(self):
        """Test que la vue ocr_tools nécessite une connexion"""
        self.client.logout()
        response = self.client.get(reverse('ocr_tools'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('ocr_tools')}")


class DocumentHistoryViewTest(TestCase):
    """Tests pour la vue document_history"""
    
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_document_history_view_get(self):
        """Test l'affichage de l'historique des documents"""
        response = self.client.get(reverse('document_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/document_history.html')
        self.assertIn('documents', response.context)
    
    def test_document_history_view_requires_login(self):
        """Test que la vue document_history nécessite une connexion"""
        self.client.logout()
        response = self.client.get(reverse('document_history'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('document_history')}")
