from elo.agent_intake.hermes_tool_search_observation import (
    CANDIDATE_ID,
    OWNER,
    observe_tool_search,
)
from elo.cognitive.routing.execution_routing import ExecutionRouter


def test_observation_reuses_execution_router_and_stays_non_executing() -> None:
    router = ExecutionRouter()
    observation = observe_tool_search(
        router,
        "calendar",
        {
            "calendar": "read calendar events",
            "mail": "send and read messages",
        },
        environment="CONTROLLED_OBSERVATION",
    )

    assert observation.candidate_id == CANDIDATE_ID
    assert observation.owner == OWNER
    assert observation.selected_tools == ("calendar",)
    assert observation.disclosed_schema_count == 1
    assert observation.representation_chars == len("calendar") + len("read calendar events")
    assert observation.bounded is True
    assert observation.executed is False
    assert observation.canonical_mutation is False
    assert observation.production_evidence is False


def test_observation_preserves_bounded_limit() -> None:
    observation = observe_tool_search(
        ExecutionRouter(),
        "tool",
        {
            "tool-a": "tool a",
            "tool-b": "tool b",
            "tool-c": "tool c",
        },
        limit=2,
    )

    assert observation.selected_tools == ("tool-a", "tool-b")
    assert observation.disclosed_schema_count == 2
    assert observation.bounded is True
    assert observation.executed is False
    assert observation.canonical_mutation is False
