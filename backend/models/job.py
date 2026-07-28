from pydantic import BaseModel

class Job(BaseModel):
    titulo: str
    empresa: str
    ubicacion: str
    url: str
