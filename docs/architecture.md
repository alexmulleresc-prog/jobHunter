# JobHunter AI - Arquitectura

## Objetivo del proyecto

Breve descripción del proyecto.

---

## Estructura de carpetas

backend/
├── api/
├── config/
├── database/
├── models/
├── repositories/
├── scrapers/
├── services/

Explicación de la responsabilidad de cada carpeta.

---

## Flujo de la aplicación

Scraper
    ↓
Job (modelo de dominio)
    ↓
JobRepository
    ↓
JobModel (SQLAlchemy)
    ↓
PostgreSQL

---

## Convenciones

- Imports absolutos usando `backend`.
- Un modelo de dominio nunca depende de SQLAlchemy.
- Los scrapers no escriben en la base de datos.
- Los repositories son la única capa que accede a la base.
- Los services coordinan el flujo de trabajo.
- Cada clase debe tener una única responsabilidad.

---

## Tecnologías

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Playwright
- BeautifulSoup