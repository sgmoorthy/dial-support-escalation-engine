from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class SupportTicketRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_email: str = Field(..., min_length=3)
    issue_summary: str = Field(..., min_length=10)
    priority: str = Field(default="medium")
    order_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EscalationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_id: str = Field(..., min_length=3)
    issue_summary: str = Field(..., min_length=10)
    customer_profile: str = Field(default="")
    policy_context: str = Field(default="")
    previous_attempts: List[str] = Field(default_factory=list)


class SupportDecision(BaseModel):
    status: str
    category: str
    confidence: float
    routing_model: str
    reasoning: str
    recommended_action: str


class EscalationResult(BaseModel):
    status: str
    escalation_level: str
    routing_model: str
    summary: str
    policy_notes: List[str]
    next_steps: List[str]
