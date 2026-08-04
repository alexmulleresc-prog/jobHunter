from fastapi import APIRouter
from backend.services.job_service import JobService

router = APIRouter()

@router.get("/scrapers/run")
def ejecutar_scraper():
    print("Ejecutando scrapers...")
    service = JobService()
    return service.ejecutar_scraper()
