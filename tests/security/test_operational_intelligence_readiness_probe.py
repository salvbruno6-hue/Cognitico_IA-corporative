from pathlib import Path


PROBE = Path("supabase/health/elo_operational_intelligence_readiness.sql")


def _source() -> str:
    return PROBE.read_text(encoding="utf-8").lower()


def test_operational_readiness_probe_is_read_only():
    source = _source()
    assert "operational_intelligence_readiness" in source
    for forbidden in (
        "insert into ",
        "update public.",
        "delete from ",
        "alter table ",
        "create table ",
        "drop table ",
        "grant ",
        "revoke ",
    ):
        assert forbidden not in source


def test_operational_readiness_probe_covers_closed_learning_loop():
    source = _source()
    for table in (
        "mt_demanda_historico",
        "mt_previsoes_demanda",
        "mt_regras_capacidade",
        "mt_capacidade_diaria",
        "mt_capacidade_componentes",
        "mt_necessidades_materiais",
        "mt_lotes_estoque",
        "mt_planos_pcp",
        "mt_linhas_plano_pcp",
        "mt_ordens_producao",
        "mt_operacoes_ordem_producao",
        "mt_eventos_fluxo_modular",
        "mt_unidades_modulares",
        "elo_aprendizado_pcp_planejamento",
        "elo_aprendizado_producao_fluxo_modular",
    ):
        assert table in source
