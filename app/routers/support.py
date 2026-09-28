from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import APIRouter, HTTPException

try:
    from app.config import get_model_for_route
    from app.models import EscalationRequest, EscalationResult, SupportDecision, SupportTicketRequest
    from app.services.dial_client import DialClient
except ImportError:  # pragma: no cover
    from config import get_model_for_route
    from models import EscalationRequest, EscalationResult, SupportDecision, SupportTicketRequest
    from services.dial_client import DialClient

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["support"])


def _extract_json_text(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"status": "unknown", "category": "general", "confidence": 0.0, "reasoning": raw}


@router.post("/support/ticket", response_model=SupportDecision)
async def classify_support_ticket(payload: SupportTicketRequest) -> SupportDecision:
    client = DialClient()
    model = get_model_for_route("support")

    prompt = f"""
You are a support triage assistant. Classify the incoming support request and propose a handling route.
Return valid JSON with keys: status, category, confidence, routing_model, reasoning, recommended_action.

Customer email: {payload.customer_email}
Issue summary: {payload.issue_summary}
Priority: {payload.priority}
Order ID: {payload.order_id or 'N/A'}
Metadata: {json.dumps(payload.metadata, ensure_ascii=False)}
"""

    result = client.chat_completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=300,
    )
    data = _extract_json_text(result)

    return SupportDecision(
        status=data.get("status", "pending_review"),
        category=data.get("category", "general"),
        confidence=float(data.get("confidence", 0.5)),
        routing_model=model,
        reasoning=data.get("reasoning", "No additional reasoning was provided."),
        recommended_action=data.get("recommended_action", "route_to_human_agent"),
    )


@router.post("/support/escalate", response_model=EscalationResult)
async def escalate_support_case(payload: EscalationRequest) -> EscalationResult:
    client = DialClient()
    model = get_model_for_route("escalate")

    prompt = f"""
You are a senior policy reviewer for a customer support team.
Assess this customer escalated issue and provide a concise, policy-aware response.
Return valid JSON with keys: status, escalation_level, summary, policy_notes, next_steps.

Ticket ID: {payload.ticket_id}
Issue summary: {payload.issue_summary}
Customer profile: {payload.customer_profile}
Policy context: {payload.policy_context}
Previous attempts: {json.dumps(payload.previous_attempts, ensure_ascii=False)}
"""

    result = client.chat_completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=500,
    )
    data = _extract_json_text(result)

    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="The model output could not be parsed.")

    return EscalationResult(
        status=data.get("status", "escalated"),
        escalation_level=data.get("escalation_level", "manager_review"),
        routing_model=model,
        summary=data.get("summary", "Policy review completed."),
        policy_notes=data.get("policy_notes", ["Follow existing support guidelines."]),
        next_steps=data.get("next_steps", ["Escalate to a senior support agent."]),
    )
