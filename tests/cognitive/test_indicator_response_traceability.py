from elo.cognitive.response.intelligent_orchestration_response import OrchestrationResponseComposer


def test_indicator_response_separates_operational_indicator_from_formal_kpi():
    context = {
        "indicator_context": {
            "formal_kpi_state": "SEM_KPI_FORMAL_REGISTRADO",
            "kpi_definition_count": 0,
            "kpi_snapshot_count": 0,
            "automatic_kpi_promotion": False,
            "catalog_authority": "elo_aprendizado_fontes",
        },
        "governed_discovery": {
            "linked_records": {
                "v_elo_pcp_carga_capacidade_periodo": [],
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
            }
        },
    }

    rendered = OrchestrationResponseComposer._append_indicator_context("base", context)

    assert "v_elo_pcp_carga_capacidade_periodo" in rendered
    assert "sem atividade operacional mensurável" in rendered
    assert "não equivale a KPI com valor zero" in rendered
    assert "nenhum registro em `mt_definicoes_kpi`" in rendered
    assert "promoção automática a KPI=false" in rendered


def test_indicator_response_renders_capacity_with_source_traceability():
    context = {
        "indicator_context": {
            "formal_kpi_state": "KPI_FORMAL_REGISTRADO",
            "kpi_definition_count": 1,
            "automatic_kpi_promotion": False,
            "catalog_authority": "elo_aprendizado_fontes",
        },
        "governed_discovery": {
            "linked_records": {
                "v_elo_pcp_carga_capacidade_periodo": [
                    {
                        "data_referencia": "2026-10-09",
                        "centro_trabalho_codigo": "CT-01",
                        "carga_horas_planejada": 6,
                        "capacidade_disponivel": 8,
                        "folga_horas": 2,
                        "utilizacao_pct": 75,
                        "excesso_carga": False,
                    }
                ],
                "v_elo_pcp_indicadores_montagem_externa": [],
                "mt_definicoes_kpi": [
                    {
                        "codigo_kpi": "PCP-UTIL-001",
                        "nome": "Utilização de capacidade",
                        "unidade": "%",
                        "formula": "carga/capacidade",
                    }
                ],
            }
        },
    }

    rendered = OrchestrationResponseComposer._append_indicator_context("base", context)

    assert "2026-10-09 / CT-01" in rendered
    assert "utilização=75%" in rendered
    assert "excesso_carga=False" in rendered
    assert "PCP-UTIL-001" in rendered
    assert "Utilização de capacidade" in rendered
    assert "elo_aprendizado_fontes" in rendered
