from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.models.schemas import ExperimentCreate, RunCreate, RunStatus
from backend.app.services.experiment_service import experiment_service

router = APIRouter(prefix="/api/experiments", tags=["experiments"])


class MetricsRequest(BaseModel):
    metrics: dict[str, float]
    step: int


class CompleteRunRequest(BaseModel):
    status: RunStatus = RunStatus.completed


@router.post("")
def create_experiment(payload: ExperimentCreate):
    return experiment_service.create_experiment(payload)


@router.get("")
def list_experiments():
    return experiment_service.list_experiments()


@router.post("/runs")
def create_run(payload: RunCreate):
    try:
        return experiment_service.create_run(payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/runs/{run_id}/metrics")
def log_metrics(run_id: UUID, payload: MetricsRequest):
    try:
        return experiment_service.log_metrics(run_id, payload.metrics, payload.step)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put("/runs/{run_id}/complete")
def complete_run(run_id: UUID, payload: CompleteRunRequest):
    try:
        return experiment_service.complete_run(run_id, payload.status)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
