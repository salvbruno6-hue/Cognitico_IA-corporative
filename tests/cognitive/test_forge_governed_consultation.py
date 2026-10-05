from elo.application.use_cases.orchestrator import GovernedOrchestrator, OrchestrationRequest


class FakeForge:
    def governed_model_context(self, reference, query):
        assert reference == "M01"
        return {
            "entity": {"requested_reference": reference, "canonical_code": "M01", "model_id": "model-01"},
            "model": {"id": "model-01", "codigo": "M01", "nome": "Habitacional Amplo 20 pés", "ativo": True},
            "relationships": {
                "taxonomia": [{"codigo": "MLT.M01"}],
                "dimensoes": [{"referencia": "20 pés"}],
                "kits": [{"id": "kit-01"}, {"id": "kit-02"}],
                "kit_itens": [{"id": f"item-{i}"} for i in range(59)],
                "lista_mae": [{"id": f"lista-{i}"} for i in range(42)],
                "estrutura_modular": [],
            },
            "governed_discovery": {
                "query": query,
                "linked_records": {
                    "fluxo_produtivo_modular": [{"id": "flow-01", "modelo_id": None}],
                    "fluxo_produtivo_modular_etapas": [{"id": f"stage-{i}", "fluxo_id": "flow-01"} for i in range(17)],
                },
                "not_linked": [
                    {"table_name": "elo_sim_demanda", "reason": "no_safe_relationship_to_model"},
                    {"table_name": "fornecedores", "reason": "no_safe_relationship_to_model"},
                ],
                "catalog_authority": "elo_aprendizado_fontes",
                "learning_performed": False,
            },
            "provenance": {"read_only": True, "guessed": False},
        }


def test_orchestrator_consult_forge_returns_human_response_and_evidence():
    orchestrator = GovernedOrchestrator()
    request = OrchestrationRequest(
        tenant_id="test-tenant",
        principal_id="test-principal",
        domain="forge",
        objective="Me explique o M01, o que temos para produzi-lo e o que está faltando.",
        correlation_id="corr-01",
    )

    response = orchestrator.consult_forge(request, FakeForge())

    assert response.status == "CONSULTED"
    assert response.stage == "ANALYZE"
    assert response.evidence_state == "OBSERVED"
    assert "M01" in response.response
    assert "17 etapa" in response.response
    assert "não há fluxo produtivo específico" in response.response.lower()
    assert "elo_sim_demanda" in response.response
    assert "fornecedores" in response.response
    assert "aprendizado ou promoção" in response.response.lower()


def test_orchestrator_forge_consultation_does_not_create_learning_path():
    orchestrator = GovernedOrchestrator()
    request = OrchestrationRequest(
        tenant_id="test-tenant",
        principal_id="test-principal",
        domain="forge",
        objective="Explique o M01.",
        correlation_id="corr-02",
    )

    response = orchestrator.consult_forge(request, FakeForge())

    assert response.capability == "forge_operational_knowledge"
    assert response.next_action
