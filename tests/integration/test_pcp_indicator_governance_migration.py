from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MIGRATION = ROOT / "supabase" / "migrations" / "20261009110000_govern_forge_pcp_indicator_kpi_sources.sql"


def test_pcp_indicator_governance_migration_is_read_only_catalog_registration():
    sql = MIGRATION.read_text(encoding="utf-8")

    for source in (
        "v_elo_pcp_carga_capacidade_periodo",
        "v_elo_pcp_indicadores_montagem_externa",
        "mt_definicoes_kpi",
        "mt_snapshots_kpi",
    ):
        assert source in sql

    assert "insert into public.elo_aprendizado_fontes" in sql.lower()
    assert '"somente_leitura":true' in sql
    assert '"preservar_proveniencia":true' in sql
    assert '"nao_promover_a_kpi":true' in sql
    assert '"autoridade_kpi_formal":true' in sql
    assert '"nao_criar_kpi":true' in sql

    lowered = sql.lower()
    assert "insert into public.mt_definicoes_kpi" not in lowered
    assert "insert into public.mt_snapshots_kpi" not in lowered
    assert "update public.mt_definicoes_kpi" not in lowered
    assert "update public.mt_snapshots_kpi" not in lowered
    assert "delete from public.mt_definicoes_kpi" not in lowered
    assert "delete from public.mt_snapshots_kpi" not in lowered
