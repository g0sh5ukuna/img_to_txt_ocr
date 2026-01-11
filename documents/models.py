from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import os


class Document(models.Model):
    """Modèle représentant un document uploadé"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('En attente')
        PROCESSING = 'processing', _('En traitement')
        COMPLETED = 'completed', _('Terminé')
        FAILED = 'failed', _('Échec')
    
    # Relations
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_("Utilisateur")
    )
    
    # Fichier
    original_file = models.FileField(
        upload_to='documents/%Y/%m/%d/',
        verbose_name=_("Fichier original")
    )
    file_name = models.CharField(
        max_length=255,
        verbose_name=_("Nom du fichier")
    )
    file_size = models.PositiveIntegerField(
        verbose_name=_("Taille du fichier (octets)")
    )
    mime_type = models.CharField(
        max_length=100,
        verbose_name=_("Type MIME")
    )
    
    # Métadonnées OCR
    language_detected = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name=_("Langue détectée")
    )
    pages_count = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Nombre de pages")
    )
    engine_used = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Moteur OCR utilisé")
    )
    
    # Résultats OCR
    extracted_text = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Texte extrait")
    )
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Score de confiance")
    )
    
    # Timestamps
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date d'upload"),
        db_index=True
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Date de traitement")
    )
    
    # Statut et erreurs
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Statut"),
        db_index=True
    )
    error_message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Message d'erreur")
    )
    
    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', 'uploaded_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.file_name} ({self.user.username})"
    
    def get_file_extension(self):
        """Retourne l'extension du fichier"""
        return os.path.splitext(self.file_name)[1].lower()


class OCRResult(models.Model):
    """Modèle représentant un résultat OCR détaillé"""
    
    # Relation
    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        related_name='ocr_result',
        verbose_name=_("Document")
    )
    
    # Texte extrait
    raw_text = models.TextField(
        verbose_name=_("Texte brut")
    )
    cleaned_text = models.TextField(
        verbose_name=_("Texte nettoyé")
    )
    
    # Métadonnées
    confidence_score = models.FloatField(
        verbose_name=_("Score de confiance")
    )
    language_detected = models.CharField(
        max_length=10,
        verbose_name=_("Langue détectée")
    )
    engine_used = models.CharField(
        max_length=50,
        verbose_name=_("Moteur OCR utilisé")
    )
    
    # Statistiques
    word_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Nombre de mots")
    )
    character_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Nombre de caractères")
    )
    processing_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Temps de traitement (secondes)")
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )
    
    class Meta:
        verbose_name = _("Résultat OCR")
        verbose_name_plural = _("Résultats OCR")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OCR Result for {self.document.file_name}"
