from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from documents.forms import DocumentUploadForm
from documents.models import Document, OCRResult
from documents.services.document_service import DocumentService
import os


def home(request):
    """Page d'accueil - redirige vers login ou OCR tools"""
    if request.user.is_authenticated:
        return redirect('ocr_tools')
    return redirect('login')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Vue de connexion personnalisée"""
    if request.user.is_authenticated:
        return redirect('ocr_tools')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Connexion réussie !')
                next_url = request.GET.get('next', 'ocr_tools')
                return redirect(next_url)
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
    
    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')


@login_required
@require_http_methods(["GET", "POST"])
def ocr_tools(request):
    """Page principale pour tester les outils OCR avec upload"""
    form = DocumentUploadForm()
    document = None
    ocr_result = None
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                service = DocumentService()
                document = service.create_document(
                    user=request.user,
                    uploaded_file=form.cleaned_data['file'],
                    language=form.cleaned_data.get('language') or None
                )
                
                # Traitement OCR
                try:
                    ocr_result = service.process_document_ocr(
                        document=document,
                        language=form.cleaned_data.get('language') or None
                    )
                    messages.success(request, 'Document traité avec succès !')
                    # Recharger le document pour avoir les données à jour
                    document.refresh_from_db()
                except Exception as e:
                    messages.error(request, f'Erreur lors du traitement OCR: {str(e)}')
                    if document:
                        document.refresh_from_db()
                    
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'upload: {str(e)}')
    
    # Liste des documents récents
    recent_documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')[:5]
    
    context = {
        'form': form,
        'recent_documents': recent_documents,
        'current_document': document,
        'current_ocr_result': ocr_result,
    }
    return render(request, 'core/ocr_tools.html', context)


@login_required
def ocr_result(request, document_id):
    """Affiche le résultat OCR d'un document"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    
    # Vérifie si le résultat OCR existe
    try:
        ocr_result = document.ocr_result
    except OCRResult.DoesNotExist:
        ocr_result = None
    
    context = {
        'document': document,
        'ocr_result': ocr_result,
    }
    return render(request, 'core/ocr_result.html', context)


@login_required
def download_text(request, document_id):
    """Télécharge le texte extrait en format TXT"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    
    if not document.extracted_text:
        raise Http404("Aucun texte extrait pour ce document")
    
    response = HttpResponse(document.extracted_text, content_type='text/plain; charset=utf-8')
    filename = os.path.splitext(document.file_name)[0] + '.txt'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def document_history(request):
    """Affiche l'historique des documents"""
    documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
    
    context = {
        'documents': documents,
    }
    return render(request, 'core/document_history.html', context)
