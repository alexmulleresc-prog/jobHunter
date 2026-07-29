from fastapi import FastAPI
from backend.services.job_service import JobService

app = FastAPI(title="JobHunter AI")


@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a JobHunter AI"}


@app.get("/empleos")
def obtener_empleos():
    service = JobService()
    return service.obtener_empleos()

