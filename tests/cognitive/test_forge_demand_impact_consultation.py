from elo.application.use_cases.orchestrator import GovernedOrchestrator, OrchestrationRequest


class DemandForge:
    def governed_demand_context(self, query):
        return {
            "source": "supabase_elo_forge",
            "query": query,
            "governed_discovery": {
                "sources_considered": [
                    {"table_name": "v_elo_pcp_cobertura_demanda_externa", "dominio_codigo": "planejamento_pcp", "prioridade": 112},
                    {"table_name": "v_elo_pcp_decisao_externa_resumo", "dominio_codigo": "operacoes_externas", "prioridade": 114},
                    {"table_name": "v_elo_pcp_dialogo_regras", "dominio_codigo": "planejamento_pcp", "prioridade": 115},
                    {"table_name": "mt_ordens_reparo", "dominio_codigo": "reparos_modulares", "prioridade": 104},
                ],
                "linked_records": {
                    "v_elo_pcp_cobertura_demanda_externa": [{"estado_cobertura": "SEM_PREVISAO"}],
                    "v_elo_pcp_decisao_externa_resumo": [{"estado_decisao": "AGUARDANDO_HISTORICO"}],
                    "v_elo_pcp_dialogo_regras": [{"gap_codigo": "SEM_HISTORICO", "bloqueia_execucao": True}],
                },
                "not_scoped": [
                    {"table_name": "mt_ordens_reparo", "reason": "model_or_entity_scope_required"},
                    {"table_name": "elo_orcamento_decisoes", "dominio_codigo": "comercial_licitacoes", "prioridade": 11},
                ],
                "catalog_authority": "elo_aprendizado_fontes",
                "learning_performed": False,
                "scope": "cross_domain_demand_and_impacts",
            },
            "provenance": {
                "source": "Supabase Elo-forge",
                "governed_catalog": "elo_aprendizado_fontes",
                "read_only": True,
                "guessed": False,
                "learning_performed": False,
            },
        }


def test_orchestrator_consults_cross_domain_demand_without_model_reference():
    orchestrator = GovernedOrchestrator()
    request = OrchestrationRequest(
        tenant_id="test-tenant",
        principal_id="test-principal",
        domain="planejamento",
        objective=(
            "Quais são as demandas de fabricação, demanda comercial, "
            "demanda de reparos e demanda de operações externas e quais impactos "
            "elas apresentam?"
        ),
        correlation_id="corr-demand-01",
    )

    response = orchestrator.consult_forge(request, DemandForge())

    assert response.status == "CONSULTED"
    assert response.stage == "ANALYZE"
    assert response.evidence_state == "OBSERVED"
    assert "demanda e impactos entre domínios" in response.response.lower()
    assert "v_elo_pcp_cobertura_demanda_externa" in response.response
    assert "elo_orcamento_decisoes" in response.response
    assert "mt_ordens_reparo" in response.response
    assert "COMEÇO" in response.response
    assert "MEIO" in response.response
    assert "FIM" in response.response
    assert "DEM-001" in response.response
    assert "132" in response.response
    assert "65" in response.response
    assert "somente leitura" in response.response.lower()
    assert "não é interpretada como inexistência" in response.response.lower()


def test_cross_domain_consultation_does_not_require_m01():
    orchestrator = GovernedOrchestrator()
    request = OrchestrationRequest(
        tenant_id="test-tenant",
        principal_id="test-principal",
        domain="planejamento",
        objective="Avalie os impactos atuais das demandas sobre o PCP.",
        correlation_id="corr-demand-02",
    )

    response = orchestrator.consult_forge(request, DemandForge())

    assert response.status == "CONSULTED"
    assert response.model is None
    assert "M01" not in response.response
