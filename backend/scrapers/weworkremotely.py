from datetime import datetime
from bs4 import BeautifulSoup
from backend.services.browser_service import obtener_html
from backend.models.job import Job


class WeWorkRemotelyScraper:
    URL = "https://weworkremotely.com/remote-jobs"
    
    def buscar_empleos(self):
        html = obtener_html(self.URL)
        return self._extraer_empleos(html)

    def _extraer_empleos(self, html):
        soup = BeautifulSoup(html, "html.parser")
        filas = soup.find_all("li", class_="new-listing-container")
        print(f"Se encontraron {len(filas)} empleos en WeWorkRemotely.")
        empleos = []
        for fila in filas:
            #URL
            link = fila.find("a", class_="listing-link--unlocked")
            url =("https://weworkremotely.com" + link["href"]
                     if link and link.get("href") else "")
            #Datos Basicos
            titulo = fila.find("span", class_="new-listing__header__title__text")
            empresa = fila.find("p", class_="new-listing__company-name")
            ubicacion = fila.find("p", class_="new-listing__company-headquarters")
            # Logo
            logo = fila.find("img")
            empresa_logo = logo["src"] if logo else None
            # Salario
            #salario = fila.find("div", class_="salary")
            #salario = salario.text.strip() if salario else None
            # Fecha publicación
            time = fila.find("p", class_="new-listing__header__icons__date")
            fecha_publicacion = (
                datetime.fromisoformat(time["datetime"])
                if time and time.get("datetime")
                else None)
            # Tags y categorias
            categorias = fila.find_all(
                "p",
                class_="new-listing__categories__category"
            )
            tags = [
                categoria.text.strip()
                for categoria in categorias
            ]
            modalidad = tags[1] if len(tags) > 1 else None
        
            empleo = Job(
                titulo=titulo.text.strip() if titulo else "",
                empresa=empresa.text.strip() if empresa else "",
                ubicacion=ubicacion.text.strip() if ubicacion else "",
                url=url,
                fecha_publicacion=None,      # la completaremos más adelante
                fecha_scraping=datetime.now(),
                descripcion=None,
                modalidad=modalidad,
                salario=None,
                empresa_logo=empresa_logo,
                tags=tags,
                fuente="We Work Remotely",
            )
            empleos.append(empleo)
        return empleos