from backend.database.base import Base
from backend.database.database import engine
from backend.database.job_model import JobModel

Base.metadata.create_all(engine)
print("✅ Base de datos inicializada correctamente.")