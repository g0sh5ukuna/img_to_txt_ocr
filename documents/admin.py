from django.contrib import admin
from documents.models import Document, OCRResult


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'user', 'status', 'uploaded_at', 'confidence_score']
    list_filter = ['status', 'uploaded_at', 'engine_used']
    search_fields = ['file_name', 'user__username']
    readonly_fields = ['uploaded_at', 'processed_at']
    date_hierarchy = 'uploaded_at'


@admin.register(OCRResult)
class OCRResultAdmin(admin.ModelAdmin):
    list_display = ['document', 'language_detected', 'confidence_score', 'word_count', 'created_at']
    list_filter = ['language_detected', 'engine_used', 'created_at']
    search_fields = ['document__file_name']
    readonly_fields = ['created_at']
