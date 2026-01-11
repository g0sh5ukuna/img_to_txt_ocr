# Dockerfile pour OCR Tool Django
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-fra \
    tesseract-ocr-eng \
    libmagic1 \
    poppler-utils \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Copie des requirements
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copie du code de l'application
COPY . .

# Création des répertoires nécessaires
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Collecte des fichiers statiques (sera fait à nouveau en production)
RUN python manage.py collectstatic --noinput || true

# Exposition du port
EXPOSE 8000

# Commande par défaut (sera surchargée par docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "img_to_txt_ocr.wsgi:application"]
