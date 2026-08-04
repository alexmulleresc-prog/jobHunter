from sqlalchemy import func
from backend.database.database import SessionLocal
from backend.database.job_model import JobModel
from backend.models import job
from backend.models.job import Job

class JobRepository:

######## ESCRIBIR EN LA BASE DE DATOS ########
    def create(self, job: Job):
        session = SessionLocal()
        try:
            job_model = JobModel(
                titulo=job.titulo,
                empresa=job.empresa,
                ubicacion=job.ubicacion,
                url=job.url,
                fecha_publicacion=job.fecha_publicacion,
                fecha_scraping=job.fecha_scraping,
                descripcion=job.descripcion,
                tipo_empleo=job.tipo_empleo,
                modalidad=job.modalidad,
                salario=job.salario,
                empresa_logo=job.empresa_logo,
                tags=job.tags,
                fuente=job.fuente
            )
            session.add(job_model)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

######## CONSULTAS ########
    def exists(self, url: str) -> bool:
        session = SessionLocal()
        try:
            job=session.query(JobModel).filter_by(url=url).first()
            return job is not None
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _to_job(self, job_model: JobModel) -> Job:
        return Job(
            titulo=job_model.titulo,
            empresa=job_model.empresa,
            ubicacion=job_model.ubicacion,
            url=job_model.url,
            fecha_publicacion=job_model.fecha_publicacion,
            fecha_scraping=job_model.fecha_scraping,
            descripcion=job_model.descripcion,
            tipo_empleo=job_model.tipo_empleo,
            modalidad=job_model.modalidad,
            salario=job_model.salario,
            empresa_logo=job_model.empresa_logo,
            tags=job_model.tags,
            fuente=job_model.fuente
        )

    def _to_jobs(self, job_models: list[JobModel]) -> list[Job]:
        return [self._to_job(job) for job in job_models]


    def get_all(self)->list[Job]:
        session = SessionLocal()
        try:
            job_models = session.query(JobModel).all()
            return self._to_jobs(job_models)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def search(self,empresa: str | None = None,
               fuente: str|None = None, 
               modalidad: str | None = None, 
               tag: str | None = None, 
               limit: int = 100, 
               offset: int = 0,) -> list[Job]:
        session = SessionLocal()
        try:
            query = session.query(JobModel)
            if empresa:
                query = query.filter(JobModel.empresa.ilike(f"%{empresa}%"))
            if fuente:
                query = query.filter(JobModel.fuente.ilike(f"%{fuente}%"))
            if modalidad:
                query = query.filter(JobModel.modalidad.ilike(f"%{modalidad}%"))
            if tag:
                query = query.filter(JobModel.tags.contains([tag]))
            query = query.offset(offset)
            query = query.limit(limit)
            job_models = query.all()
            return self._to_jobs(job_models)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

######## ESTADISTICAS ########
    def get_total_jobs(self) -> int:
        session = SessionLocal()
        try:
            total_jobs = session.query(JobModel).count()
            return total_jobs
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_jobs_by_source(self) -> dict[str, int]:
        session = SessionLocal()
        try:
            result = session.query(JobModel.fuente, func.count(JobModel.id)).group_by(JobModel.fuente).all()
            return {fuente: count for fuente, count in result}
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_top_companies(self, limit: int = 10) -> list[dict[str, str|int]]:
        session = SessionLocal()
        try:
            result = session.query(JobModel.empresa, func.count(JobModel.id)).group_by(JobModel.empresa).order_by(func.count(JobModel.id).desc()).limit(limit).all()
            return [{"empresa": empresa, "empleos": count} for empresa, count in result]
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_total_companies_count(self) -> int:
        session = SessionLocal()
        try:
            total_companies = session.query(JobModel.empresa).distinct().count()
            return total_companies
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()