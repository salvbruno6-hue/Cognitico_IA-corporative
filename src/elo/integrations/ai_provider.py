"""Provider-neutral boundary for governed external AI calls.

The ELO decides the mission, context, specialist role and evaluation criteria.
This adapter only connects that governed request to a selected provider.
Secrets are read from the execution environment and are never stored here.
Provider-side response storage is disabled so ELO remains the canonical memory authority.
"""

from dataclasses import dataclass, field
from typing import Mapping, Protocol
import os


@dataclass(frozen=True)
class AIRequest:
    """Auditable request envelope prepared by ELO orchestration."""

    request_id: str
    tenant_id: str
    specialist_id: str
    provider: str
    model: str
    instructions: str
    context: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class AIResponse:
    """Provider result kept separate from ELO decision authority."""

    request_id: str
    provider: str
    model: str
    output: str
    provenance: Mapping[str, str] = field(default_factory=dict)


class AIProvider(Protocol):
    """Minimal provider contract used by the Intelligence Router."""

    provider_id: str

    def generate(self, request: AIRequest) -> AIResponse:
        ...


class OpenAIProvider:
    """OpenAI adapter; credentials come only from OPENAI_API_KEY."""

    provider_id = "openai"

    def __init__(self):
        self._api_key = os.environ.get("OPENAI_API_KEY")
        if not self._api_key:
            raise RuntimeError("OPENAI_API_KEY is required for the OpenAI adapter")

    def generate(self, request: AIRequest) -> AIResponse:
        if request.provider != self.provider_id:
            raise ValueError("request provider does not match OpenAI adapter")
        from openai import OpenAI

        client = OpenAI(api_key=self._api_key)
        response = client.responses.create(
            model=request.model,
            input=(
                f"SPECIALIST MISSION:\n{request.instructions}\n\n"
                f"CORPORATE CONTEXT:\n{request.context}"
            ),
            store=False,
        )
        return AIResponse(
            request_id=request.request_id,
            provider=self.provider_id,
            model=request.model,
            output=response.output_text,
            provenance={
                "provider": self.provider_id,
                "model": request.model,
                "request_id": request.request_id,
            },
        )
