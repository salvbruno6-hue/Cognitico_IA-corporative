"""Governed symbiotic intelligence router.

Reuses the canonical ExecutionRouter for capability/model/tool selection and
adds provider resolution without creating a second routing authority.
"""

from dataclasses import dataclass, field
from typing import Mapping

from ...agent_intake.hermes_routing_adapter import RoutingPlanContract, adapt_routing
from ...agent_intake.hermes_routing_boundary import RoutingSignal
from ...agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeEvidenceSink,
    RuntimeProvenance,
    create_execution_id,
    create_runtime_evidence,
)
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

    ExecutionRouter remains the canonical selection authority. Provider
    resolution is interoperability only and never becomes a second policy.
    """

    def __init__(
        self,
        execution_router: ExecutionRouter,
        providers: Mapping[str, AIProvider],
        *,
        runtime_evidence_sink: RuntimeEvidenceSink | None = None,
    ):
        self.execution_router = execution_router
        self.providers = providers
        self.runtime_evidence_sink = runtime_evidence_sink

    def route_and_execute(
        self,
        request: IntelligenceRequest,
        *,
        models=None,
        tools=None,
        preferred_models=None,
        hermes_routing_signal: RoutingSignal | None = None,
        runtime_commit: str | None = None,
        runtime_trace: str | None = None,
        execution_id: str | None = None,
    ) -> tuple[RoutingDecision, AIResponse]:
        route_contract: RoutingPlanContract | None = None
        if hermes_routing_signal is not None:
            route_contract = adapt_routing(hermes_routing_signal)
            if route_contract is None:
                raise PermissionError("Hermes routing policy rejected execution")

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
        if route_contract is not None and provider_id != route_contract.primary_provider:
            raise PermissionError("selected provider violates Hermes routing policy")

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
        response = provider.generate(ai_request)

        if route_contract is not None and self.runtime_evidence_sink is not None and runtime_commit and runtime_trace:
            self.runtime_evidence_sink.append(
                create_runtime_evidence(
                    execution_id=execution_id or create_execution_id("EXT-ROUTE-HERMES"),
                    candidate_id="EXT-ROUTE-HERMES",
                    owner="ELO Model/Tool Routing",
                    runtime_entrypoint="IntelligenceRouter.route_and_execute",
                    action_observed=True,
                    metric="routing_plan_integrity_rate",
                    direction="maximize",
                    baseline=0.0,
                    observed_value=1.0,
                    attribution="candidate",
                    regression=False,
                    provenance=RuntimeProvenance(
                        commit=runtime_commit,
                        runtime_trace=runtime_trace,
                    ),
                    repeatability=RepeatabilityEvidence(1, 1, 1.0),
                )
            )
        return decision, response

    @staticmethod
    def _resolve_provider_and_model(model_id: str) -> tuple[str, str]:
        """Resolve provider:model explicitly; malformed identifiers are rejected."""
        if not model_id or ":" not in model_id:
            raise LookupError("model identifier must use provider:model format")
        provider_id, selected_model = model_id.split(":", 1)
        if not provider_id or not selected_model:
            raise LookupError("model identifier must contain provider and model")
        return provider_id, selected_model
