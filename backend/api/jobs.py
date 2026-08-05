from fastapi import APIRouter
from backend.services.job_service import JobService

router = APIRouter()

@router.get("/empleos")
def obtener_empleos(fuente: str | None = None,
                    empresa: str | None = None,
                    modalidad: str | None = None,
                    tag: str | None = None,
                    search: str | None = None,
                    limit: int = 100,
                    offset: int = 0):
    service = JobService()
    return service.search(fuente=fuente, empresa=empresa, modalidad=modalidad, tag=tag, search=search, limit=limit, offset=offset)

@router.get("/empleos/todos")
def obtener_todos_los_empleos():
    service = JobService()
    return service.get_all()