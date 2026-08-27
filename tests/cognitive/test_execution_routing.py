from elo.cognitive.routing.execution_routing import ExecutionRouter
from elo.cognitive.routing.model_selection import ModelCandidate, ModelSelector
from elo.cognitive.routing.tool_selection import ToolCandidate, ToolSelector


def test_execution_router_can_select_model_and_tool_for_same_capability():
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    decision = router.route(
        "retrieval",
        models=[ModelCandidate("retriever-model", frozenset({"retrieval"}), quality=.9, evidence=.9)],
        tools=[ToolCandidate("supabase", frozenset({"retrieval"}), reliability=.95, evidence=.9)],
    )
    assert decision.model_id == "retriever-model"
    assert decision.tool_id == "supabase"


def test_execution_router_requires_an_executable_route():
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    try:
        router.route("calculation")
    except LookupError as exc:
        assert "calculation" in str(exc)
    else:
        raise AssertionError("missing execution route must fail")
