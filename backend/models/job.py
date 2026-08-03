from datetime import datetime
from pydantic import BaseModel

class Job(BaseModel):
    titulo: str
    empresa: str
    ubicacion: str
    url: str
    fecha_publicacion: datetime | None = None
    fecha_scraping: datetime = datetime.now()
    descripcion: str | None = None
    tipo_empleo: str | None = None
    modalidad: str | None = None
    salario: str | None = None
    empresa_logo: str | None = None