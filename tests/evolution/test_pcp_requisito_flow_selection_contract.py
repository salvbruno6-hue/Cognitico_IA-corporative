from pathlib import Path


MIGRATION = Path(
    "supabase/migrations/20261028140000_pcp_requisito_fisico_selecionar_fluxo_por_modelo.sql"
)


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def _select_flow(requirement_model_id: str, flows: list[dict[str, object]]) -> dict[str, object]:
    candidates = [
        flow
        for flow in flows
        if flow["active"]
        and (flow["model_id"] == requirement_model_id or flow["model_id"] is None)
    ]
    return sorted(
        candidates,
        key=lambda flow: (
            flow["model_id"] != requirement_model_id,
            str(flow["version"]),
            str(flow["code"]),
        ),
    )[0]


def test_requisito_flow_selection_prefers_model_specific_then_general_fallback():
    sql = _sql()
    assert "fp.modelo_id=r.modelo_id or fp.modelo_id is null" in sql
    assert "(fp.modelo_id=r.modelo_id) desc nulls last" in sql
    assert "limit 1" in sql


def test_model_specific_flow_wins_when_general_and_specific_are_both_active():
    flows = [
        {
            "code": "MLT.PROD.PADRAO.V2",
            "model_id": None,
            "version": "2.0",
            "active": True,
        },
        {
            "code": "MLT.PROD.M16.NAO_CUSTOMIZAVEL.V1",
            "model_id": "MLT.M16",
            "version": "1.0",
            "active": True,
        },
    ]
    selected = _select_flow("MLT.M16", flows)
    assert selected["code"] == "MLT.PROD.M16.NAO_CUSTOMIZAVEL.V1"


def test_general_flow_is_used_when_model_has_no_specific_active_flow():
    flows = [
        {
            "code": "MLT.PROD.PADRAO.V2",
            "model_id": None,
            "version": "2.0",
            "active": True,
        },
        {
            "code": "MLT.PROD.M16.NAO_CUSTOMIZAVEL.V1",
            "model_id": "MLT.M16",
            "version": "1.0",
            "active": True,
        },
    ]
    selected = _select_flow("M01", flows)
    assert selected["code"] == "MLT.PROD.PADRAO.V2"


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
