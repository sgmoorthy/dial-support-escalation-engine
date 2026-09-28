# Architecture Overview

This project demonstrates a practical orchestration pattern for support automation using an OpenAI-compatible model gateway. The app routes customer queries through two model paths:

- a fast, low-latency model for support classification
- a higher-reasoning model for policy-sensitive escalations

## System components

### 1. UI layer

The React app runs in the browser and allows a user to:

- submit a customer issue for ticket classification
- trigger an escalation review for policy-heavy support cases
- inspect the raw JSON response returned by the API

The UI sends requests to the FastAPI service on port 8000.

### 2. FastAPI orchestration layer

The Python service exposes two REST endpoints:

- `POST /api/support/ticket`
- `POST /api/support/escalate`

This service validates incoming data, builds a prompt for the model gateway, and converts the returned content into a structured JSON response.

### 3. DIAL Core gateway

DIAL Core acts as the OpenAI-compatible proxy layer. It is configured to forward requests to the local Ollama runtime but presents a consistent OpenAI-like API contract to the Python backend.

This abstraction keeps the app logic portable and allows the system to swap providers without changing the orchestration code.

### 4. Ollama model runtime

The local model host provides:

- `llama3` for fast classification and routing
- `phi3` for higher-reasoning support review and exception handling

## Request flow

### Ticket classification flow

1. User submits a support ticket from the UI.
2. UI makes a POST request to `/api/support/ticket`.
3. FastAPI validates the payload and builds a classification prompt.
4. The application calls the DIAL-compatible API using the configured model.
5. The response is parsed and returned as a normalized `SupportDecision` object.

### Escalation flow

1. User submits an escalation scenario from the UI.
2. UI posts the payload to `/api/support/escalate`.
3. FastAPI builds a policy-review prompt.
4. The application routes the request to the reasoning model.
5. The response is parsed into an `EscalationResult` object containing summary notes and next steps.

## Failure tolerant behavior

The backend includes a safe fallback path when the DIAL endpoint is not available. In that case, the service still returns structured data to keep the demo environment usable.

This is especially helpful for local development or constrained environments where model backends are not fully available.

## Security and operational notes

- The app is designed for local development and demo use by default.
- Environment variables are used to control route endpoints and model names.
- CORS is enabled to allow browser-based testing against the API.
- The Docker setup is intentionally simple for a reference implementation.

## Why this architecture works well

This pattern separates concerns cleanly:

- the UI is only responsible for interaction
- the API handles request orchestration
- DIAL abstracts model connectivity
- Ollama provides local model runtime support

That separation makes the system easier to test, extend, and evolve into a larger support automation platform.
