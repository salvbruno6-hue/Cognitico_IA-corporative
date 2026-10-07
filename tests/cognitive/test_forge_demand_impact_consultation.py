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
                    "elo_sim_demanda": [
                        {"demanda_id": "DEM-001", "descricao": "Demanda simulada 001", "quantidade": 100, "prazo_dias": 10, "prioridade": 3, "status": "ABERTA"},
                        {"demanda_id": "DEM-002", "descricao": "Demanda simulada 002", "quantidade": 24, "prazo_dias": 12, "prioridade": 3, "status": "ABERTA"},
                        {"demanda_id": "DEM-003", "descricao": "Demanda simulada 003", "quantidade": 8, "prazo_dias": 8, "prioridade": 5, "status": "ABERTA"},
                    ],
                    "elo_sim_demanda_materiais": [
                        {"demanda_id": "DEM-001", "material_id": "MAT-001", "quantidade_necessaria": 100},
                        {"demanda_id": "DEM-002", "material_id": "MAT-002", "quantidade_necessaria": 24},
                        {"demanda_id": "DEM-003", "material_id": "MAT-003", "quantidade_necessaria": 8},
                    ],
                    "elo_sim_demanda_recursos": [
                        {"demanda_id": "DEM-001", "recurso_id": "REC-001", "horas_demanda_h": 20},
                        {"demanda_id": "DEM-002", "recurso_id": "REC-002", "horas_demanda_h": 15},
                        {"demanda_id": "DEM-003", "recurso_id": "REC-001", "horas_demanda_h": 30},
                    ],
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
    assert response.evidence_refs
    assert response.orientation is not None
    assert response.orientation.evidence_refs
    assert response.orientation.confidence.value == "aligned"
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
    assert "MEMÓRIA NARRADA DO ORQUESTRADOR" in response.response
    assert "CLARIVIDÊNCIA OPERACIONAL" in response.response
    assert "condicional" in response.response.lower()
    assert "não é uma previsão" in response.response.lower()
    assert "somente leitura" in response.response.lower()
    assert "ELO APRENDER" in response.response
    assert "qual assunto pesquisar" in response.response
    assert "quais dados colher" in response.response
    assert "indicadores" in response.response
    assert "resultado posterior" in response.response
    assert "aprendizado governado" in response.response


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
