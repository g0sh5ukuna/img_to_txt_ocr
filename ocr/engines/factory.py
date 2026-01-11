from django.conf import settings
from typing import Optional
from .base_engine import BaseOCREngine
from .tesseract_engine import TesseractEngine


class OCREngineFactory:
    """Factory pour créer des instances de moteurs OCR"""
    
    _engines = {
        'tesseract': TesseractEngine,
        # Ajouter d'autres moteurs ici (EasyOCR, etc.)
    }
    
    @classmethod
    def get_engine(cls, engine_name: Optional[str] = None) -> BaseOCREngine:
        """
        Crée une instance de moteur OCR
        
        Args:
            engine_name: Nom du moteur ('tesseract', etc.)
                        Si None, utilise le moteur par défaut
        
        Returns:
            Instance du moteur OCR
        
        Raises:
            ValueError: Si le moteur n'est pas disponible
        """
        if engine_name is None:
            # Utilise le moteur par défaut (tesseract)
            engine_name = 'tesseract'
        
        engine_name = engine_name.lower()
        
        if engine_name not in cls._engines:
            available = ', '.join(cls._engines.keys())
            raise ValueError(f"Moteur '{engine_name}' non disponible. Moteurs disponibles: {available}")
        
        engine_class = cls._engines[engine_name]
        engine = engine_class()
        
        if not engine.is_available():
            raise RuntimeError(f"Le moteur '{engine_name}' n'est pas disponible sur ce système")
        
        return engine
    
    @classmethod
    def get_default_engine(cls) -> BaseOCREngine:
        """Retourne le moteur OCR par défaut"""
        return cls.get_engine('tesseract')
    
    @classmethod
    def get_available_engines(cls) -> list:
        """Retourne la liste des moteurs disponibles"""
        available = []
        for name, engine_class in cls._engines.items():
            try:
                engine = engine_class()
                if engine.is_available():
                    available.append(name)
            except Exception:
                pass
        return available
