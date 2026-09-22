"""Testes do analyze handler."""
from elo.cognitive.runtime.crl import CRLContext
from elo.cognitive.runtime.handlers.analyze import analyze_handler


def test_analyze_produces_delta():
    ctx = CRLContext(request_id="t1")
    ctx.payload["chatgpt_analysis"] = "manutenção dos módulos"
    ctx.stage_results["so_context"] = {
        "so_id": "SO-155.26",
        "learning": {"so_id": "SO-155.26", "tags": ["manutencao", "modulos"]},
        "handbook": [],
        "precedents": [],
    }
    analyze_handler(ctx)
    assert "delta" in ctx.stage_results
    delta = ctx.stage_results["delta"]
    assert delta.so_id == "SO-155.26"
