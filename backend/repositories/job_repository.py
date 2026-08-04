from backend.database.database import SessionLocal
from backend.database.job_model import JobModel
from backend.models import job
from backend.models.job import Job

class JobRepository:

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

    def search(self,empresa: str | None = None,fuente: str|None = None, modalidad: str | None = None, tag: str | None = None) -> list[Job]:
        session = SessionLocal()
        try:
            query = session.query(JobModel)
            if empresa:
                query = query.filter_by(empresa=empresa)
            if fuente:
                query = query.filter_by(fuente=fuente)
            if modalidad:
                query = query.filter_by(modalidad=modalidad)
            if tag:
                query = query.filter(JobModel.tags.contains([tag]))
            job_models = query.all()
            return self._to_jobs(job_models)
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()