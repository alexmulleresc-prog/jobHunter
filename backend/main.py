from fastapi import FastAPI
from backend.api import scrapers, stats
from backend.api.jobs import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="JobHunter AI")
app.include_router(stats.router)
app.include_router(router)
app.include_router(scrapers.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
