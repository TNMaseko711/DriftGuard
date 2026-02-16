# Deployment Guide

## Local

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

## Containerization (recommended next step)

1. Add backend Dockerfile from `python:3.10-slim`.
2. Install dependencies and copy application code.
3. Run `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000`.
4. Place behind an API gateway and add JWT authentication.

## Production hardening

- Replace in-memory store with PostgreSQL and object storage.
- Enable audit logs and RBAC.
- Add Prometheus metrics endpoint and tracing middleware.
- Use Kubernetes HPA for inference services and workers.
