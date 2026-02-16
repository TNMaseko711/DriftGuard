from __future__ import annotations

from uuid import UUID

from backend.app.models.schemas import DeploymentCreate, DeploymentRecord
from backend.app.services.store import store


class DeploymentService:
    def create(self, payload: DeploymentCreate) -> DeploymentRecord:
        deployment = DeploymentRecord(**payload.model_dump())
        store.deployments[str(deployment.id)] = deployment
        return deployment

    def list_all(self) -> list[DeploymentRecord]:
        return list(store.deployments.values())

    def update_status(self, deployment_id: UUID, status: str) -> DeploymentRecord:
        deployment = store.deployments.get(str(deployment_id))
        if not deployment:
            raise KeyError("deployment not found")
        deployment.status = status
        return deployment


deployment_service = DeploymentService()
