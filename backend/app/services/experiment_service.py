from __future__ import annotations

from datetime import datetime
from uuid import UUID

from backend.app.models.schemas import ExperimentCreate, ExperimentRecord, RunCreate, RunRecord, RunStatus
from backend.app.services.store import store


class ExperimentService:
    def create_experiment(self, payload: ExperimentCreate) -> ExperimentRecord:
        record = ExperimentRecord(**payload.model_dump())
        store.experiments[str(record.id)] = record
        return record

    def list_experiments(self) -> list[ExperimentRecord]:
        return list(store.experiments.values())

    def create_run(self, payload: RunCreate) -> RunRecord:
        if str(payload.experiment_id) not in store.experiments:
            raise KeyError("experiment not found")
        run = RunRecord(**payload.model_dump())
        store.runs[str(run.id)] = run
        return run

    def log_metrics(self, run_id: UUID, metrics: dict[str, float], step: int) -> RunRecord:
        run = store.runs.get(str(run_id))
        if not run:
            raise KeyError("run not found")
        for key, value in metrics.items():
            run.metrics.setdefault(key, []).append({"step": step, "value": value})
        return run

    def complete_run(self, run_id: UUID, status: RunStatus) -> RunRecord:
        run = store.runs.get(str(run_id))
        if not run:
            raise KeyError("run not found")
        run.status = status
        run.end_time = datetime.utcnow()
        return run


experiment_service = ExperimentService()
