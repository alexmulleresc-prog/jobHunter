from backend.database.database import SessionLocal
from backend.database.job_model import JobModel
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
                empresa_logo=job.empresa_logo
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