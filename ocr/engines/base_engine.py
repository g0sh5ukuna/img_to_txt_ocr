from abc import ABC, abstractmethod
from typing import Dict, Optional
from PIL import Image


class BaseOCREngine(ABC):
    """Interface de base pour les moteurs OCR"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nom du moteur OCR"""
        pass
    
    @abstractmethod
    def extract_text(
        self,
        image: Image.Image,
        language: Optional[str] = None,
        **kwargs
    ) -> Dict[str, any]:
        """
        Extrait le texte d'une image
        
        Args:
            image: Image PIL à traiter
            language: Code langue (ex: 'fra', 'eng')
            **kwargs: Options supplémentaires spécifiques au moteur
            
        Returns:
            Dict avec les clés:
            - text: Texte extrait
            - confidence: Score de confiance (0-100)
            - language: Langue détectée/utilisée
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Vérifie si le moteur est disponible"""
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> list:
        """Retourne la liste des langues supportées"""
        pass
