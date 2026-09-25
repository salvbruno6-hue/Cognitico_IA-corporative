from elo.cognitive.routing.execution_routing import ExecutionRouter
from elo.cognitive.routing.model_selection import ModelSelector
from elo.cognitive.routing.tool_schema_runtime import prepare_tool_schema_context
from elo.cognitive.routing.tool_selection import ToolSelector


def test_operational_schema_context_reuses_canonical_router_without_execution():
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    catalog = {
        "browser_tool": "navigate and search web pages",
        "database_tool": "query database records",
        "computer_tool": "browser computer interaction",
    }

    result = prepare_tool_schema_context(
        router,
        query="browser",
        tool_schemas=catalog,
        limit=2,
    )

    assert result.selected_tools == ("browser_tool", "computer_tool")
    assert result.bounded is True
    assert result.executed is False
    assert result.canonical_mutation is False


def test_operational_schema_context_excludes_unrelated_tools():
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    result = prepare_tool_schema_context(
        router,
        query="database",
        tool_schemas={
            "browser_tool": "navigate pages",
            "database_tool": "query database records",
        },
    )

    assert result.selected_tools == ("database_tool",)
    assert "browser_tool" not in result.selected_tools
