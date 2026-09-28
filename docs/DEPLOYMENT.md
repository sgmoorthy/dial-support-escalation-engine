# Deployment Guide

This document covers how to deploy the project in a local development environment and how to extend it toward a more production-oriented setup.

## Local deployment

The repository is designed to run locally first using Docker Compose.

```bash
docker compose up --build
```

This starts the complete stack:

- Ollama runtime
- DIAL Core proxy
- FastAPI backend
- React frontend

## Service ports

| Service | Port | Purpose |
|---|---:|---|
| Ollama | 11434 | Local model runtime |
| DIAL Core | 8080 | OpenAI-compatible gateway |
| FastAPI API | 8000 | Support orchestration API |
| UI | 3000 | Demo browser interface |

## Production-oriented considerations

The current reference implementation is intentionally lightweight and local-first. For a real production deployment, consider the following improvements:

- move sensitive secrets to a secret manager such as GCP Secret Manager or HashiCorp Vault
- add authentication and authorization for the API
- add structured logs and request tracing
- enforce timeout and retry policies for external model calls
- store configuration in a managed deployment environment
- add a CI pipeline for build and test validation
- add health-check and readiness monitoring for all services

## Environment configuration

The service reads settings from environment variables or a `.env` file. Typical settings include:

- `APP_PORT`
- `OPENAI_BASE_URL`
- `OPENAI_API_KEY`
- `FAST_MODEL`
- `REASONING_MODEL`
- `LOG_LEVEL`

These values are defined in `.env.example` and can be adjusted to match your deployment target.

## Docker Compose deployment

Use the Compose file in the root of the repository:

```bash
docker compose up --build -d
```

To stop the stack:

```bash
docker compose down -v
```

## Frontend deployment

The UI is a Vite application and can be built for production with:

```bash
cd ui
npm install
npm run build
```

The output is generated under `ui/dist` and can be served by a static web host or behind a reverse proxy.

## Backend deployment

The backend can be started directly with Uvicorn:

```bash
cd app
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

For production, consider a process manager or container orchestrator such as Docker, Kubernetes, or a managed service.

## Health monitoring

The API exposes a health endpoint:

```bash
curl http://localhost:8000/healthz
```

This endpoint can be used by Docker health checks, load balancers, and uptime monitoring systems.

## Recommended rollout checklist

1. Validate environment variables and network access.
2. Ensure model runtime is available and healthy.
3. Run the backend test suite.
4. Build and validate the UI bundle.
5. Deploy the stack to the target environment.
6. Confirm health endpoints and example API calls succeed.
7. Monitor logs and model gateway latency after release.
