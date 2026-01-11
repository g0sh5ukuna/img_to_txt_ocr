"""
URLs pour l'API REST
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet, basename='document')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
