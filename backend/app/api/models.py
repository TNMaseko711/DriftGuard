from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.models.schemas import ModelCreate, ModelVersionCreate, Stage
from backend.app.services.model_registry import model_registry_service

router = APIRouter(prefix="/api/models", tags=["models"])


class PromoteRequest(BaseModel):
    stage: Stage
    promoted_by: str


@router.post("")
def create_model(payload: ModelCreate):
    return model_registry_service.create_model(payload)


@router.get("")
def list_models():
    return model_registry_service.list_models()


@router.post("/{model_id}/versions")
def create_version(model_id: UUID, payload: ModelVersionCreate):
    try:
        return model_registry_service.create_version(model_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{model_id}/versions")
def list_versions(model_id: UUID):
    return model_registry_service.list_versions(model_id)


@router.put("/{model_id}/versions/{version}/stage")
def promote_version(model_id: UUID, version: str, payload: PromoteRequest):
    try:
        return model_registry_service.promote_version(model_id, version, payload.stage, payload.promoted_by)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
