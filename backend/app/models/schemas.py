from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Stage(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"
    archived = "archived"


class RunStatus(str, Enum):
    running = "running"
    completed = "completed"
    failed = "failed"
    stopped = "stopped"


class DeploymentStrategy(str, Enum):
    blue_green = "blue_green"
    canary = "canary"
    shadow = "shadow"


class ModelCreate(BaseModel):
    name: str
    description: str = ""
    framework: str
    task_type: str
    created_by: str
    tags: list[str] = Field(default_factory=list)


class ModelVersionCreate(BaseModel):
    version: str
    artifact_uri: str
    metrics: dict[str, float] = Field(default_factory=dict)
    parameters: dict[str, Any] = Field(default_factory=dict)
    training_data_hash: str
    training_duration_seconds: int
    model_size: int
    inference_latency_ms: float
    notes: str = ""


class ModelRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    name: str
    version: str
    description: str
    framework: str
    task_type: str
    created_by: str
    tags: list[str] = Field(default_factory=list)


class ModelVersionRecord(BaseModel):
    model_id: UUID
    version: str
    stage: Stage = Stage.development
    artifact_uri: str
    metrics: dict[str, float] = Field(default_factory=dict)
    parameters: dict[str, Any] = Field(default_factory=dict)
    training_data_hash: str
    training_duration_seconds: int
    model_size: int
    inference_latency_ms: float
    promoted_at: datetime | None = None
    promoted_by: str | None = None
    notes: str = ""


class ExperimentCreate(BaseModel):
    name: str
    description: str = ""
    tags: list[str] = Field(default_factory=list)


class ExperimentRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RunCreate(BaseModel):
    experiment_id: UUID
    run_name: str
    user_id: str
    git_commit: str
    source_code: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class RunRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    experiment_id: UUID
    run_name: str
    status: RunStatus = RunStatus.running
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime | None = None
    user_id: str
    git_commit: str
    source_code: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, list[dict[str, float | int]]] = Field(default_factory=dict)
    artifacts: list[str] = Field(default_factory=list)


class DeploymentCreate(BaseModel):
    model_id: UUID
    model_version: str
    environment: str
    strategy: DeploymentStrategy
    traffic_percentage: int = 100


class DeploymentRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    model_id: UUID
    model_version: str
    environment: str
    strategy: DeploymentStrategy
    status: str = "created"
    traffic_percentage: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ABVariant(BaseModel):
    variant_id: str
    model_version: str
    traffic_percentage: int


class ABTestCreate(BaseModel):
    name: str
    model_id: UUID
    variants: list[ABVariant]
    primary_metric: str
    allocation_method: str = "user_id_hash"


class ABTestRecord(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    model_id: UUID
    variants: list[ABVariant]
    primary_metric: str
    allocation_method: str
    status: str = "running"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DriftRequest(BaseModel):
    feature_name: str
    reference: list[float]
    current: list[float]
    bins: int = 10
