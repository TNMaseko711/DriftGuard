# Architecture Overview

DriftGuard is organized as modular services behind a FastAPI entrypoint.

## Components

1. **Model Registry Service**
   - Registers models and semantic versions.
   - Tracks stage promotion (`development`, `staging`, `production`, `archived`).

2. **Experiment Service**
   - Stores experiments, runs, hyperparameters, and step metrics.

3. **Deployment Service**
   - Persists deployment plans and strategy metadata (`blue_green`, `canary`, `shadow`).

4. **A/B Test Service**
   - Creates weighted variants and deterministic user assignment using MD5 hashing.

5. **Monitoring Service**
   - Computes PSI and KS statistics for drift detection.

## Data Layer

The reference implementation uses in-memory dictionaries for portability.
In production, replace with:
- PostgreSQL for metadata
- Object storage for model artifacts
- Time-series DB for metrics
- Message bus for async pipelines

## Production Extensions

- JWT auth + RBAC middleware
- Event-driven retraining scheduler
- Prometheus and Grafana integration
- Artifact immutability and lineage metadata
- Model serving and Kubernetes automation
