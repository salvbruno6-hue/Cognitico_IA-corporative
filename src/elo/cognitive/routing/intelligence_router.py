"""Governed symbiotic intelligence router.

Reuses the canonical ExecutionRouter for capability/model/tool selection and
adds provider resolution without creating a second routing authority.
"""

from dataclasses import dataclass
from typing import Mapping

from .execution_routing import ExecutionRouter, RoutingDecision
from ..integrations.ai_provider import AIProvider, AIRequest, AIResponse


@dataclass(frozen=True)
class IntelligenceRequest:
    request_id: str
    tenant_id: str
    specialist_id: str
    capability: str
    instructions: str
    context: str = ""
    metadata: Mapping[str, str] = None


class IntelligenceRouter:
    """Coordinate selection and invocation of an already-governed provider."""

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
        provider_id = decision.model_id.split(":", 1)[0]
        provider = self.providers.get(provider_id)
        if provider is None:
            raise LookupError(f"no provider adapter registered for: {provider_id}")
        ai_request = AIRequest(
            request_id=request.request_id,
            tenant_id=request.tenant_id,
            specialist_id=request.specialist_id,
            provider=provider_id,
            model=decision.model_id.split(":", 1)[1] if ":" in decision.model_id else decision.model_id,
            instructions=request.instructions,
            context=request.context,
            metadata=request.metadata or {},
        )
        return decision, provider.generate(ai_request)
