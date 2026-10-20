import pytest

from elo.cognitive.reasoning.requirement_analysis import RequirementNode
from elo.cognitive.reasoning.requirement_dependencies import (
    RequirementDependencyGraph,
    audit_requirement_dependency_graph,
)


def test_whitespace_only_requirement_id_invalidates_graph_before_assessment():
    node = RequirementNode(requirement_id="   ", text="blank identifier")
    graph = RequirementDependencyGraph((node,))

    assert graph.validation.valid is False
    assert graph.validation.invalid_requirement_ids == ("   ",)

    audit = audit_requirement_dependency_graph(graph)
    assert audit["valid"] is False
    assert audit["invalid_requirement_ids"] == ("   ",)

    with pytest.raises(ValueError, match="requirement dependency graph is invalid"):
        graph.assess(requirement_id="   ", assessments={})
