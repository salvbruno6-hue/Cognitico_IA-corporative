from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.precedent_index import PrecedentIndex
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback


def _closed_cycle() -> DecisionLifecycle:
    lifecycle = DecisionLifecycle(DecisionRecord("d1", "replan", "capacity gap", expected_outcome="reduce delay"))
    lifecycle.transition(DecisionState.APPROVED)
    lifecycle.transition(DecisionState.EXECUTED)
    lifecycle.transition(DecisionState.OBSERVING)
    lifecycle.attach_outcome(OutcomeFeedback("d1", "reduce delay", "delay reduced", evidence_ids=("e1",)))
    lifecycle.transition(DecisionState.EVALUATED, evidence_ids=("e1",))
    lifecycle.attach_attribution({"decision": 0.7, "external": 0.3})
    lifecycle.transition(DecisionState.ATTRIBUTED, evidence_ids=("e1",))
    lifecycle.attach_learning({"pattern": "capacity-aware replanning"})
    lifecycle.transition(DecisionState.LEARNED, evidence_ids=("e1",))
    lifecycle.transition(DecisionState.CLOSED, evidence_ids=("e1",))
    return lifecycle


def test_lifecycle_requires_ordered_outcome():
    lifecycle = DecisionLifecycle(DecisionRecord("d1", "replan", "gap"))
    lifecycle.transition(DecisionState.APPROVED)
    lifecycle.transition(DecisionState.EXECUTED)
    lifecycle.transition(DecisionState.OBSERVING)
    lifecycle.attach_outcome(OutcomeFeedback("d1", "ok", "ok", evidence_ids=("e1",)))
    lifecycle.transition(DecisionState.EVALUATED, evidence_ids=("e1",))
    assert lifecycle.state == DecisionState.EVALUATED


def test_invalid_transition_is_blocked():
    lifecycle = DecisionLifecycle(DecisionRecord("d1", "replan", "gap"))
    try:
        lifecycle.transition(DecisionState.CLOSED, evidence_ids=("e1",))
        assert False
    except ValueError:
        assert True


def test_closed_cycle_can_become_precedent():
    lifecycle = _closed_cycle()
    precedent = PrecedentIndex()
    precedent.add(lifecycle, domain="planning", context_keys=("capacity", "delay"), outcome_summary="delay reduced")
    assert precedent.find(domain="planning", context_keys=("capacity",))[0].decision_id == "d1"


class _SymbiontCandidate:
    candidate_id = "c1"
    experience_id = "x1"
    dataset_version = "ds1"
    hypothesis = "pattern"


class _SymbiontEvaluation:
    candidate = _SymbiontCandidate()
    evolution_classification = "COMPATIBLE"


class _SymbiontAdapter:
    def evaluate(self, observation, *, principal_id, dataset_version):
        assert observation.decision_id == "d1"
        assert principal_id == "p1"
        assert dataset_version == "ds1"
        return _SymbiontEvaluation()


def test_attributed_outcome_handoffs_to_existing_symbiont():
    lifecycle = DecisionLifecycle(DecisionRecord("d1", "replan", "gap", expected_outcome="ok"))
    lifecycle.transition(DecisionState.APPROVED)
    lifecycle.transition(DecisionState.EXECUTED)
    lifecycle.transition(DecisionState.OBSERVING)
    lifecycle.attach_outcome(OutcomeFeedback("d1", "ok", "ok", evidence_ids=("e1",)))
    lifecycle.transition(DecisionState.EVALUATED, evidence_ids=("e1",))
    lifecycle.attach_attribution({"decision": 1.0})
    lifecycle.transition(DecisionState.ATTRIBUTED, evidence_ids=("e1",))
    evaluation = lifecycle.handoff_to_symbiont(
        adapter=_SymbiontAdapter(),
        observation=type("Observation", (), {"decision_id": "d1", "evidence_ids": ("e1",)})(),
        principal_id="p1",
        dataset_version="ds1",
    )
    assert evaluation.candidate.candidate_id == "c1"
    assert lifecycle.state == DecisionState.LEARNED
    assert lifecycle.learning_candidate["candidate_id"] == "c1"


def test_symbiont_handoff_preserves_decision_pattern_provenance():
    from elo.cognitive.symbionte_lab import SymbiontLabObservation

    lifecycle = DecisionLifecycle(DecisionRecord("d-pattern", "replan", "gap", expected_outcome="ok"))
    lifecycle.transition(DecisionState.APPROVED)
    lifecycle.transition(DecisionState.EXECUTED)

    outcome = __import__("elo.core.execution_boundary", fromlist=["ExecutionOutcome", "ExecutionStatus"]).ExecutionOutcome(
        request_id="exec-pattern-1",
        status=__import__("elo.core.execution_boundary", fromlist=["ExecutionStatus"]).ExecutionStatus.EXECUTED,
        executed=True,
        reason="completed",
        provenance={"source_commit": "commit-pattern"},
        evidence_ids=("e-pattern",),
        correlation_id="d-pattern",
        occurred_at=__import__("datetime").datetime(2026, 9, 30),
        decision_pattern_candidate_ref="PATTERN-REF-1",
    )

    observation = SymbiontLabObservation.from_execution_outcome(
        outcome,
        decision_id="d-pattern",
        domain="ORCAMENTO",
        expected_outcome="ok",
        observed_outcome="ok",
        hypothesis="pattern",
        baseline="before",
        experiment="paired",
        result="validated",
        regression_status="PASS",
        generalization_status="CONFIRMED",
        risk="LOW",
        existing_owner=None,
        scope="tenant-a",
        tenant_id="tenant-a",
        observation_id="obs-pattern-1",
        source_commit="commit-pattern",
    )

    assert observation.decision_pattern_candidate_ref == "PATTERN-REF-1"
