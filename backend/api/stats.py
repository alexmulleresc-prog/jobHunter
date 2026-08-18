from fastapi import APIRouter
from backend.services.job_service import JobService

router = APIRouter()

@router.get("/stats")
def obtener_estadisticas():
    service = JobService()
    update_info = service._get_update_info()
    return {
        "total_jobs": service.get_total_jobs_count(),
        "total_companies": service.get_total_companies_count(),
        "sources": service.get_jobs_by_source(),
        "top_companies": service.get_top_companies(),
        "last_update": update_info["last_update"],
        "last_new_jobs": update_info["last_new_jobs"]
        }