import pytesseract
from typing import Dict, Optional
from PIL import Image
from django.conf import settings
from .base_engine import BaseOCREngine


class TesseractEngine(BaseOCREngine):
    """Moteur OCR utilisant Tesseract"""
    
    # Mapping des langues (codes Django -> codes Tesseract)
    LANGUAGE_MAP = {
        'fr': 'fra',
        'en': 'eng',
        'fr-fr': 'fra',
        'en-us': 'eng',
        'fra': 'fra',
        'eng': 'eng',
    }
    
    # Langues supportées par défaut
    DEFAULT_LANGUAGES = ['fra', 'eng']
    
    def __init__(self):
        """Initialise le moteur Tesseract"""
        self._tesseract_cmd = getattr(settings, 'TESSERACT_CMD', None)
        if self._tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = self._tesseract_cmd
        
        # Langues configurées dans settings
        configured_langs = getattr(settings, 'TESSERACT_LANGUAGES', [])
        if configured_langs:
            self._supported_languages = list(configured_langs)
        else:
            self._supported_languages = self.DEFAULT_LANGUAGES.copy()
    
    @property
    def name(self) -> str:
        """Nom du moteur"""
        return 'tesseract'
    
    def is_available(self) -> bool:
        """Vérifie si Tesseract est disponible"""
        try:
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False
    
    def get_supported_languages(self) -> list:
        """Retourne la liste des langues supportées"""
        return self._supported_languages.copy()
    
    def _normalize_language(self, language: Optional[str] = None) -> str:
        """Normalise le code langue pour Tesseract"""
        if not language:
            # Utilise la langue par défaut du projet ou 'fra+eng'
            default_lang = getattr(settings, 'LANGUAGE_CODE', 'fr')
            language = self.LANGUAGE_MAP.get(default_lang, 'fra')
        
        # Convertit le code si nécessaire
        language = self.LANGUAGE_MAP.get(language.lower(), language.lower())
        
        # Vérifie si la langue est supportée
        if language not in self._supported_languages:
            # Utilise la première langue disponible
            language = self._supported_languages[0] if self._supported_languages else 'fra'
        
        return language
    
    def extract_text(
        self,
        image: Image.Image,
        language: Optional[str] = None,
        **kwargs
    ) -> Dict[str, any]:
        """
        Extrait le texte d'une image avec Tesseract
        
        Args:
            image: Image PIL à traiter
            language: Code langue (ex: 'fra', 'eng')
            **kwargs: Options supplémentaires
            
        Returns:
            Dict avec text, confidence, language
        """
        if not self.is_available():
            raise RuntimeError("Tesseract n'est pas disponible sur ce système")
        
        # Normalise la langue
        tesseract_lang = self._normalize_language(language)
        
        # Configuration Tesseract
        config = kwargs.get('config', '')
        
        try:
            # Extraction du texte
            text = pytesseract.image_to_string(image, lang=tesseract_lang, config=config)
            
            # Extraction des données avec confiance
            data = pytesseract.image_to_data(image, lang=tesseract_lang, output_type=pytesseract.Output.DICT)
            
            # Calcul de la confiance moyenne
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return {
                'text': text.strip(),
                'confidence': round(avg_confidence, 2),
                'language': tesseract_lang,
            }
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'extraction OCR: {str(e)}")
