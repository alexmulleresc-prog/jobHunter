from backend.scrapers.remoteok import RemoteOKScraper
from backend.scrapers.weworkremotely import WeWorkRemotelyScraper
from backend.repositories.job_repository import JobRepository
from backend.models import job
from backend.database.database import SessionLocal

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
               limit: int = 100,
               offset: int = 0):
        return self.repository.search(fuente=fuente, empresa=empresa, modalidad=modalidad, tag=tag, limit=limit, offset=offset)
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
        return {"mensaje": f"Scrapers ejecutados. Se encontraron {len(empleos)} empleos nuevos. Se agregaron {empleos_agregados} empleos a la base de datos."}