"""
Django settings for img_to_txt_ocr project.
"""

# Importation de Celery pour initialiser l'app (optionnel)
try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except ImportError:
    # Celery n'est pas installé, l'application fonctionne sans
    pass
