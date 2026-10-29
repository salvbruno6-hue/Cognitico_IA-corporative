from pathlib import Path


MIGRATION = Path(
    "supabase/migrations/20261029013000_pcp_requisito_fisico_fluxo_modelo_nulls_last.sql"
)


def test_followup_migration_reconciles_model_specific_null_ordering():
    sql = MIGRATION.read_text(encoding="utf-8")
    assert "(fp.modelo_id=r.modelo_id) desc nulls last" in sql
    assert "fp.modelo_id=r.modelo_id or fp.modelo_id is null" in sql
    assert "with (security_invoker = true)" in sql
    assert "revoke all on public.v_elo_pcp_requisito_fisico_planejamento from anon, authenticated" in sql
