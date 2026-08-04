from fastapi import FastAPI
from backend.api import scrapers, stats
from backend.api.jobs import router

app = FastAPI()
app.include_router(stats.router)
app.include_router(router)
app.include_router(scrapers.router)
