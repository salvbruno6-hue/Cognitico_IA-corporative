"""Teste de ciclo completo do CRL com persistência."""
from __future__ import annotations
from pathlib import Path
import pytest
from elo.cognitive.runtime.bootstrap import build_default_crl
from elo.cognitive.runtime.crl import CRLContext

@pytest.fixture(autouse=True)
def _isolate_memory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "memory" / "cognitive").mkdir(parents=True)

def test_crl_escalates_when_no_symbiont():
    crl = build_default_crl()
    ctx = CRLContext(request_id="test-1")
    ctx.payload.update({"question":"reduce cost in logistics","domain":"planning","context_keys":("capacity","delay"),"evidence_ids":("e1",),"approver":"human-1","outcome":{"expected":"reduce 10%","observed":"reduced 8%","evidence_ids":("e1",)},"attribution":{"decision":0.8,"external":0.2}})
    result = crl.run(ctx)
    escalation = result.stage_results.get("escalation")
    assert escalation is not None
    assert escalation["stage"] == "learn"
    assert escalation["reason"] == "symbiont_required_for_learning"

def test_crl_persists_lifecycle():
    crl = build_default_crl()
    ctx = CRLContext(request_id="test-2")
    ctx.payload.update({"question":"reduce cost","domain":"planning","context_keys":("capacity",),"evidence_ids":("e1",),"approver":"human-1","decision_id":"DEC_2026_9999"})
    crl.run(ctx)
    p = Path("memory/cognitive/decisions/DEC_2026_9999/lifecycle.json")
    assert p.exists()
