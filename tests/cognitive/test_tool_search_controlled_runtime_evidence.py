"""Controlled runtime-path evidence for progressive tool-schema disclosure.

This test exercises the existing ExecutionRouter integration without invoking
any selected tool or mutating canonical state. It is evidence for the
post-merge observation stage, not production deployment evidence.
"""

from elo.cognitive.routing.execution_router import ExecutionRouter
from elo.cognitive.routing.model_selection import ModelSelector
from elo.cognitive.routing.tool_selection import ToolSelector


def test_progressive_tool_schema_search_controlled_runtime_path():
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    catalog = {
        "browser_tool": "browser navigation and page lookup",
        "database_tool": "database query and records",
        "computer_tool": "browser computer interaction",
    }

    result = router.search_tool_schemas("browser", catalog, limit=2)

    assert result.selected_tools == ("browser_tool", "computer_tool")
    assert result.bounded is True
    assert result.executed is False
    assert result.canonical_mutation is False
    assert result.representation_chars == (
        len("browser_tool")
        + len("browser navigation and page lookup")
        + len("computer_tool")
        + len("browser computer interaction")
    )


def test_progressive_tool_schema_search_controlled_path_excludes_unrelated_schema():
    router = ExecutionRouter(ModelSelector(), ToolSelector())
    result = router.search_tool_schemas(
        "database",
        {
            "browser_tool": "browser navigation",
            "database_tool": "database query",
        },
        limit=5,
    )

    assert result.selected_tools == ("database_tool",)
    assert result.executed is False
    assert result.canonical_mutation is False
