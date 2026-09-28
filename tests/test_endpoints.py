from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ticket_classification() -> None:
    response = client.post(
        "/api/support/ticket",
        json={
            "customer_email": "alex@example.com",
            "issue_summary": "I need help with a billing dispute and refund request.",
            "priority": "high",
            "order_id": "ORD-123",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "routing_model" in body


def test_escalation() -> None:
    response = client.post(
        "/api/support/escalate",
        json={
            "ticket_id": "T-1001",
            "issue_summary": "The customer wants a policy exception after a duplicate charge.",
            "customer_profile": "Important customer",
            "policy_context": "Exceptions are limited to fraud or outage cases.",
            "previous_attempts": ["Explained policy", "Requested manual review"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "summary" in body
