from backend.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class JobModel(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column()
    empresa: Mapped[str] = mapped_column()
    ubicacion: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()