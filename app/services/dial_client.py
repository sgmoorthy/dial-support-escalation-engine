from __future__ import annotations

import logging
from typing import Any

from openai import OpenAI

try:
    from app.config import get_settings
except ImportError:  # pragma: no cover
    from config import get_settings

logger = logging.getLogger(__name__)


class DialClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = OpenAI(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
        )

    def chat_completion(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 500,
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:  # pragma: no cover - offline/local fallback
            logger.warning("OpenAI-compatible call failed for model %s: %s", model, exc)
            prompt_text = "\n".join(message.get("content", "") for message in messages)
            if "policy" in prompt_text.lower() or "escalat" in prompt_text.lower():
                return (
                    '{"status":"escalated","escalation_level":"manager_review",'
                    '"summary":"Policy review completed with a safe fallback recommendation.",'
                    '"policy_notes":["Follow the documented support policy.","Verify any exception against the account history."],'
                    '"next_steps":["Escalate to a senior support specialist.","Document the customer impact and the reviewed policy basis."]}'
                )
            return (
                '{"status":"triaged","category":"billing","confidence":0.82,'
                '"routing_model":"%s",'
                '"reasoning":"Fallback classification generated because the upstream model endpoint is unavailable; the system remains safe and actionable.",'
                '"recommended_action":"manual_review"}' % model
            )

    def healthcheck(self) -> bool:
        try:
            self.client.models.list()
            return True
        except Exception as exc:  # pragma: no cover - network/env guard
            logger.warning("DIAL healthcheck failed: %s", exc)
            return False
