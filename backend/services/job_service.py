from backend.scrapers.remoteok import RemoteOKScraper
from backend.scrapers.weworkremotely import WeWorkRemotelyScraper
from backend.repositories.job_repository import JobRepository
from backend.models import job
from backend.database.database import SessionLocal
import json
from pathlib import Path
from datetime import datetime

UPDATE_INFO_PATH = Path("backend/data/update_info.json")

class JobService:
    def __init__(self):
        self.scrapers = [WeWorkRemotelyScraper(), RemoteOKScraper()]
        self.repository = JobRepository()
##### FUNCIONES PRINCIPALES #####
    def obtener_empleos(self):
        empleos =[]
        for scraper in self.scrapers:
            jobs = scraper.buscar_empleos()
            for job in jobs:
                if not self.repository.exists(job.url):
                    self.repository.create(job)
            empleos.extend(jobs)
        return empleos

    def get_all(self):
        return self.repository.get_all()

    def search(self,
               fuente: str | None = None,
               empresa: str | None = None,
               modalidad: str | None = None,
               tag: str | None = None,
               search: str | None = None,
               limit: int = 100,
               offset: int = 0):
        return self.repository.search(fuente=fuente, empresa=empresa, modalidad=modalidad, tag=tag, search=search, limit=limit, offset=offset)
#### FUNCION DE FILTROS ###
    def get_filters(self):
        return {
            "companies": self.repository.get_top_companies(limit=50),
            "sources": self.repository.get_jobs_by_source()
    }
    
#### FUNCIONES DE ESTADISTICAS ###
    def get_total_jobs_count(self) -> int:
        return self.repository.get_total_jobs()

    def get_jobs_by_source(self) -> dict[str, int]:
        return self.repository.get_jobs_by_source()

    def get_top_companies(self, limit: int = 10) -> list[dict[str, str|int]]:
        return self.repository.get_top_companies(limit)

    def get_total_companies_count(self) -> int:
        return self.repository.get_total_companies_count()
#### FUNCIONES DE EJECUCION DE SCRAPERS ###
    def ejecutar_scraper(self):
        empleos = []
        empleos_agregados = 0
        for scraper in self.scrapers:
            jobs = scraper.buscar_empleos()
            for job in jobs:
                if not self.repository.exists(job.url):
                    self.repository.create(job)
                    empleos_agregados += 1
            empleos.extend(jobs)
        self._save_update_info(empleos_agregados)
        return {"status": "success", "jobs_found": len(empleos), "new_jobs": empleos_agregados, "total_jobs": self.get_total_jobs_count()}

    def _save_update_info(self, new_jobs):
        data = {
            "last_update": datetime.now().isoformat(),
            "last_new_jobs": new_jobs
        }
        with open(UPDATE_INFO_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def _get_update_info(self):
        if not UPDATE_INFO_PATH.exists():
            return {
                "last_update": None,
                "last_new_jobs": 0
            }
        with open(UPDATE_INFO_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
