from backend.scrapers.remoteok import RemoteOKScraper
from backend.repositories.job_repository import JobRepository
from backend.models import job
from backend.database.database import SessionLocal

class JobService:
    def __init__(self):
        self.scrapers = [RemoteOKScraper()]
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