"""Teste de ida-e-volta dos serializadores."""
from __future__ import annotations
from elo.core.calibration import CalibrationObservation, ConfidenceCalibration
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.precedent_index import PrecedentIndex
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback
from elo.cognitive.runtime.serialization import calibration_serializer, decision_serializer, precedent_serializer

def test_decision_roundtrip():
    lc = DecisionLifecycle(DecisionRecord("DEC_1", "d", "r"))
    lc.transition(DecisionState.APPROVED)
    restored = decision_serializer.deserialize(decision_serializer.serialize(lc))
    assert restored.decision.decision_id == "DEC_1"
    assert restored.state == DecisionState.APPROVED

def test_calibration_roundtrip():
    c = ConfidenceCalibration()
    c.add(CalibrationObservation(0.8, 1.0, "d1"))
    restored = calibration_serializer.from_dict(calibration_serializer.to_dict(c))
    assert len(restored.observations()) == 1

def test_precedent_roundtrip():
    lc = DecisionLifecycle(DecisionRecord("DEC_2", "d", "r", expected_outcome="ok"))
    lc.transition(DecisionState.APPROVED)
    lc.transition(DecisionState.EXECUTED)
    lc.transition(DecisionState.OBSERVING)
    lc.attach_outcome(OutcomeFeedback("DEC_2", "ok", "ok", evidence_ids=("e1",)))
    lc.transition(DecisionState.EVALUATED, evidence_ids=("e1",))
    lc.attach_attribution({"decision": 1.0})
    lc.transition(DecisionState.ATTRIBUTED, evidence_ids=("e1",))
    lc.attach_learning({"pattern":"x"})
    lc.transition(DecisionState.LEARNED, evidence_ids=("e1",))
    lc.transition(DecisionState.CLOSED, evidence_ids=("e1",))
    idx = PrecedentIndex()
    idx.add(lc, domain="planning", context_keys=("capacity",), outcome_summary="ok")
    p = list(idx._items.values())[0]
    restored = precedent_serializer.from_dict(precedent_serializer.to_dict(p))
    assert restored.decision_id == "DEC_2"
