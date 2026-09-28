# API Documentation

This service provides a pair of support orchestration endpoints powered by an OpenAI-compatible model gateway. The interface is intentionally simple and can be tested directly with curl, Postman, or a browser-based UI.

## Base URL

```text
http://localhost:8000
```

## Health endpoint

### GET /healthz

Returns the service status.

#### Example

```bash
curl http://localhost:8000/healthz
```

#### Response

```json
{
  "status": "ok",
  "service": "epam-dial-multi-model-orchestrator"
}
```

---

## 1. Ticket classification

### POST /api/support/ticket

Classifies a customer support request and suggests which model route or support path should be used.

#### Request schema

```json
{
  "customer_email": "string",
  "issue_summary": "string",
  "priority": "string",
  "order_id": "string or null",
  "metadata": {
    "additionalProp": true
  }
}
```

#### Example request

```bash
curl -X POST http://localhost:8000/api/support/ticket \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "alex@example.com",
    "issue_summary": "Customer reports duplicate billing and wants a refund for a recent order.",
    "priority": "high",
    "order_id": "ORD-9981",
    "metadata": {"channel": "web", "source": "support-portal"}
  }'
```

#### Example response

```json
{
  "status": "triaged",
  "category": "billing",
  "confidence": 0.87,
  "routing_model": "llama3",
  "reasoning": "The request indicates a billing dispute and refund request; route to billing review.",
  "recommended_action": "manual_review"
}
```

#### Response fields

- `status`: classification status
- `category`: inferred issue category
- `confidence`: model confidence score
- `routing_model`: model used for routing
- `reasoning`: explanation text
- `recommended_action`: recommended next action

---

## 2. Escalation review

### POST /api/support/escalate

Reviews an escalated issue and returns a policy-aware recommendation and next-step guidance.

#### Request schema

```json
{
  "ticket_id": "string",
  "issue_summary": "string",
  "customer_profile": "string",
  "policy_context": "string",
  "previous_attempts": ["string"]
}
```

#### Example request

```bash
curl -X POST http://localhost:8000/api/support/escalate \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "T-1042",
    "issue_summary": "Customer disputes a policy denial and asks for an exception to a refund rule.",
    "customer_profile": "VIP customer with 4-year history",
    "policy_context": "The refund policy allows exceptions only for fraud or service outages.",
    "previous_attempts": ["Agent explained policy", "Customer requested a manual review"]
  }'
```

#### Example response

```json
{
  "status": "escalated",
  "escalation_level": "manager_review",
  "routing_model": "phi3",
  "summary": "Policy review completed and escalated to senior support because the exception request falls outside standard policy guidance.",
  "policy_notes": [
    "Follow the documented support policy.",
    "Verify any exception against customer history and incident context."
  ],
  "next_steps": [
    "Escalate to a senior support specialist.",
    "Document the policy basis and decision trail."
  ]
}
```

#### Response fields

- `status`: escalation status
- `escalation_level`: review level required
- `routing_model`: model used for the escalation path
- `summary`: concise summary of the policy decision
- `policy_notes`: human-readable policy guidance
- `next_steps`: recommended follow-up actions

---

## Error handling

The API returns HTTP 422 errors for invalid request payloads and HTTP 500 errors when internal processing fails unexpectedly.

## Notes

This project intentionally keeps the API surface minimal so it can be used as a local reference architecture for model routing, support automation, and customer service orchestration workflows.
