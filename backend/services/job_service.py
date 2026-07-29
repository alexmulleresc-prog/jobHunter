from backend.scrapers.remoteok import RemoteOKScraper

class JobService:
    def __init__(self):
        self.scrapers = [RemoteOKScraper()]

    def obtener_empleos(self):
        empleos =[]
        for scraper in self.scrapers:
            empleos.extend(scraper.buscar_empleos())
        return empleos