from __future__ import annotations

from fastapi import FastAPI

from backend.app.api.ab_testing import router as ab_router
from backend.app.api.deployments import router as deployment_router
from backend.app.api.experiments import router as experiment_router
from backend.app.api.models import router as model_router
from backend.app.api.monitoring import router as monitoring_router

app = FastAPI(title="DriftGuard MLOps", version="0.1.0")

app.include_router(model_router)
app.include_router(experiment_router)
app.include_router(deployment_router)
app.include_router(ab_router)
app.include_router(monitoring_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
