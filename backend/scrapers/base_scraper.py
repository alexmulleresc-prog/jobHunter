from abc import ABC, abstractmethod
from backend.models.job import Job
from backend.services.browser_service import obtener_html

class BaseScraper(ABC):
    URL = ""

    def buscar_empleos(self) -> list[Job]:
        html = obtener_html(self.URL)
        return self._extraer_empleos(html)
    
    @abstractmethod
    def _extraer_empleos(self, html: str) -> list[Job]:
        pass