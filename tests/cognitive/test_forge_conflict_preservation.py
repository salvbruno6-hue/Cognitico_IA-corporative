from elo.cognitive.runtime.humanization.humanizer import Humanizer


def test_forge_humanizer_preserves_conflicting_source_observations():
    text = Humanizer().humanize(
        {
            "intent": "forge_consulta",
            "forge_context": {
                "entity": {"requested_reference": "M01"},
                "model": {"codigo": "M01", "nome": "Habitacional Amplo 20 pés", "ativo": True},
                "relationships": {},
                "governed_discovery": {
                    "sources_considered": [],
                    "linked_records": {},
                    "not_linked": [],
                    "conflicts": [
                        "modelos.nome='Habitacional Amplo 20 pés' diverge de outra fonte observada.",
                        "A segunda observação foi preservada sem seleção silenciosa.",
                    ],
                    "applicability": {"fluxo_produtivo_modular": []},
                },
            },
        }
    )

    assert "Conflitos preservados" in text
    assert "Habitacional Amplo 20 pés" in text
    assert "seleção silenciosa" in text
