"""
URL configuration for img_to_txt_ocr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

# API REST
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="OCR Tool API",
        default_version='v1',
        description="API REST pour l'outil OCR - Extraction de texte à partir d'images et PDF",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@ocrtool.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ocr-tools/', views.ocr_tools, name='ocr_tools'),
    path('ocr-result/<int:document_id>/', views.ocr_result, name='ocr_result'),
    path('download-text/<int:document_id>/', views.download_text, name='download_text'),
    path('history/', views.document_history, name='document_history'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # API REST
    path('api/v1/', include('api.urls')),
    
    # Documentation Swagger
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

# Servir les fichiers média en développement (les fichiers statiques sont gérés automatiquement)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
