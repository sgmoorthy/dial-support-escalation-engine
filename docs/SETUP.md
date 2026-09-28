# Local Setup Guide

This guide explains how to run the EPAM DIAL Multi-Model Orchestrator in a local environment and verify all major services.

## Prerequisites

- Docker Desktop or Docker Engine
- Python 3.11+
- Node.js 18+
- Git
- Access to the internet for pulling model and package dependencies

## 1. Clone the repository

```bash
git clone https://github.com/sgmoorthy/dial-support-escalation-engine.git
cd dial-support-escalation-engine
```

## 2. Configure environment variables

Create a local `.env` file from the example template:

```bash
cp .env.example .env
```

The default values are suitable for a local demo:

```env
APP_ENV=development
APP_PORT=8000
DIAL_HOST=0.0.0.0
DIAL_PORT=8080
OLLAMA_HOST=ollama
OLLAMA_PORT=11434
OPENAI_API_KEY=dial-demo-key
OPENAI_BASE_URL=http://localhost:8080/v1
FAST_MODEL=llama3
REASONING_MODEL=phi3
LOG_LEVEL=INFO
```

## 3. Run the full stack with Docker Compose

```bash
docker compose up --build
```

This starts:

- Ollama on port 11434
- DIAL Core on port 8080
- FastAPI service on port 8000
- React UI on port 3000

## 4. Validate the services

### API health

```bash
curl http://localhost:8000/healthz
```

Expected output:

```json
{"status":"ok","service":"epam-dial-multi-model-orchestrator"}
```

### DIAL Core status

```bash
curl http://localhost:8080
```

### Ollama available models

```bash
curl http://localhost:11434/api/tags
```

### UI access

Open the browser at:

```text
http://localhost:3000
```

## 5. Run the backend locally without Docker

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

python -m pip install -r app/requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 6. Run the frontend locally

```bash
cd ui
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

## 7. Run automated tests

```bash
python -m venv .venv
. .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
python -m pip install -r app/requirements.txt pytest
python -m pytest -q
```

## 8. Build the frontend for release

```bash
cd ui
npm run build
```

This creates a production bundle in the `ui/dist` folder.

## 9. Stop the stack

```bash
docker compose down -v
```

This removes the containers and also deletes the local Ollama volume.

## Troubleshooting

### Port already in use

Check whether another process is using the required port:

```bash
netstat -ano | findstr :3000
netstat -ano | findstr :8000
netstat -ano | findstr :8080
```

### DIAL Core cannot reach Ollama

Make sure the `ollama-init` service has finished pulling the required models and that the Docker network is running correctly.

### The UI is blank or API calls fail

Verify that the backend is running and that `http://localhost:8000` is reachable from the browser session.

### Python environment issues

Use the project virtual environment created in `.venv` and install dependencies from `app/requirements.txt` before running the backend tests.
