from backend.models.job import Job
from backend.repositories.job_repository import JobRepository

print("1")

job = Job(
    titulo="Python Developer",
    empresa="OpenAI",
    ubicacion="Remote",
    url="https://ejemplo.com"
)

print("2")

repository = JobRepository()

print("3")

repository.create(job)

print("4")