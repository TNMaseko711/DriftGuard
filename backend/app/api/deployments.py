from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.models.schemas import DeploymentCreate
from backend.app.services.deployment_service import deployment_service

router = APIRouter(prefix="/api/deployments", tags=["deployments"])


class StatusUpdate(BaseModel):
    status: str


@router.post("")
def create_deployment(payload: DeploymentCreate):
    return deployment_service.create(payload)


@router.get("")
def list_deployments():
    return deployment_service.list_all()


@router.put("/{deployment_id}/status")
def update_deployment(deployment_id: UUID, payload: StatusUpdate):
    try:
        return deployment_service.update_status(deployment_id, payload.status)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
