"""
Configuration Celery pour traitement asynchrone
"""
import os
from celery import Celery
from django.conf import settings

# Configuration du nom du module Django par défaut
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'img_to_txt_ocr.settings')

app = Celery('img_to_txt_ocr')

# Configuration avec le préfixe CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découverte automatique des tâches dans toutes les apps Django
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tâche de débogage pour tester Celery"""
    print(f'Request: {self.request!r}')
