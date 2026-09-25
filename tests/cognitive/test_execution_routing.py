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


def test_execution_router_progressive_tool_schema_search_is_bounded_and_non_executing():
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    result = router.search_tool_schemas("browser", {"session_search": "search session context", "computer_use": "browser computer interaction", "mcp_tool": "external tool invocation"}, limit=1)
    assert result.selected_tools == ("computer_use",)
    assert result.representation_chars == len("computer_use") + len("browser computer interaction")
    assert result.bounded is True
    assert result.executed is False
    assert result.canonical_mutation is False


def test_execution_router_tool_schema_search_preserves_catalog_order():
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    result = router.search_tool_schemas("browser", {"alpha_tool": "alpha browser", "beta_tool": "beta browser", "gamma_tool": "gamma browser"}, limit=2)
    assert result.selected_tools == ("alpha_tool", "beta_tool")


def test_execution_router_tool_schema_search_excludes_unrelated_schemas():
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    result = router.search_tool_schemas("database", {"browser_tool": "browser interaction"})
    assert result.selected_tools == ()
