from dataclasses import dataclass

from elo.agent_intake.hermes_routing_boundary import RoutingSignal
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector
from elo.cognitive.routing.execution_routing import ExecutionRouter
from elo.cognitive.routing.intelligence_router import IntelligenceRequest, IntelligenceRouter
from elo.cognitive.routing.model_selection import ModelCandidate, ModelSelector
from elo.cognitive.routing.tool_selection import ToolSelector
from elo.integrations.ai_provider import AIRequest, AIResponse


@dataclass
class FakeProvider:
    provider_id: str = "openai"

    def generate(self, request: AIRequest) -> AIResponse:
        return AIResponse(
            request_id=request.request_id,
            provider=self.provider_id,
            model=request.model,
            output="ok",
        )


def _router(collector: RuntimeOperationalEvidenceCollector) -> IntelligenceRouter:
    execution = ExecutionRouter(ModelSelector(), ToolSelector())
    return IntelligenceRouter(
        execution,
        {"openai": FakeProvider()},
        runtime_evidence_sink=collector,
    )


def _request(run: int) -> IntelligenceRequest:
    return IntelligenceRequest(
        request_id=f"route-request-{run}",
        tenant_id="tenant-a",
        specialist_id="specialist-a",
        capability="reasoning",
        instructions="bounded route",
    )


def _signal(run: int) -> RoutingSignal:
    return RoutingSignal(
        route_id=f"route-{run}",
        tenant_scope="tenant-a",
        source_refs=("route-source",),
        primary_provider="openai",
        fallback_providers=("backup",),
        credential_pool_strategy="existing-pool",
        provenance_verified=True,
        explicit_policy=True,
    )


def _models() -> list[ModelCandidate]:
    return [
        ModelCandidate(
            model_id="openai:test-model",
            capabilities=frozenset({"reasoning"}),
            quality=1.0,
            evidence=1.0,
        )
    ]


def test_real_intelligence_router_records_route_runtime_observation() -> None:
    collector = RuntimeOperationalEvidenceCollector()
    result = _router(collector).route_and_execute(
        _request(1),
        models=_models(),
        hermes_routing_signal=_signal(1),
        runtime_commit="abc123",
        runtime_trace="route-trace-1",
        execution_id="route-exec-1",
    )
    assert result[0].model_id == "openai:test-model"
    evidence = collector.observations()[0]
    assert evidence.candidate_id == "EXT-ROUTE-HERMES"
    assert evidence.runtime_entrypoint == "IntelligenceRouter.route_and_execute"
    assert evidence.operational_outcome_proven is False


def test_two_real_route_executions_become_operational_outcome() -> None:
    collector = RuntimeOperationalEvidenceCollector()
    router = _router(collector)
    for run in (1, 2):
        router.route_and_execute(
            _request(run),
            models=_models(),
            hermes_routing_signal=_signal(run),
            runtime_commit="abc123",
            runtime_trace=f"route-trace-{run}",
            execution_id=f"route-exec-{run}",
        )
    groups = collector.ready_groups()
    assert len(groups) == 1
    group = groups[0]
    assert group.candidate_id == "EXT-ROUTE-HERMES"
    assert group.repeatable is True
    outcome = group.to_operational_outcome()
    assert outcome.candidate_id == "EXT-ROUTE-HERMES"
    assert outcome.production_proven is False
    assert outcome.repeatable is True
