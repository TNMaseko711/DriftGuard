# Experimentra MLOps Platform

Experimentra is a self-hosted, framework-agnostic MLOps platform blueprint that covers the full ML lifecycle:

- Experiment tracking
- Model registry and semantic versioning
- Deployment orchestration (blue/green, canary, shadow)
- A/B testing with consistent assignment
- Drift and performance monitoring
- Automated retraining trigger evaluation

This repository contains a production-style **backend reference implementation** with modular services, REST API routes, and tests for critical platform behaviors.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload
```

## Run tests

```bash
pytest -q
```

## Implemented API groups

- `/api/models` — model registry metadata and versioning
- `/api/experiments` — experiments and runs
- `/api/deployments` — deployment plans and lifecycle states
- `/api/ab-tests` — test configuration and deterministic assignment
- `/api/monitoring` — drift statistics (PSI, KS)

## Architecture notes

See `docs/architecture.md` for a logical architecture and `docs/api-reference.md` for API contracts.
