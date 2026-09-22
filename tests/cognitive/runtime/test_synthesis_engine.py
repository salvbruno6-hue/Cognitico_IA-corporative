"""Testes do motor de síntese."""
from elo.cognitive.runtime.synthesis.engine import SynthesisEngine


def test_synthesis_detects_alignment():
    engine = SynthesisEngine()
    delta = engine.synthesize(
        external_analysis="A manutenção contempla os 24 módulos",
        so_context={
            "so_id": "SO-155.26",
            "learning": {
                "so_id": "SO-155.26",
                "tags": ["modulos", "manutencao"],
            },
            "handbook": [],
            "precedents": [],
        },
    )
    assert any("modulos" in i.summary for i in delta.aligned)


def test_synthesis_detects_missing():
    engine = SynthesisEngine()
    delta = engine.synthesize(
        external_analysis="Análise qualquer",
        so_context={
            "so_id": "SO-155.26",
            "learning": {
                "so_id": "SO-155.26",
                "tags": ["manutencao", "esquadrias"],
            },
            "handbook": [],
            "precedents": [],
        },
    )
    assert len(delta.improvements) >= 2


def test_synthesis_empty_context():
    engine = SynthesisEngine()
    delta = engine.synthesize(
        external_analysis="qualquer",
        so_context={"so_id": None, "learning": None, "handbook": [], "precedents": []},
    )
    assert delta.overall_confidence < 0.5
