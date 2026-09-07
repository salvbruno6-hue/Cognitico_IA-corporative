import pytest

from elo.agentic.graph import GraphRuntimePolicy, build_agentic_graph
from elo.agentic.orchestrator import KnowledgeOrchestrator


def test_graph_runtime_rejects_writes():
    with pytest.raises(ValueError):
        build_agentic_graph(
            KnowledgeOrchestrator(provider=object()),
            policy=GraphRuntimePolicy(allow_writes=True),
        )


def test_graph_runtime_does_not_require_langgraph_for_import():
    # Importing the module itself must remain possible without the optional dependency.
    assert GraphRuntimePolicy().allow_writes is False
