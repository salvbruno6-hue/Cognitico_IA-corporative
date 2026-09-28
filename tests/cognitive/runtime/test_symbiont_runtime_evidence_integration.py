from datetime import datetime, timezone

from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeOperationalEvidenceCollector
from elo.cognitive.symbiont_skill_runtime import SymbiontSkillRuntime


def _item(execution_id: str):
    return create_runtime_evidence(
        execution_id=execution_id,
        candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
        owner="HERMES-CONTEXT",
        runtime_entrypoint="elo.context.resolve",
        action_observed=True,
        metric="context_plugin_activation_success_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=1.0,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit="runtime-commit",
            runtime_trace=f"trace-{execution_id}",
        ),
        regression=False,
        repeatability=RepeatabilityEvidence(1, 1, 1.0),
        timestamp=datetime(2026, 9, 27, tzinfo=timezone.utc),
    )


def test_symbiont_runtime_consumes_collector_outcome_without_promoting_it():
    collector = RuntimeOperationalEvidenceCollector()
    collector.append(_item("exec-1"))
    collector.append(_item("exec-2"))

    group = collector.ready_groups()[0]
    evidence = SymbiontSkillRuntime.evaluate_runtime_evidence(group)

    assert evidence.level == "OPERATIONAL_OUTCOME"
    assert evidence.production_proven is False
    assert evidence.attribution == "CANDIDATE_ATTRIBUTED"
