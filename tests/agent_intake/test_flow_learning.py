from elo.agent_intake.elo_flow_cadence import CadenceOutcome
from elo.agent_intake.flow_complementarity import (
    ComplementarityEngine,
    FlowProfile,
    RelationKind,
    hermes_relation,
)
from elo.agent_intake.governed_flow_router import GovernedFlowRouter
from elo.agent_intake.flow_learning import (
    FlowAdaptationEngine,
    FlowOutcomeRecord,
    SQLiteFlowLearningStore,
)


def test_flow_learning_persists_and_adapts(tmp_path):
    store = SQLiteFlowLearningStore(tmp_path / "flow-learning.db")
    learning = FlowAdaptationEngine(store)

    first = learning.record(
        FlowOutcomeRecord(
            relation_id="r1",
            origin_flow="CONTROLLED_TEST",
            target_flow="MEASURED_GAIN",
            outcome="PASS",
            success=True,
            evidence_refs=("e1",),
            provenance_refs=("p1",),
        )
    )
    assert first.status == "INSUFFICIENT_EVIDENCE"

    second = learning.record(
        FlowOutcomeRecord(
            relation_id="r1",
            origin_flow="CONTROLLED_TEST",
            target_flow="MEASURED_GAIN",
            outcome="PASS",
            success=True,
            evidence_refs=("e2",),
            provenance_refs=("p2",),
        )
    )
    assert second.status == "REPEATABLE_CANDIDATE"
    assert second.observations == 2
    assert second.success_rate == 1.0

    reopened = SQLiteFlowLearningStore(tmp_path / "flow-learning.db")
    assert len(reopened.history("r1")) == 2


def test_failed_outcomes_do_not_become_repeatable():
    store = SQLiteFlowLearningStore(":memory:")
    learning = FlowAdaptationEngine(store)
    for success in (True, False):
        result = learning.record(
            FlowOutcomeRecord(
                relation_id="r2",
                origin_flow="A",
                target_flow="B",
                outcome="PASS" if success else "REJECT",
                success=success,
            )
        )
    assert result.status == "REVIEW_REQUIRED"
    assert result.success_rate == 0.5

def test_repeatable_flow_becomes_learning_candidate_only():
    store = SQLiteFlowLearningStore(":memory:")
    learning = FlowAdaptationEngine(store)
    for index in (1, 2):
        learning.record(
            FlowOutcomeRecord(
                relation_id="r-candidate",
                origin_flow="CONTROLLED_TEST",
                target_flow="MEASURED_GAIN",
                outcome="PASS",
                success=True,
                evidence_refs=(f"e{index}",),
                provenance_refs=("source",),
            )
        )

    candidate = learning.learning_candidate("r-candidate")
    assert candidate is not None
    assert candidate["promotion_state"] == "candidate_only"
    assert candidate["observations"] == 2
    assert candidate["success_rate"] == 1.0
    assert candidate["evidence_refs"] == ("e1", "e2")
    assert candidate["provenance_refs"] == ("source",)


def test_flow_learning_candidate_requires_evidence_and_provenance():
    store = SQLiteFlowLearningStore(":memory:")
    learning = FlowAdaptationEngine(store)
    for _ in (1, 2):
        learning.record(
            FlowOutcomeRecord(
                relation_id="r-incomplete",
                origin_flow="A",
                target_flow="B",
                outcome="PASS",
                success=True,
            )
        )
    assert learning.learning_candidate("r-incomplete") is None
