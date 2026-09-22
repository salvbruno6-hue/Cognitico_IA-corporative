"""Testes de humanização de diretrizes."""
from elo.cognitive.runtime.humanization.humanizer import Humanizer


def test_humanizer_shows_directives():
    h = Humanizer()
    text = h.humanize({
        "intent": "confere_analise",
        "delta": {
            "so_id": "SO-155.26",
            "aligned": [{"summary": "módulos"}],
            "improvements": [],
            "corrections": [],
            "conflicts": [],
            "overall_confidence": 0.7,
            "directives": [
                {
                    "id": "DIR-001",
                    "question": "Confirme a premissa de 30%",
                    "why": "Aprendizado menciona mas não confirmada",
                    "priority": "high",
                },
            ],
        },
        "decision_brief": {"recommendation": "considerar_melhorias"},
    })
    assert "preciso confirmar" in text.lower()
    assert "Confirme a premissa de 30%" in text


def test_humanizer_sem_directives():
    h = Humanizer()
    text = h.humanize({
        "intent": "confere_analise",
        "delta": {
            "so_id": "SO-155.26",
            "aligned": [{"summary": "módulos"}],
            "improvements": [],
            "corrections": [],
            "conflicts": [],
            "overall_confidence": 0.7,
            "directives": [],
        },
        "decision_brief": {"recommendation": "alinhado_prosseguir"},
    })
    assert "preciso confirmar" not in text.lower()
