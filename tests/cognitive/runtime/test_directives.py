"""Testes do gerador de diretrizes."""
from elo.cognitive.runtime.synthesis.directives import DirectiveGenerator


def test_generates_premise_directive():
    g = DirectiveGenerator()
    directives = g.generate(
        so_context={
            "so_id": "SO-155.26",
            "learning": {
                "so_id": "SO-155.26",
                "tags": ["manutencao", "premissa_30"],
                "summary": "manutenção 6 meses",
            },
        }
    )
    assert any("premissa" in d.question.lower() for d in directives)
    assert any(d.priority == "high" for d in directives)


def test_generates_temporal_directive():
    g = DirectiveGenerator()
    directives = g.generate(
        so_context={
            "so_id": "SO-134.26",
            "learning": {
                "so_id": "SO-134.26",
                "tags": ["preco"],
                "summary": "preço do aço registrado há 8 meses",
            },
        }
    )
    assert any("atualize" in d.question.lower() for d in directives)


def test_generates_correction_directive():
    g = DirectiveGenerator()
    directives = g.generate(
        so_context={"so_id": "SO-155.26", "learning": {"tags": []}},
        delta={
            "corrections": [
                {"summary": "ART/RRT não deve incidir sobre materiais"}
            ],
        },
    )
    assert any(d.source == "delta_correction" for d in directives)


def test_no_directives_when_clean():
    g = DirectiveGenerator()
    directives = g.generate(
        so_context={
            "so_id": "SO-155.26",
            "learning": {
                "so_id": "SO-155.26",
                "tags": ["modulos", "manutencao"],
                "summary": "24 módulos, manutenção 6 meses",
            },
        },
        delta={"corrections": []},
    )
    assert directives == []


def test_ids_are_sequential():
    g = DirectiveGenerator()
    directives = g.generate(
        so_context={
            "so_id": "SO-X",
            "learning": {
                "tags": ["premissa_a", "premissa_b"],
                "summary": "premissa a, premissa b",
            },
        },
    )
    ids = [d.id for d in directives]
    assert ids == sorted(ids)
    assert all(i.startswith("DIR-") for i in ids)


def test_to_dict_works():
    from elo.cognitive.runtime.synthesis.directives import Directive

    d = Directive(
        id="DIR-001",
        question="Q",
        why="W",
        priority="high",
        source="s",
        resolvable_by="human_confirmation",
        context_keys=["a"],
    )
    result = d.to_dict()
    assert result["id"] == "DIR-001"
    assert result["question"] == "Q"
    assert result["context_keys"] == ["a"]
