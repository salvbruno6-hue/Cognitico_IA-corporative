from elo.cognitive import CognitiveCore
from elo.interface.contracts import CognitiveRequest


class FakeForge:
    def governed_model_context(self, reference, query):
        assert reference == "M01"
        return {
            "entity": {"requested_reference": "M01", "model_id": "model-01"},
            "model": {"id": "model-01", "codigo": "M01", "nome": "Habitacional Amplo 20 pés", "ativo": True},
            "relationships": {
                "taxonomia": [{"id": "tax-01", "codigo": "MLT.M01"}],
                "dimensoes": [{"id": "dim-01", "referencia": "20 pés"}],
                "kits": [{"id": "kit-01"}],
                "kit_itens": [{"id": "item-01"}],
                "lista_mae": [{"id": "lista-01"}],
                "estrutura_modular": [],
            },
            "governed_discovery": {
                "linked_records": {},
                "not_linked": [],
                "applicability": {"fluxo_produtivo_modular": []},
            },
            "provenance": {"read_only": True, "guessed": False},
        }


def test_cognitive_core_routes_human_question_to_governed_forge(monkeypatch):
    monkeypatch.setattr(
        "elo.infrastructure.forge_runtime.load_forge_adapter",
        lambda: FakeForge(),
    )
    core = CognitiveCore()
    result = core.process(
        CognitiveRequest(
            tenant_id="tenant-a",
            principal_id="principal-a",
            domain="produtos",
            message="Me explique o M01.",
            context={"forge_enabled": True},
        )
    )

    assert result["response"]["type"] == "forge_grounded_analysis"
    assert "M01" in result["response"]["content"]
    assert result["provenance"]["policy_decision"] == "READ_ONLY_GOVERNED_SOURCE_SELECTION"
    assert result["provenance"]["evidence_refs"]
