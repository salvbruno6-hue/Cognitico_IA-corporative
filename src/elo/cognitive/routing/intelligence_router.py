"""Governed symbiotic intelligence router.

Reuses the canonical ExecutionRouter for capability/model/tool selection and
adds provider resolution without creating a second routing authority.
"""

from dataclasses import dataclass, field
from typing import Mapping

from .execution_routing import ExecutionRouter, RoutingDecision
from ...integrations.ai_provider import AIProvider, AIRequest, AIResponse


@dataclass(frozen=True)
class IntelligenceRequest:
    request_id: str
    tenant_id: str
    specialist_id: str
    capability: str
    instructions: str
    context: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)


class IntelligenceRouter:
    """Coordinate selection and invocation of an already-governed provider.

    ``ExecutionRouter`` remains the canonical selection authority. Provider
    resolution is an interoperability concern and never becomes a second
    model-selection policy.
    """

    def __init__(self, execution_router: ExecutionRouter, providers: Mapping[str, AIProvider]):
        self.execution_router = execution_router
        self.providers = providers

    def route_and_execute(
        self,
        request: IntelligenceRequest,
        *,
        models=None,
        tools=None,
        preferred_models=None,
    ) -> tuple[RoutingDecision, AIResponse]:
        decision = self.execution_router.route(
            request.capability,
            models=models,
            tools=tools,
            preferred_models=preferred_models,
        )
        if not decision.model_id:
            raise LookupError("selected route has no AI model")

        provider_id, model_id = self._resolve_provider_and_model(decision.model_id)
        provider = self.providers.get(provider_id)
        if provider is None:
            raise LookupError(f"no provider adapter registered for: {provider_id}")

        ai_request = AIRequest(
            request_id=request.request_id,
            tenant_id=request.tenant_id,
            specialist_id=request.specialist_id,
            provider=provider_id,
            model=model_id,
            instructions=request.instructions,
            context=request.context,
            metadata=dict(request.metadata),
        )
        return decision, provider.generate(ai_request)

    @staticmethod
    def _resolve_provider_and_model(model_id: str) -> tuple[str, str]:
        """Resolve the current model-candidate convention explicitly.

        Model selection remains provider-neutral. Interoperability currently
        accepts the repository's ``provider:model`` identifier convention;
        malformed identifiers are rejected instead of guessing a provider.
        """
        if not model_id or ":" not in model_id:
            raise LookupError("model identifier must use provider:model format")
        provider_id, selected_model = model_id.split(":", 1)
        if not provider_id or not selected_model:
            raise LookupError("model identifier must contain provider and model")
        return provider_id, selected_model
