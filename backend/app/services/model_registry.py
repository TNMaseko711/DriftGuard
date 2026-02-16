from __future__ import annotations

from datetime import datetime
from uuid import UUID

from backend.app.models.schemas import ModelCreate, ModelRecord, ModelVersionCreate, ModelVersionRecord, Stage
from backend.app.services.store import store


class ModelRegistryService:
    def create_model(self, payload: ModelCreate) -> ModelRecord:
        record = ModelRecord(version="0.0.0", **payload.model_dump())
        store.models[str(record.id)] = record
        return record

    def list_models(self) -> list[ModelRecord]:
        return list(store.models.values())

    def create_version(self, model_id: UUID, payload: ModelVersionCreate) -> ModelVersionRecord:
        if str(model_id) not in store.models:
            raise KeyError("model not found")
        version = ModelVersionRecord(model_id=model_id, **payload.model_dump())
        store.model_versions[str(model_id)][payload.version] = version
        return version

    def list_versions(self, model_id: UUID) -> list[ModelVersionRecord]:
        return list(store.model_versions[str(model_id)].values())

    def promote_version(self, model_id: UUID, version: str, stage: Stage, promoted_by: str) -> ModelVersionRecord:
        model_versions = store.model_versions[str(model_id)]
        if version not in model_versions:
            raise KeyError("version not found")
        target = model_versions[version]
        target.stage = stage
        target.promoted_at = datetime.utcnow()
        target.promoted_by = promoted_by
        return target


model_registry_service = ModelRegistryService()
