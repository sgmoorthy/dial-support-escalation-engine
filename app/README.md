# API Service

This service exposes a production-ready support orchestration API for routing support requests through a DIAL-compatible model gateway.

## Run locally

```bash
cd app
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Health check

```bash
curl http://localhost:8000/healthz
```
