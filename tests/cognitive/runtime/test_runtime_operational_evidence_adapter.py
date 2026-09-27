from elo.agent_intake.hermes_functional_value_proof import FunctionalValueEvidence
from elo.agent_intake.runtime_operational_evidence import (
    RepeatabilityEvidence,
    RuntimeProvenance,
    create_runtime_evidence,
)
from elo.agent_intake.runtime_operational_evidence_adapter import to_operational_outcome


def _item(execution_id: str):
    return create_runtime_evidence(
        execution_id=execution_id,
        candidate_id="EXT-CONTEXT-PLUGIN-HERMES",
        owner="HERMES-CONTEXT",
        runtime_entrypoint="ELOKnowledgeProvider.retrieve",
        action_observed=True,
        metric="context_plugin_activation_success_rate",
        direction="maximize",
        baseline=0.0,
        observed_value=1.0,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit="commit-1",
            runtime_trace=f"trace-{execution_id}",
        ),
        regression=False,
        repeatability=RepeatabilityEvidence(1, 1, 1.0),
    )


def test_two_real_observations_become_operational_outcome():
    evidence = to_operational_outcome((_item("exec-1"), _item("exec-2")))

    assert isinstance(evidence, FunctionalValueEvidence)
    assert evidence.level == "OPERATIONAL_OUTCOME"
    assert evidence.production_proven is True
    assert evidence.repeatable is True
    assert evidence.functional_gain_proven is True
    assert len(evidence.provenance_refs) == 2


def test_single_observation_does_not_become_operational_outcome():
    evidence = to_operational_outcome((_item("exec-1"),))

    assert evidence.level == "FUNCTIONAL_CONTROLLED_GAIN"
    assert evidence.production_proven is False
    assert evidence.repeatable is False
