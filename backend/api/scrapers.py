from fastapi import APIRouter
from backend.services.job_service import JobService

router = APIRouter()

@router.post("/scrapers/run")
def ejecutar_scraper():
    service = JobService()
    return service.ejecutar_scraper()
