from fastapi import APIRouter
from backend.services.job_service import JobService

router = APIRouter()

@router.get("/empleos")
def obtener_empleos(fuente: str | None = None,
                    empresa: str | None = None,
                    modalidad: str | None = None,
                    tag: str | None = None,
                    search: str | None = None,
                    orden: str = "recientes",
                    limit: int = 25,
                    offset: int = 0):
    service = JobService()
    jobs = service.search(fuente=fuente, empresa=empresa, modalidad=modalidad, tag=tag, search=search,orden=orden, limit=limit, offset=offset)
    total = service.count_search(fuente=fuente,empresa=empresa,modalidad=modalidad,tag=tag,search=search)
    return{"jobs":jobs,
           "total":total}

@router.get("/empleos/nuevos")
def obtener_nuevos_empleos():
    service = JobService()
    return service.get_new_jobs()

@router.get("/empleos/todos")
def obtener_todos_los_empleos():
    service = JobService()
    return service.get_all()

@router.get("/filters")
def get_filters():
    service = JobService()
    return service.get_filters()