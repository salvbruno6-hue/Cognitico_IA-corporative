import pytest

from src.elo.cognitive.routing.execution_routing import ExecutionRouter
from src.elo.cognitive.routing.intelligence_router import IntelligenceRequest, IntelligenceRouter
from src.elo.cognitive.routing.model_selection import ModelCandidate, ModelSelector
from src.elo.cognitive.routing.tool_selection import ToolSelector


class FakeProvider:
    provider_id = "fake"

    def generate(self, request):
        from src.elo.integrations.ai_provider import AIResponse
        return AIResponse(request.request_id, self.provider_id, request.model, "ok", {"tenant_id": request.tenant_id})


def test_router_reuses_execution_router_and_preserves_tenant():
    router = IntelligenceRouter(
        ExecutionRouter(ModelSelector(), ToolSelector()),
        {"fake": FakeProvider()},
    )
    decision, response = router.route_and_execute(
        IntelligenceRequest("r1", "tenant-a", "budget-specialist", "reasoning", "calculate", "context"),
        models=[ModelCandidate("fake:test-model", frozenset({"reasoning"}), 1.0)],
    )
    assert decision.model_id == "fake:test-model"
    assert response.request_id == "r1"
    assert response.provenance["tenant_id"] == "tenant-a"


def test_router_blocks_unknown_provider():
    router = IntelligenceRouter(ExecutionRouter(ModelSelector(), ToolSelector()), {})
    with pytest.raises(LookupError):
        router.route_and_execute(
            IntelligenceRequest("r1", "tenant-a", "specialist", "reasoning", "do"),
            models=[ModelCandidate("unknown:model", frozenset({"reasoning"}), 1.0)],
        )
