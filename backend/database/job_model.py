from datetime import datetime
from backend.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

class JobModel(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column()
    empresa: Mapped[str] = mapped_column()
    ubicacion: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    fecha_publicacion: Mapped[datetime | None] = mapped_column()
    fecha_scraping: Mapped[datetime] = mapped_column()
    descripcion: Mapped[str | None] = mapped_column()
    tipo_empleo: Mapped[str | None] = mapped_column()
    modalidad: Mapped[str | None] = mapped_column()
    salario: Mapped[str | None] = mapped_column()
    empresa_logo: Mapped[str | None] = mapped_column()
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    fuente: Mapped[str] = mapped_column()