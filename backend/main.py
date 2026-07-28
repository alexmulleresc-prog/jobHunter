from fastapi import FastAPI
from backend.scrapers.remoteok import buscar_empleos

app = FastAPI(title="JobHunter AI")


@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a JobHunter AI"}


@app.get("/empleos")
def obtener_empleos():
    return buscar_empleos()

