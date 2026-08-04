from fastapi import FastAPI
from backend.services.job_service import JobService

app = FastAPI(title="JobHunter AI")


@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a JobHunter AI"}


@app.get("/empleos")
def obtener_empleos(fuente: str | None = None, empresa: str | None = None, modalidad: str | None = None, tag: str | None = None):
    service = JobService()
    return service.search(fuente=fuente, empresa=empresa, modalidad=modalidad, tag=tag)

@app.get("/empleos/todos")
def obtener_todos_los_empleos():
    service = JobService()
    return service.get_all()