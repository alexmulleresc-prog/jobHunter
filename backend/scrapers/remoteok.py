from bs4 import BeautifulSoup
from backend.services.browser_service import obtener_html
from backend.models.job import Job

def buscar_empleos():
    html = obtener_html("https://remoteok.com")
    soup = BeautifulSoup(html, "html.parser")
    filas = soup.find_all("tr", class_="job")
    print(f"Se encontraron {len(filas)} empleos en RemoteOK.")
    empleos = []
    for fila in filas:
        link = fila.find("a", itemprop="url")
        url =""
        if link and link.get("href"):
            url = "https://remoteok.com" + link["href"]
        titulo = fila.find("h2")
        empresa = fila.find("span", itemprop="hiringOrganization")
        ubicacion = fila.find(class_="location")
        empleo = Job(
            titulo=titulo.text.strip() if titulo else "",
            empresa=empresa.text.strip() if empresa else "",
            ubicacion=ubicacion.text.strip() if ubicacion else "",
            url=url
        )
        empleos.append(empleo)
    return empleos