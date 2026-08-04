from fastapi import FastAPI
from backend.services.job_service import JobService

app = FastAPI(title="JobHunter AI")


@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a JobHunter AI"}


@app.get("/empleos")
def obtener_empleos(fuente: str | None = None, empresa: str | None = None, modalidad: str | None = None, tag: str | None = None):
    service = JobService()
    if fuente:
        return service.get_by_fuente(fuente)
    elif empresa:
        return service.get_by_empresa(empresa)
    elif modalidad:
        return service.get_by_modalidad(modalidad)
    elif tag:
        return service.get_by_tag(tag)
    return service.obtener_empleos()

@app.get("/empleos/todos")
def obtener_todos_los_empleos():
    service = JobService()
    return service.get_all()