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
