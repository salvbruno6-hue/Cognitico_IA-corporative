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


def test_synthesis_handles_accents():
    """Garante que 'módulos' casa com tag 'modulos'."""
    engine = SynthesisEngine()
    delta = engine.synthesize(
        external_analysis="A manutenção contempla os módulos",
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
    aligned_summaries = [i.summary for i in delta.aligned]
    assert any("modulos" in s for s in aligned_summaries), (
        f"esperado 'modulos' em aligned, obtido: {aligned_summaries}"
    )


def test_synthesis_handles_both_directions():
    """Análise sem acento, tag com acento — também deve casar."""
    engine = SynthesisEngine()
    delta = engine.synthesize(
        external_analysis="A manutencao cobre tudo",
        so_context={
            "so_id": "SO-155.26",
            "learning": {
                "so_id": "SO-155.26",
                "tags": ["manutenção"],
            },
            "handbook": [],
            "precedents": [],
        },
    )
    aligned_summaries = [i.summary for i in delta.aligned]
    assert any("manutencao" in s for s in aligned_summaries)
