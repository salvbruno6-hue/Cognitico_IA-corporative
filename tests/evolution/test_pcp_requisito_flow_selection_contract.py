from pathlib import Path


MIGRATION = Path(
    "supabase/migrations/20261028140000_pcp_requisito_fisico_selecionar_fluxo_por_modelo.sql"
)


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def test_requisito_flow_selection_prefers_model_specific_then_general_fallback():
    sql = _sql()
    assert "fp.modelo_id=r.modelo_id or fp.modelo_id is null" in sql
    assert "(fp.modelo_id=r.modelo_id) desc" in sql
    assert "limit 1" in sql


def test_requisito_flow_metrics_are_scoped_to_selected_flow():
    sql = _sql()
    assert "left join public.fluxo_produtivo_modular_etapas e on e.fluxo_id=fp.id" in sql
    assert "from public.fluxo_produtivo_modular_etapas where upper(coalesce(status,''))='ATIVO'" not in sql


def test_requisito_view_preserves_security_and_fail_closed_capacity_readiness():
    sql = _sql()
    assert "with (security_invoker = true)" in sql
    assert "GAP_ROTEIRO_PRODUTIVO" in sql
    assert "GAP_TEMPO_FLUXO" in sql
    assert "GAP_CAPACIDADE_FLUXO" in sql
    assert "revoke all on public.v_elo_pcp_requisito_fisico_planejamento from anon, authenticated" in sql
