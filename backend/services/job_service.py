from backend.scrapers.remoteok import RemoteOKScraper
from backend.repositories.job_repository import JobRepository

class JobService:
    def __init__(self):
        self.scrapers = [RemoteOKScraper()]
        self.repository = JobRepository()

    def obtener_empleos(self):
        empleos =[]
        for scraper in self.scrapers:
            jobs = scraper.buscar_empleos()
            for job in jobs:
                self.repository.create(job)
            empleos.extend(jobs)
        return empleos