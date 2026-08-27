from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class InferenceRequest:
    prompt: str
    temperature: float = 0.0
    max_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class InferenceResponse:
    text: str
    provider: str
    model: str
    usage: dict[str, int]


class InferencePort(Protocol):
    """Stable ELO boundary around any model/inference engine."""

    def complete(self, request: InferenceRequest) -> InferenceResponse:
        ...


class StaticInference:
    """Deterministic adapter for tests and contract verification."""

    provider = "static"
    model = "test"

    def __init__(self, response: str) -> None:
        self.response = response

    def complete(self, request: InferenceRequest) -> InferenceResponse:
        return InferenceResponse(
            text=self.response,
            provider=self.provider,
            model=self.model,
            usage={"prompt_tokens": len(request.prompt.split()), "completion_tokens": len(self.response.split())},
        )
