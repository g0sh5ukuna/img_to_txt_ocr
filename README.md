# 🖼️ OCR Tool - Outil OCR Open Source

> **Un outil OCR (Optical Character Recognition) simple, puissant et open source** pour convertir des images et PDF en texte avec Django.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2+](https://img.shields.io/badge/django-5.2+-green.svg)](https://www.djangoproject.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Status: In Development](https://img.shields.io/badge/status-in%20development-orange.svg)](https://github.com/g0sh5ukuna/img_to_txt_ocr)

---

## 📌 Présentation

**OCR Tool** est un outil web Django open source en développement actif, conçu pour extraire du texte à partir d'images (JPEG, PNG, TIFF, BMP, WebP) et de documents PDF. Développé avec une approche **DevSecOps**, il privilégie la **sécurité, la performance et la facilité d'utilisation**.

> ⚠️ **Note importante** : Ce projet est actuellement en **phase de développement initial**. Les fonctionnalités sont en cours d'implémentation. Consultez [.dev_evolutions.md](.dev_evolutions.md) pour suivre la progression.

### ✨ Features prévues

- 🔄 **Multi-engines OCR** : Tesseract, EasyOCR (Google Vision optionnel) - *En cours*
- 🔄 **Support multi-langues** : Français, Anglais, et plus de 80 langues - *Planifié*
- 🔄 **Interface web moderne** : Templates Django natifs (pas de frontend externe) - *En cours*
- 🔄 **Traitement asynchrone** : Celery pour les gros volumes (optionnel) - *Planifié*
- 🔄 **API REST** : Pour intégrations programmatiques - *Planifié*
- 🔄 **Sécurité renforcée** : Validation fichiers, scan antivirus, rate limiting - *Planifié*
- ✅ **Installation simple** : Fonctionne avec SQLite par défaut, PostgreSQL optionnel - *Architecture définie*
- 🔄 **Docker ready** : Démarrage en une commande - *Planifié*

---

## 🚀 Quick Start (En développement)

> ⚠️ **Le projet est actuellement en phase de développement initial.** Les instructions d'installation complètes seront disponibles prochainement.

### État actuel du projet

Le projet est au stade initial de développement :
- ✅ Structure de base Django configurée
- ✅ Architecture définie (voir [architecture_projets_opensource.md](architecture_projets_opensource.md))
- 🔄 Applications Django à créer
- 🔄 Modèles de données à implémenter
- 🔄 Interface utilisateur à développer
- 🔄 Intégration OCR à réaliser

### Installation pour développeurs/contributeurs

Si vous souhaitez contribuer au développement :

```bash
# 1. Cloner le projet
git clone https://github.com/g0sh5ukuna/img_to_txt_ocr.git
cd img_to_txt_ocr

# 2. Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer les migrations de base
python manage.py migrate

# 5. Créer un superutilisateur (ou utiliser la commande par défaut)
python manage.py create_default_admin  # Crée admin/admin
# OU
python manage.py createsuperuser  # Crée un superutilisateur personnalisé

# 6. Lancer le serveur de développement
python manage.py runserver

# ✅ Serveur Django de base accessible sur http://127.0.0.1:8000
# ⚠️ Les fonctionnalités OCR ne sont pas encore implémentées
```

---

## 📋 Prérequis

### Minimal (mode simple)
- **Python** >= 3.10
- **Tesseract OCR** installé sur le système
- **pip** et **virtualenv**

### Complet (production)
- **PostgreSQL** >= 14 (optionnel, SQLite par défaut)
- **Redis** >= 6 (pour Celery et cache, optionnel)
- **Docker & Docker Compose** (pour déploiement containerisé)

---

## 📂 Structure du projet

### Structure actuelle (réelle)

```
img_to_txt_ocr/
├── img_to_txt_ocr/                # Configuration Django
│   ├── settings.py                # Settings Django (à refactoriser)
│   ├── urls.py                    # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── templates/                     # Templates Django (structure de base)
│   ├── base/
│   ├── core/
│   └── registration/
├── static/                        # Fichiers statiques (structure de base)
│   ├── css/
│   ├── js/
│   └── img/
├── manage.py
├── README.md
├── architecture_projets_opensource.md  # Architecture complète prévue
└── .dev_evolutions.md             # Suivi du développement
```

### Structure prévue (architecture cible)

```
img_to_txt_ocr/
├── apps/                          # Applications Django modulaires (à créer)
│   ├── core/                      # App principale
│   ├── ocr/                       # Logique OCR (engines, processors)
│   ├── documents/                 # Gestion des documents
│   ├── frontend/                  # Interface utilisateur (templates)
│   ├── users/                     # Gestion utilisateurs
│   ├── api/                       # API REST
│   └── analytics/                 # Analytics & monitoring
├── config/                        # Configuration Django (à créer)
│   └── settings/                  # Settings par environnement
│       ├── base.py
│       ├── development.py
│       ├── simple.py              # Mode minimal
│       └── production.py
├── requirements.txt               # Dépendances Python
├── docker-compose.simple.yml      # Docker version simple (à créer)
├── docker-compose.yml             # Docker version complète (à créer)
└── ...
```

> 📖 **Architecture complète** : Voir [architecture_projets_opensource.md](architecture_projets_opensource.md) pour la vision complète  
> 📊 **Suivi du développement** : Voir [.dev_evolutions.md](.dev_evolutions.md) pour l'état actuel

---

## 🏗️ Architecture technique

### Stack principale

- **Backend** : Python 3.10+ / Django 5.2+
- **Frontend** : Templates Django natifs (pas de framework frontend externe)
- **OCR Engines** :
  - Tesseract OCR (par défaut, open source)
  - EasyOCR (optionnel, deep learning)
  - Google Vision API (optionnel, cloud)
- **Base de données** :
  - SQLite (par défaut, développement)
  - PostgreSQL (production, optionnel)
- **Traitement asynchrone** : Celery + Redis (optionnel)
- **Cache** : Redis ou cache mémoire local

### Sécurité

- Validation stricte des fichiers uploadés (MIME type, taille)
- Protection CSRF / XSS / SQL Injection
- Rate limiting par utilisateur/IP
- Scan antivirus (ClamAV, optionnel)
- Chiffrement des données sensibles
- Audit trail complet

### DevSecOps

- CI/CD avec GitHub Actions
- Tests automatisés (unit, integration, security, performance)
- Scan de sécurité automatisé (Bandit, Safety)
- Monitoring avec Prometheus/Grafana (optionnel)
- Logging centralisé (optionnel)

---

## ⚙️ Configuration

### Variables d'environnement

Copiez `.env.example` vers `.env` et configurez selon vos besoins :

```bash
# Configuration minimale
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données (SQLite par défaut)
# DATABASE_URL=sqlite:///db.sqlite3
# Pour PostgreSQL: DATABASE_URL=postgresql://user:password@localhost:5432/ocrtool

# Celery & Redis (optionnel)
# CELERY_BROKER_URL=redis://localhost:6379/0
# CELERY_RESULT_BACKEND=redis://localhost:6379/0

# OCR Engines
# EASYOCR_ENABLED=True
# GOOGLE_VISION_API_KEY=your-api-key

# Sécurité
# MAX_FILE_SIZE=52428800  # 50MB
# ALLOWED_MIME_TYPES=image/jpeg,image/png,application/pdf
```

### Installation des dépendances

```bash
pip install -r requirements.txt
```

> **Note :** Certaines dépendances optionnelles (EasyOCR, Celery, etc.) sont commentées dans `requirements.txt`. Décommentez-les selon vos besoins.

---

## 🧪 Tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=apps --cov-report=html

# Tests de sécurité
pytest tests/security/

# Tests de performance
pytest tests/performance/
```

Les tests couvrent :
- ✅ Logique métier OCR
- ✅ Validation et sécurité
- ✅ API REST
- ✅ Templates et vues
- ✅ Performance et charge

---

## 📚 Documentation

- **[Quick Start](docs/QUICKSTART.md)** : Guide de démarrage rapide
- **[Installation](docs/INSTALLATION.md)** : Installation détaillée
- **[Configuration](docs/CONFIGURATION.md)** : Toutes les options de configuration
- **[Architecture](architecture_projets_opensource.md)** : Architecture complète du projet
- **[API Documentation](docs/API.md)** : Documentation de l'API REST
- **[Déploiement](docs/DEPLOYMENT.md)** : Guide de déploiement production
- **[Contribution](docs/CONTRIBUTING.md)** : Comment contribuer au projet

---

## 🤝 Contribution

Les contributions sont **très bienvenues** ! Ce projet est open source et a besoin de vous.

### Comment contribuer

1. **Fork** le projet
2. Créer une **branche** (`git checkout -b feature/ma-feature`)
3. **Commit** vos changements (`git commit -m 'Ajout d'une nouvelle feature'`)
4. **Push** vers la branche (`git push origin feature/ma-feature`)
5. Ouvrir une **Pull Request**

### Standards de code

- Respecter PEP 8
- Utiliser Black pour le formatage
- Ajouter des tests pour les nouvelles features
- Documenter le code avec des docstrings
- Suivre les conventions Django

> 📖 **Guide complet** : Voir [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## 🔐 Sécurité

### Signaler une vulnérabilité

Si vous découvrez une vulnérabilité de sécurité, merci de **ne pas créer d'issue publique**. Contactez directement :

- **Email** : [votre-email] (pour signalement sécurité)
- **GitHub Security** : Utilisez la fonctionnalité [Security Advisories](https://github.com/g0sh5ukuna/img_to_txt_ocr/security/advisories)

### Bonnes pratiques appliquées

- ✅ Validation stricte de tous les inputs
- ✅ Protection CSRF/XSS/SQL Injection
- ✅ Gestion sécurisée des fichiers uploadés
- ✅ Rate limiting
- ✅ Secrets dans variables d'environnement
- ✅ Logs sans données sensibles

---

## 🗺️ Roadmap

> 📋 **Suivi détaillé** : Consultez [.dev_evolutions.md](.dev_evolutions.md) pour l'état complet et les tâches à réaliser.

### Phase 1 : MVP (En cours - Développement initial)
- [x] Structure de base Django
- [x] Architecture définie et documentée
- [ ] Refactorisation settings Django (structure config/)
- [ ] Création des apps Django de base
- [ ] Modèles de données (User, Document, OCRResult)
- [ ] Intégration Tesseract OCR
- [ ] Interface d'upload basique
- [ ] Affichage résultats

### Phase 2 : Features avancées (Planifié)
- [ ] Multi-engine OCR (EasyOCR, Google Vision)
- [ ] Traitement asynchrone avec Celery
- [ ] API REST complète
- [ ] Dashboard utilisateur
- [ ] Gestion batch

### Phase 3 : DevSecOps (Planifié)
- [ ] CI/CD avec GitHub Actions
- [ ] Tests automatisés complets
- [ ] Dockerisation complète
- [ ] Monitoring avec Prometheus/Grafana
- [ ] Documentation complète

### Phase 4 : Production (Planifié)
- [ ] Configuration production
- [ ] Optimisations performance
- [ ] Scaling horizontal
- [ ] Backup automatique

### Comment suivre le développement ?

- **État détaillé** : [.dev_evolutions.md](.dev_evolutions.md)
- **Architecture** : [architecture_projets_opensource.md](architecture_projets_opensource.md)
- **Issues GitHub** : [GitHub Issues](https://github.com/g0sh5ukuna/img_to_txt_ocr/issues)

---

## 📊 Statistiques

- **Dernière mise à jour** : 2024
- **Version actuelle** : 0.1.0 (développement)
- **Langages** : Python 3.10+
- **Framework** : Django 5.2+

---

## 📝 Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🧑‍💻 Auteur

**Josh (Sounon Josué)**  
DevSecOps • Python/Django • Sécurité applicative • Expert Fintech

- **GitHub** : [@g0sh5ukuna](https://github.com/g0sh5ukuna)
- **LinkedIn** : [joshsounon07](https://www.linkedin.com/in/joshsounon07/)

---

## ⭐ Remerciements

- Merci à la communauté **Tesseract OCR** pour cet outil open source exceptionnel
- Merci à la communauté **Django** pour ce framework puissant
- Merci à tous les **contributeurs** qui participent à l'amélioration continue de ce projet
- Merci à la communauté **open source** pour l'inspiration et le partage

---

## 🆘 Support

- 📖 **Documentation** : [docs/](docs/)
- 🐛 **Issues** : [GitHub Issues](https://github.com/g0sh5ukuna/img_to_txt_ocr/issues)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/g0sh5ukuna/img_to_txt_ocr/discussions)
- 📧 **Email** : [josh.sounon@gmail.com]

---

## 🙏 Star le projet

Si ce projet vous est utile, pensez à ⭐ **star** le projet sur GitHub pour montrer votre soutien !

---

**Fait avec ❤️ et Python par la communauté open source**
