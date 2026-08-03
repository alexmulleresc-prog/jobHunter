from datetime import datetime
from bs4 import BeautifulSoup
from backend.services.browser_service import obtener_html
from backend.models.job import Job
from backend.scrapers.base_scraper import BaseScraper

class RemoteOKScraper(BaseScraper):
    URL = "https://remoteok.com"
    
    def buscar_empleos(self):
        html = obtener_html(self.URL)
        return self._extraer_empleos(html)

    def _extraer_empleos(self, html):
        soup = BeautifulSoup(html, "html.parser")
        filas = soup.find_all("tr", class_="job")
        print(f"Se encontraron {len(filas)} empleos en RemoteOK.")
        empleos = []
        for fila in filas:
            link = fila.find("a", itemprop="url")
            url = ""
            if link and link.get("href"):
                url = self.URL + link["href"]
            titulo = fila.find("h2")
            empresa = fila.find("span", itemprop="hiringOrganization")
            ubicacion = fila.find(class_="location")
            empleo = Job(
                titulo=titulo.text.strip() if titulo else "",
                empresa=empresa.text.strip() if empresa else "",
                ubicacion=ubicacion.text.strip() if ubicacion else "",
                url=url,
                fecha_publicacion=None,
                fecha_scraping=datetime.now(),
                descripcion=None,
                tipo_empleo=None,
                modalidad=None,
                salario=None,
                empresa_logo=None
            )
            empleos.append(empleo)
        return empleos