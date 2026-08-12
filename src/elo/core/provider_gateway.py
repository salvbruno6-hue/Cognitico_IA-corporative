"""Provider-neutral gateway for authorized external AI consultation.

Providers implement this boundary; the Cognitive Core remains provider-agnostic.
No provider response is considered canonical without ELO admission and provenance.
"""

from dataclasses import dataclass
from typing import Protocol

from .external_entity import EntityKnowledgeResult, ExternalEntityRequest, EntityResolution


@dataclass(frozen=True)
class ProviderRequest:
    request: ExternalEntityRequest
    entity: EntityResolution
    instruction: str


class AIProvider(Protocol):
    """Minimal provider contract for GPT, Claude, Gemini or another source."""

    name: str

    def consult(self, request: ProviderRequest) -> EntityKnowledgeResult:
        """Return attributed external knowledge for the requested entity."""
        ...


class ProviderUnavailable(RuntimeError):
    """Raised when no authorized provider can answer the consultation."""


class ProviderGateway:
    """Select an authorized provider without coupling ELO to a vendor."""

    def __init__(self, providers: tuple[AIProvider, ...] = ()) -> None:
        self._providers = providers

    def consult(self, request: ProviderRequest) -> EntityKnowledgeResult:
        if not request.request.external_consultation_authorized:
            raise ProviderUnavailable("external consultation is not authorized")
        if not self._providers:
            raise ProviderUnavailable("no authorized AI provider is configured")

        failures: list[str] = []
        for provider in self._providers:
            try:
                return provider.consult(request)
            except Exception as exc:  # provider isolation: one failure must not break fallback
                failures.append(f"{provider.name}: {exc}")

        raise ProviderUnavailable("all configured providers failed: " + "; ".join(failures))
