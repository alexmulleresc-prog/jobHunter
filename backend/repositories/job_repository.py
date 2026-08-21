from sqlalchemy import func, or_
from backend.database.database import SessionLocal
from backend.database.job_model import JobModel
from backend.models import job
from backend.models.job import Job
from datetime import datetime, timedelta

MAX_JOB_AGE_DAYS = 15

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
               search: str | None = None,
               orden: str = "recientes",
               limit: int = 100, 
               offset: int = 0,) -> list[Job]:
        session = SessionLocal()
        try:
            query = session.query(JobModel)
            fecha_limite = datetime.now() - timedelta(days=MAX_JOB_AGE_DAYS)
            query = query.filter(JobModel.fecha_scraping >= fecha_limite)
            if empresa:
                query = query.filter(JobModel.empresa.ilike(f"%{empresa}%"))
            if fuente:
                query = query.filter(JobModel.fuente.ilike(f"%{fuente}%"))
            if modalidad:
                query = query.filter(JobModel.modalidad.ilike(f"%{modalidad}%"))
            if tag:
                query = query.filter(JobModel.tags.contains([tag]))
            if search:
                query = query.filter(or_(JobModel.titulo.ilike(f"%{search}%"),JobModel.empresa.ilike(f"%{search}%"),))
            if orden == "recientes":
                query = query.order_by(JobModel.fecha_scraping.desc())
            elif orden == "antiguos":
                query = query.order_by(JobModel.fecha_scraping.asc())
            elif orden == "titulo_az":
                query = query.order_by(func.lower(func.trim(JobModel.titulo)).asc())
            elif orden == "titulo_za":
                query = query.order_by(func.lower(func.trim(JobModel.titulo)).desc())
            elif orden == "empresa_az":
                query = query.order_by(func.lower(func.trim(JobModel.empresa)).asc())
            elif orden == "empresa_za":
                query = query.order_by(func.lower(func.trim(JobModel.empresa)).desc())
            query = query.offset(offset)
            query = query.limit(limit)
            job_models = query.all()
            return self._to_jobs(job_models)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def count_search(self,
                     empresa :str | None = None,
                     fuente: str|None = None, 
                     modalidad: str | None = None, 
                     tag: str | None = None,
                     search: str | None = None) -> int:
        session = SessionLocal()
        try:
            query = session.query(JobModel)
            fecha_limite = datetime.now() - timedelta(days=MAX_JOB_AGE_DAYS)
            query = query.filter(JobModel.fecha_scraping >= fecha_limite)
            if empresa:
                query = query.filter(JobModel.empresa.ilike(f"%{empresa}%"))
            if fuente:
                query = query.filter(JobModel.fuente.ilike(f"%{fuente}%"))
            if modalidad:
                query = query.filter(JobModel.modalidad.ilike(f"%{modalidad}%"))
            if tag:
                query = query.filter(JobModel.tags.contains([tag]))
            if search:
                query = query.filter(or_(JobModel.titulo.ilike(f"%{search}%"),JobModel.empresa.ilike(f"%{search}%"),))
            return query.count()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_jobs_by_urls(self, urls: list[str]) -> list[Job]:
        session = SessionLocal()
        try:
            if not urls:
                return []
            job_models = (
                session.query(JobModel)
                .filter(JobModel.url.in_(urls))
                .all())
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
            fecha_limite = datetime.now() - timedelta(days=MAX_JOB_AGE_DAYS)
            return (session.query(JobModel).filter(JobModel.fecha_scraping >= fecha_limite).count())
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_jobs_by_source(self) -> dict[str, int]:
        session = SessionLocal()
        try:
            fecha_limite = datetime.now() - timedelta(days=MAX_JOB_AGE_DAYS)
            result = (session.query(JobModel.fuente, func.count(JobModel.id)).filter(JobModel.fecha_scraping >= fecha_limite)
                      .group_by(JobModel.fuente).all())
            return [{"name": fuente, "count": count}for fuente, count in result]
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_top_companies(self, limit: int = 10) -> list[dict[str, str|int]]:
        session = SessionLocal()
        try:
            fecha_limite = datetime.now() - timedelta(days=MAX_JOB_AGE_DAYS)
            result = (session.query(JobModel.empresa, func.count(JobModel.id)).filter(JobModel.fecha_scraping >= fecha_limite)
                        .group_by(JobModel.empresa).order_by(func.count(JobModel.id).desc()).limit(limit).all())
            return [{"name": empresa, "count": count} for empresa, count in result]
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_total_companies_count(self) -> int:
        session = SessionLocal()
        try:
            fecha_limite = datetime.now() - timedelta(days=MAX_JOB_AGE_DAYS)
            total_companies = (session.query(JobModel.empresa).filter(JobModel.fecha_scraping >= fecha_limite).distinct().count())
            return total_companies
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()