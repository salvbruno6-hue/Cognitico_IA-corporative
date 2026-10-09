from elo.cognitive import CognitiveCore
from elo.interface.contracts import CognitiveRequest
from elo.interface.response import ResponseBuilder


class IndicatorForge:
    def governed_demand_context(self, query):
        return {
            "source": "supabase_elo_forge",
            "query": query,
            "indicator_context": {
                "state": "CONSULTED",
                "formal_kpi_state": "SEM_KPI_FORMAL_REGISTRADO",
                "kpi_definition_count": 0,
                "kpi_snapshot_count": 0,
                "automatic_kpi_promotion": False,
                "catalog_authority": "elo_aprendizado_fontes",
                "read_only": True,
            },
            "governed_discovery": {
                "sources_considered": [
                    {
                        "table_name": "v_elo_pcp_carga_capacidade_periodo",
                        "dominio_codigo": "planejamento_pcp",
                        "prioridade": 116,
                    },
                    {
                        "table_name": "v_elo_pcp_indicadores_montagem_externa",
                        "dominio_codigo": "operacoes_externas",
                        "prioridade": 117,
                    },
                    {
                        "table_name": "mt_definicoes_kpi",
                        "dominio_codigo": "gestao_indicadores",
                        "prioridade": 118,
                    },
                ],
                "linked_records": {
                    "v_elo_pcp_carga_capacidade_periodo": [
                        {
                            "data_referencia": "2026-10-09",
                            "centro_trabalho_id": "ct-01",
                            "centro_trabalho_codigo": "CT-01",
                            "centro_trabalho_nome": "Montagem",
                            "unidade_capacidade": "horas",
                            "quantidade_planejada": 2,
                            "carga_horas_planejada": 6,
                            "capacidade_disponivel": 8,
                            "capacidade_padrao": 8,
                            "capacidade_recuperacao": 0,
                            "capacidade_bloqueada": 0,
                            "folga_horas": 2,
                            "utilizacao_pct": 75,
                            "excesso_carga": False,
                        }
                    ],
                    "v_elo_pcp_indicadores_montagem_externa": [
                        {
                            "ordens_total": 0,
                            "ordens_abertas": 0,
                            "ordens_atrasadas": 0,
                            "modulos_total": 0,
                            "colaboradores_alocados": 0,
                            "funcoes_ativas": 0,
                            "horas_planejadas_ordens": 0,
                            "horas_realizadas_ordens": 0,
                            "horas_planejadas_equipe": 0,
                            "horas_mao_obra_realizadas": 0,
                            "aderencia_horas_pct": None,
                        }
                    ],
                    "mt_definicoes_kpi": [],
                    "mt_snapshots_kpi": [],
                },
                "not_scoped": [],
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


def test_indicator_evidence_reaches_cognitive_response_api(monkeypatch):
    monkeypatch.setattr(
        "elo.infrastructure.forge_runtime.load_forge_adapter",
        lambda: IndicatorForge(),
    )
    request = CognitiveRequest(
        tenant_id="tenant-a",
        principal_id="principal-a",
        domain="planejamento_pcp",
        message="Quais indicadores de capacidade e KPIs estão afetados?",
        context={"forge_enabled": True},
    )

    result = CognitiveCore().process(request)
    response = ResponseBuilder().build(request, "session-a", result)

    assert result["response"]["type"] == "forge_grounded_analysis"
    assert "Indicadores governados" in result["response"]["content"]
    assert "v_elo_pcp_carga_capacidade_periodo" in result["response"]["content"]
    assert "utilização=75%" in result["response"]["content"]
    assert "nenhum registro em `mt_definicoes_kpi`" in result["response"]["content"]
    assert result["provenance"]["evidence_refs"]
    assert response.provenance.evidence_refs == result["provenance"]["evidence_refs"]
    assert response.provenance.provider == "supabase_elo_forge"
    assert response.response["type"] == "forge_grounded_analysis"
