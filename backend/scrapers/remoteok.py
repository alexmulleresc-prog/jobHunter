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
            #URL
            link = fila.find("a", itemprop="url")
            url = self.URL + link["href"] if link and link.get("href") else ""
            #Datos Basicos
            titulo = fila.find("h2")
            empresa = fila.find("span", itemprop="hiringOrganization")
            ubicacion = fila.find(class_="location")
            # Logo
            logo = fila.find("img", class_="logo")
            empresa_logo = logo["src"] if logo else None
            # Salario
            salario = fila.find("div", class_="salary")
            salario = salario.text.strip() if salario else None
            # Fecha publicación
            time = fila.find("time")
            fecha_publicacion = (
                datetime.fromisoformat(time["datetime"])
                if time and time.get("datetime")
                else None)
            # Tags
            tags = [
                tag.get("aria-label")
                for tag in fila.select("td.tags a")]
            # Descripción
            expand = fila.find_next_sibling("tr")
            descripcion = None
            if expand:
                descripcion_div = expand.find("div", class_="html")
                if descripcion_div:
                    descripcion = descripcion_div.get_text(" ", strip=True)

            empleo = Job(
                titulo=titulo.text.strip() if titulo else "",
                empresa=empresa.text.strip() if empresa else "",
                ubicacion=ubicacion.text.strip() if ubicacion else "",
                url=url,
                fecha_publicacion=fecha_publicacion,
                fecha_scraping=datetime.now(),
                descripcion=descripcion,
                tipo_empleo=None,
                modalidad=ubicacion.text.strip() if ubicacion else None,
                salario=salario,
                empresa_logo=empresa_logo,
                tags=tags,
                fuente="RemoteOK"
            )
            empleos.append(empleo)
        return empleos