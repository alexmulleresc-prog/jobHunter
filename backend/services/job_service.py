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

    def search(self, fuente: str | None = None, empresa: str | None = None, modalidad: str | None = None, tag: str | None = None):
        return self.repository.search(fuente=fuente, empresa=empresa, modalidad=modalidad, tag=tag)