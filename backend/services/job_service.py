from backend.scrapers.remoteok import RemoteOKScraper
from backend.scrapers.weworkremotely import WeWorkRemotelyScraper
from backend.repositories.job_repository import JobRepository
from backend.models import job
from backend.database.database import SessionLocal

class JobService:
    def __init__(self):
        self.scrapers = [WeWorkRemotelyScraper(), RemoteOKScraper()]
        self.repository = JobRepository()

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

    def get_by_fuente(self, fuente: str):
        return self.repository.get_by_fuente(fuente)

    def get_by_empresa(self, empresa: str):
        return self.repository.get_by_empresa(empresa)

    def get_by_modalidad(self, modalidad: str):
        return self.repository.get_by_modalidad(modalidad)

    def get_by_tag(self, tag: str):
        return self.repository.get_by_tag(tag)