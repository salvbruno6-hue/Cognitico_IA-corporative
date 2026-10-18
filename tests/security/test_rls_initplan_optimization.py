from pathlib import Path
import re

MIGRATION = Path(
    "supabase/migrations/20261018203315_optimize_rls_auth_jwt_initplan.sql"
)

EXPECTED_POLICIES = {
    "p_pcp_lista_mae_admin_write",
    "p_pcp_modelos_admin_write",
    "p_pcp_dimensoes_admin_write",
    "p_pcp_kits_admin_write",
    "p_pcp_kit_itens_admin_write",
    "p_pcp_fluxo_admin_write",
    "p_pcp_fluxo_etapas_admin_write",
    "p_pcp_reparo_delete_admin",
    "p_pcp_lotes_delete_admin",
}


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def _executable_sql(sql: str) -> str:
    """Strip line comments so guards inspect executable SQL only."""
    return "\n".join(
        line for line in sql.splitlines() if not line.lstrip().startswith("--")
    )


def test_only_the_nine_known_policies_are_altered() -> None:
    sql = _sql()
    altered = set(
        re.findall(r"ALTER\s+POLICY\s+([a-zA-Z0-9_]+)", sql, re.IGNORECASE)
    )
    assert altered == EXPECTED_POLICIES
    assert len(re.findall(r"ALTER\s+POLICY\b", sql, re.IGNORECASE)) == 9


def test_change_is_performance_shape_only() -> None:
    sql = _executable_sql(_sql())
    lowered = sql.lower()

    # This migration must not change the authorization surface.
    for forbidden in (
        "create policy",
        "drop policy",
        "grant ",
        "revoke ",
        "enable row level security",
        "disable row level security",
    ):
        assert forbidden not in lowered

    # Seven FOR ALL policies have USING + WITH CHECK; two DELETE policies only
    # have USING. That yields 16 unchanged PCP_ADMIN fallback occurrences.
    assert sql.count("elo_private.has_capability('PCP_ADMIN'::text)") == 16


def test_every_jwt_lookup_uses_scalar_select_initplan_shape() -> None:
    sql = _executable_sql(_sql())
    # Seven USING+WITH CHECK pairs plus two DELETE USING predicates = 16 calls.
    assert len(re.findall(r"\(\s*SELECT\s+auth\.jwt\(\)\s*\)", sql, re.IGNORECASE)) == 16

    # Remove the approved scalar form; no direct executable auth.jwt() call may remain.
    without_wrapped = re.sub(
        r"\(\s*SELECT\s+auth\.jwt\(\)\s*\)",
        "",
        sql,
        flags=re.IGNORECASE,
    )
    assert "auth.jwt()" not in without_wrapped.lower()


def test_admin_claim_contract_is_preserved() -> None:
    sql = _executable_sql(_sql())
    assert sql.count("'app_metadata'::text") == 16
    assert sql.count("'role'::text") == 16
    assert sql.count("= 'admin'::text") == 16
