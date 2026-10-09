from elo.infrastructure.governed_indicator_forge import GovernedIndicatorForge


class FakeForge:
    def __init__(self, sources, rows):
        self._sources = sources
        self._rows = rows

    def governed_sources(self):
        return self._sources

    def read_table(self, table, **kwargs):
        return list(self._rows.get(table, []))

    def governed_demand_context(self, query):
        return {
            "source": "fake",
            "query": query,
            "governed_discovery": {
                "sources_considered": [],
                "linked_records": {},
                "catalog_authority": "elo_aprendizado_fontes",
                "learning_performed": False,
                "scope": "cross_domain_demand_and_impacts",
            },
            "provenance": {
                "source": "fake",
                "read_only": True,
                "guessed": False,
            },
        }


def source(table, source_type, domain="planejamento_pcp", priority=116, **rule):
    extraction_rule = {
        "tipo": source_type,
        "somente_leitura": True,
        "preservar_proveniencia": True,
        **rule,
    }
    return {
        "schema_name": "public",
        "table_name": table,
        "dominio_codigo": domain,
        "prioridade": priority,
        "enabled": True,
        "extracao_ativa": True,
        "regra_extracao": extraction_rule,
    }


def test_indicator_query_reads_only_catalog_governed_indicator_sources():
    sources = [
        source(
            "v_elo_pcp_carga_capacidade_periodo",
            "read_model_indicador_capacidade",
            nao_promover_a_kpi=True,
        ),
        source(
            "v_elo_pcp_indicadores_montagem_externa",
            "read_model_indicadores_montagem_externa",
            domain="operacoes_externas",
            priority=117,
            nao_promover_a_kpi=True,
        ),
        source("modelos", "cadastro_produto", domain="produtos", priority=1),
    ]
    rows = {
        "v_elo_pcp_carga_capacidade_periodo": [
            {"centro_trabalho": "CT-01", "utilizacao_pct": 85, "excesso_carga": False}
        ],
        "v_elo_pcp_indicadores_montagem_externa": [
            {"ordens_total": 2, "ordens_atrasadas": 1, "aderencia_horas_pct": 90}
        ],
        "modelos": [{"codigo": "M01"}],
    }

    result = GovernedIndicatorForge(FakeForge(sources, rows)).governed_demand_context(
        "Quais indicadores de capacidade e montagem externa estão afetados?"
    )

    linked = result["governed_discovery"]["linked_records"]
    assert "v_elo_pcp_carga_capacidade_periodo" in linked
    assert "v_elo_pcp_indicadores_montagem_externa" in linked
    assert "modelos" not in linked
    assert result["indicator_context"]["automatic_kpi_promotion"] is False
    assert result["indicator_context"]["formal_kpi_state"] == "REGISTRO_KPI_NAO_GOVERNADO"


def test_empty_kpi_registry_blocks_automatic_kpi_claim():
    sources = [
        source("mt_definicoes_kpi", "kpi_definition_registry", domain="gestao_indicadores", priority=118),
        source("mt_snapshots_kpi", "kpi_snapshot_registry", domain="gestao_indicadores", priority=119),
    ]
    result = GovernedIndicatorForge(FakeForge(sources, {})).governed_demand_context(
        "Quais KPIs estão afetados?"
    )

    indicator = result["indicator_context"]
    assert indicator["formal_kpi_state"] == "SEM_KPI_FORMAL_REGISTRADO"
    assert indicator["kpi_definition_count"] == 0
    assert indicator["kpi_snapshot_count"] == 0
    assert indicator["automatic_kpi_promotion"] is False


def test_registered_kpi_is_reported_without_creating_or_promoting_it():
    sources = [
        source("mt_definicoes_kpi", "kpi_definition_registry", domain="gestao_indicadores", priority=118),
        source("mt_snapshots_kpi", "kpi_snapshot_registry", domain="gestao_indicadores", priority=119),
    ]
    rows = {
        "mt_definicoes_kpi": [
            {
                "id": "kpi-1",
                "codigo_kpi": "PCP-UTIL-001",
                "nome": "Utilização de capacidade",
                "formula": "carga/capacidade",
            }
        ],
        "mt_snapshots_kpi": [
            {"id": "snap-1", "kpi_id": "kpi-1", "data_referencia": "2026-10-09", "valor": 85}
        ],
    }
    result = GovernedIndicatorForge(FakeForge(sources, rows)).governed_demand_context(
        "Mostre o KPI de utilização e seus indicadores."
    )

    indicator = result["indicator_context"]
    assert indicator["formal_kpi_state"] == "KPI_FORMAL_REGISTRADO"
    assert indicator["kpi_definition_count"] == 1
    assert indicator["kpi_snapshot_count"] == 1
    assert indicator["automatic_kpi_promotion"] is False


def test_non_indicator_query_preserves_base_context_without_extra_reads():
    base = FakeForge(
        [source("mt_definicoes_kpi", "kpi_definition_registry", domain="gestao_indicadores")],
        {"mt_definicoes_kpi": [{"id": "kpi-1"}]},
    )
    result = GovernedIndicatorForge(base).governed_demand_context("Qual é o modelo M01?")

    assert "indicator_context" not in result
    assert result["governed_discovery"]["linked_records"] == {}
