# EPAM DIAL Multi-Model Orchestrator

A production-oriented reference implementation for a multi-model support orchestration system built with FastAPI, OpenAI-compatible client code, Ollama, and EPAM DIAL Core. The repository demonstrates dynamic routing between a fast classification model and a higher-reasoning model behind a single OpenAI-compatible API surface.

## Architecture

- DIAL Core: OpenAI-compatible proxy layer on port 8080.
- Ollama: local model provider hosting `llama3:8b` and `phi3`.
- FastAPI service: orchestrator for support workflows on port 8000.
- React UI: lightweight chat panel on port 3000.

## Local stack

- `api`: FastAPI orchestrator with OpenAI Python SDK connected to DIAL Core.
- `dial-core`: EPAM DIAL proxy that routes requests to Ollama.
- `ollama`: local model runtime for `llama3` and `phi3`.
- `ui`: React application for test and demo workflows.

## Quick start

1. Copy environment variables from the example file:

   ```bash
   cp .env.example .env
   ```

2. Start the platform:

   ```bash
   docker compose up --build
   ```

3. Open the UI:

   - http://localhost:3000

4. Health checks:

   - DIAL Core: http://localhost:8080
   - API: http://localhost:8000/healthz
   - Ollama: http://localhost:11434/api/tags

## API endpoints

### Support ticket classification

```http
POST http://localhost:8000/api/support/ticket
Content-Type: application/json
```

Example body:

```json
{
  "customer_email": "alex@example.com",
  "issue_summary": "Customer wants to cancel a subscription and requests a refund after 14 days.",
  "priority": "high",
  "order_id": "ORD-9981"
}
```

### Policy escalation

```http
POST http://localhost:8000/api/support/escalate
Content-Type: application/json
```

Example body:

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

## Model routing

- `llama3` is used for fast intent classification and routing.
- `phi3` is used for policy-heavy, high-reasoning escalations and approvals.

## Repository layout

```text
.
├── app/
│   ├── __init__.py
│   ├── Dockerfile
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── routers/
│   │   ├── __init__.py
│   │   └── support.py
│   └── services/
│       ├── __init__.py
│       └── dial_client.py
├── docker/
│   └── dial/
│       └── config.yaml
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
├── README.md
└── tests/
    └── test_endpoints.py
```

## Notes

This repo is designed to run locally first and can serve as the base for CI/CD operations or a deployment pipeline. The OpenAI-compatible client ensures that the FastAPI service can easily switch between DIAL Core, local mock providers, or a cloud-hosted AI gateway without changing app logic.
