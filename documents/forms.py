from django import forms
from documents.models import Document


class CustomFileInput(forms.FileInput):
    """Widget personnalisé pour l'upload de fichiers avec style moderne"""
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'file-input',
            'accept': '.jpg,.jpeg,.png,.tiff,.tif,.bmp,.webp,.pdf',
            'id': 'file-upload-input',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class DocumentUploadForm(forms.Form):
    """Formulaire pour l'upload de documents"""
    
    file = forms.FileField(
        label="Sélectionner un fichier",
        help_text="Formats supportés: JPEG, PNG, TIFF, BMP, WebP, PDF (max 50MB)",
        widget=CustomFileInput(attrs={
            'accept': '.jpg,.jpeg,.png,.tiff,.tif,.bmp,.webp,.pdf',
        }),
        required=True,
    )
    
    language = forms.ChoiceField(
        label="Langue du document",
        required=False,
        choices=[
            ('', 'Auto-détection'),
            ('fra', 'Français'),
            ('eng', 'Anglais'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control language-select',
        }),
        help_text="Sélectionnez la langue du document pour améliorer la précision (optionnel)"
    )
