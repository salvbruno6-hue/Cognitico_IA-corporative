"""Teste da Política B (ADR-0015)."""
from __future__ import annotations
import pytest
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback
from elo.cognitive.runtime.crl import CRLContext
from elo.cognitive.runtime.handlers.learn import learn_handler

@pytest.fixture(autouse=True)
def _isolate_memory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "memory" / "cognitive").mkdir(parents=True)

def _attributed_lifecycle() -> DecisionLifecycle:
    lc = DecisionLifecycle(DecisionRecord("DEC_X", "d", "r", expected_outcome="ok"))
    lc.transition(DecisionState.APPROVED)
    lc.transition(DecisionState.EXECUTED)
    lc.transition(DecisionState.OBSERVING)
    lc.attach_outcome(OutcomeFeedback("DEC_X", "ok", "ok", evidence_ids=("e1",)))
    lc.transition(DecisionState.EVALUATED, evidence_ids=("e1",))
    lc.attach_attribution({"decision": 1.0})
    lc.transition(DecisionState.ATTRIBUTED, evidence_ids=("e1",))
    return lc

def test_learn_escalates_without_symbiont():
    lc = _attributed_lifecycle()
    ctx = CRLContext(request_id="test")
    ctx.stage_results["lifecycle"] = lc
    learn_handler(ctx)
    assert lc.state == DecisionState.ESCALATED
    assert ctx.stage_results["escalation"]["reason"] == "symbiont_required_for_learning"
