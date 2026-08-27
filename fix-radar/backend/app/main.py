from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.competitors import router as competitors_router
from app.api.export import router as export_router
from app.api.integrations import router as integrations_router
from app.api.opportunities import router as opportunities_router
from app.api.opportunities import tasks_router
from app.api.simulator import router as simulator_router
from app.api.sites import router as sites_router
from app.core.config import get_settings
from app.database import Base, engine
from app import models  # noqa: F401 -- ensures all models are registered on Base before create_all

settings = get_settings()

app = FastAPI(title="OmniFit Website Fix Radar", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/api/health")
def health():
    return {"status": "ok"}


app.include_router(sites_router)
app.include_router(opportunities_router)
app.include_router(tasks_router)
app.include_router(competitors_router)
app.include_router(integrations_router)
app.include_router(simulator_router)
app.include_router(export_router)
