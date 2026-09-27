from elo.agent_intake.hermes_tool_search_runtime import (
    CANDIDATE_ID,
    RUNTIME_ENTRYPOINT,
    search_tool_schemas_with_runtime_evidence,
)
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector
from elo.cognitive.routing.execution_routing import ExecutionRouter
from elo.cognitive.routing.model_selection import ModelSelector
from elo.cognitive.routing.tool_selection import ToolSelector
from elo.cognitive.symbiont_skill_runtime import SymbiontSkillRuntime


def _router() -> ExecutionRouter:
    return ExecutionRouter(ModelSelector(), ToolSelector())


def _schemas() -> dict[str, str]:
    return {"calculator": "add numbers", "search": "find information"}


def test_runtime_bridge_records_one_real_router_observation_without_claiming_repeatability() -> None:
    observation = search_tool_schemas_with_runtime_evidence(
        _router(),
        "search",
        _schemas(),
        baseline_representation_chars=100.0,
        source_commit="abc123",
        runtime_trace="trace-1",
        execution_id="exec-1",
    )

    assert observation.evidence.candidate_id == CANDIDATE_ID
    assert observation.evidence.owner == "ELO Model/Tool Routing"
    assert observation.evidence.runtime_entrypoint == RUNTIME_ENTRYPOINT
    assert observation.evidence.action_observed is True
    assert observation.evidence.attribution == "candidate"
    assert observation.evidence.repeatability.executions == 1
    assert observation.evidence.operational_outcome_proven is False


def test_two_independent_router_executions_become_operational_outcome_through_canonical_collector() -> None:
    collector = RuntimeOperationalEvidenceCollector()

    for execution_id, trace in (("exec-1", "trace-1"), ("exec-2", "trace-2")):
        observation = search_tool_schemas_with_runtime_evidence(
            _router(),
            "search",
            _schemas(),
            baseline_representation_chars=100.0,
            source_commit="abc123",
            runtime_trace=trace,
            execution_id=execution_id,
        )
        collector.append(observation.evidence)

    groups = collector.ready_groups()
    assert len(groups) == 1

    outcome = SymbiontSkillRuntime.evaluate_runtime_evidence(groups[0])

    assert outcome.candidate_id == CANDIDATE_ID
    assert outcome.level == "OPERATIONAL_OUTCOME"
    assert outcome.production_proven is True
    assert outcome.repeatable is True
