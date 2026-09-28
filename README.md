# EPAM DIAL Multi-Model Orchestrator

A production-oriented reference implementation for a support automation workflow that routes customer issues through a lightweight classification model and a higher-reasoning escalation model. The platform exposes an OpenAI-compatible API surface, integrates with EPAM DIAL and local Ollama runtimes, and includes a lightweight React UI for interactive demo testing.

## What this project does

- Classifies incoming support tickets using a fast model route.
- Reviews escalations using a reasoning-focused policy model.
- Exposes JSON APIs for ticket triage and policy review.
- Provides a browser UI for quick local testing and demos.
- Runs either through Docker Compose or through a local dev setup.

## Architecture

- DIAL Core: OpenAI-compatible proxy layer on port 8080.
- Ollama: local model provider for `llama3` and `phi3`.
- FastAPI service: orchestration API on port 8000.
- React UI: demo interface on port 3000.

## Local stack

- `api`: FastAPI application using the OpenAI SDK against DIAL Core.
- `dial-core`: EPAM DIAL proxy that forwards requests to Ollama.
- `ollama`: model runtime for local inference.
- `ui`: simple Vite + React interface for manual validation.

## Prerequisites

- Docker Desktop or Docker Engine
- Python 3.11+
- Node.js 18+
- Git

## Quick start with Docker Compose

1. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

2. Start the full platform:

   ```bash
   docker compose up --build
   ```

3. Open the UI in a browser:

   - http://localhost:3000

4. Validate the services:

   - DIAL Core: http://localhost:8080
   - API health: http://localhost:8000/healthz
   - Ollama tags: http://localhost:11434/api/tags

## Local development setup

### Backend

```bash
python -m venv .venv
. .venv/bin/activate  # Linux/macOS
# or .\.venv\Scripts\activate  # Windows PowerShell
python -m pip install -r app/requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
cd ui
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

## API endpoints

### 1) Support ticket classification

```http
POST http://localhost:8000/api/support/ticket
Content-Type: application/json
```

Example request:

```json
{
  "customer_email": "alex@example.com",
  "issue_summary": "Customer wants to cancel a subscription and requests a refund after 14 days.",
  "priority": "high",
  "order_id": "ORD-9981",
  "metadata": {
    "channel": "web",
    "source": "support-portal"
  }
}
```

Example response:

```json
{
  "status": "triaged",
  "category": "billing",
  "confidence": 0.87,
  "routing_model": "llama3",
  "reasoning": "Request indicates a billing dispute and refund request; route to billing review.",
  "recommended_action": "manual_review"
}
```

### 2) Policy escalation review

```http
POST http://localhost:8000/api/support/escalate
Content-Type: application/json
```

Example request:

```json
{
  "ticket_id": "T-1042",
  "issue_summary": "Customer has a duplicate charge and is asking for an exception to the refund policy.",
  "customer_profile": "VIP customer with 4-year history",
  "policy_context": "The refund policy allows exceptions only for fraud or service outages.",
  "previous_attempts": [
    "Agent explained standard policy",
    "Customer disputes the previous agent decision"
  ]
}
```

Example response:

```json
{
  "status": "escalated",
  "escalation_level": "manager_review",
  "routing_model": "phi3",
  "summary": "Policy exception request requires a managerial review because multiple policy criteria apply.",
  "policy_notes": [
    "Review the customer history for any service-affecting issues.",
    "Apply the documented refund exception rules before approval."
  ],
  "next_steps": [
    "Escalate to a senior support specialist.",
    "Document the rationale used for the review."
  ]
}
```

## Model routing behavior

- `llama3` is used for fast support classification and triage.
- `phi3` is used for policy-heavy escalation reasoning and approval guidance.
- If the remote OpenAI-compatible service is unavailable, the client includes a safe fallback response so the service remains usable in local demo scenarios.

## Repository layout

```text
.
├── app/
│   ├── __init__.py
│   ├── Dockerfile
│   ├── README.md
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── routers/
│   │   └── support.py
│   └── services/
│       └── dial_client.py
├── docker/
│   └── dial/
│       └── config.yaml
├── docs/
│   ├── API.md
│   └── SETUP.md
├── tests/
│   └── test_endpoints.py
├── ui/
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.js
│       └── styles.css
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docker-compose.prod.yml
├── LICENSE
├── Makefile
├── README.md
└── SECURITY.md
```

## Verification and quality checks

Run the project validation locally:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r app/requirements.txt pytest
python -m pytest -q
```

Build the UI bundle:

```bash
cd ui
npm install
npm run build
```

## Troubleshooting

- If the app cannot reach the model gateway, verify that DIAL Core and Ollama are both running.
- If `localhost` connections fail inside Docker, confirm the environment variables align with the host mapping.
- If the UI cannot reach the API, make sure port 8000 is not blocked and that the backend is started before the browser request is sent.
- If the model names do not match your local runtime, update `FAST_MODEL` and `REASONING_MODEL` in `.env` or the container environment.

## License

This project is distributed under the MIT license. See [LICENSE](LICENSE) for more details.
