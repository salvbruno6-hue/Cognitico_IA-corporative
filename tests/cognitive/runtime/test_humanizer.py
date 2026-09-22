"""Testes do humanizador."""
from elo.cognitive.runtime.humanization.humanizer import Humanizer


def test_o_que_sabe_with_learning():
    h = Humanizer()
    text = h.humanize({
        "intent": "o_que_sabe",
        "so_context": {
            "so_id": "SO-155.26",
            "learning": {
                "so_id": "SO-155.26",
                "tags": ["modulos", "manutencao"],
                "summary": "24 módulos, manutenção 6 meses",
            },
        },
    })
    assert "SO-155.26" in text
    assert "24 módulos" in text
    assert "pode evoluir" in text
    assert "Próximo passo" in text


def test_o_que_sabe_sem_learning():
    h = Humanizer()
    text = h.humanize({
        "intent": "o_que_sabe",
        "so_context": {"so_id": "SO-999.99", "learning": None},
    })
    assert "ainda não tem registro" in text
    assert "pode evoluir" in text


def test_confere_analise_com_delta():
    h = Humanizer()
    text = h.humanize({
        "intent": "confere_analise",
        "delta": {
            "so_id": "SO-155.26",
            "aligned": [{"summary": "módulos"}],
            "improvements": [{"summary": "esquadrias"}],
            "corrections": [],
            "conflicts": [],
            "overall_confidence": 0.7,
        },
        "decision_brief": {"recommendation": "considerar_melhorias"},
    })
    assert "alinhada" in text
    assert "Pontos positivos" in text
    assert "Ajustes sugeridos" in text


def test_lista_abertas_vazia():
    h = Humanizer()
    text = h.humanize({"intent": "lista_abertas", "count": 0, "items": []})
    assert "Não há decisões abertas" in text


def test_lista_abertas_com_items():
    h = Humanizer()
    text = h.humanize({
        "intent": "lista_abertas",
        "count": 2,
        "items": [
            {"decision_id": "DEC_1", "state": "approved"},
            {"decision_id": "DEC_2", "state": "observing"},
        ],
    })
    assert "2 decisões" in text
    assert "DEC_1" in text


def test_error():
    h = Humanizer()
    text = h.humanize({
        "error": "intent_not_recognized",
        "suggestions": ["ELO, o que você sabe sobre a SO X"],
    })
    assert "Houve um problema" in text
    assert "O ELO reconhece" in text


def test_nunca_contem_exclamacao():
    h = Humanizer()
    samples = [
        h.humanize({"intent": "o_que_sabe",
                    "so_context": {"so_id": "X", "learning": None}}),
        h.humanize({"intent": "lista_abertas", "count": 0, "items": []}),
        h.humanize({"intent": "status_decisao", "found": False}),
    ]
    for text in samples:
        assert "!" not in text


def test_nunca_contem_json():
    h = Humanizer()
    text = h.humanize({
        "intent": "o_que_sabe",
        "so_context": {
            "so_id": "SO-155.26",
            "learning": {"tags": ["a", "b"], "summary": "x"},
        },
    })
    assert "{" not in text
    assert "}" not in text
    assert "[" not in text


def test_sempre_tem_proximo_passo():
    h = Humanizer()
    samples = [
        h.humanize({"intent": "o_que_sabe",
                    "so_context": {"so_id": "X", "learning": None}}),
        h.humanize({"intent": "lista_abertas", "count": 0, "items": []}),
        h.humanize({"error": "x", "suggestions": []}),
    ]
    for text in samples:
        assert "Próximo passo" in text or "pode evoluir" in text
