from pathlib import Path


SQL = Path(
    "docs/implementation/sql/ELO_AUTHZ_PCP_ADMIN_DEBT_RESOLUTION_CANDIDATE.sql"
).read_text(encoding="utf-8")
DECISION = Path(
    "docs/architecture/ELO_AUTHZ_PCP_ADMIN_DEBT_RESOLUTION_DECISION_20261102.md"
).read_text(encoding="utf-8")
ADR = Path("10-adr/ADR-0017-lista-mae-editable-by-admin.md").read_text(encoding="utf-8")
HEALTH = Path("supabase/health/elo_capability_reference_integrity.sql").read_text(encoding="utf-8")


def test_resolution_remains_non_live_candidate() -> None:
    assert "CANDIDATE ONLY" in SQL
    assert "NOT AUTHORIZED FOR LIVE DDL" in SQL
    assert "PREPARED / NOT LIVE" in DECISION
    assert "supabase/migrations" not in str(
        Path("docs/implementation/sql/ELO_AUTHZ_PCP_ADMIN_DEBT_RESOLUTION_CANDIDATE.sql")
    )


def test_admin_role_and_capability_are_separate_predicates() -> None:
    assert "FUNCTION elo_private.has_admin_role()" in SQL
    assert "r.code IN ('ELO_ADMIN', 'CANONICAL_ADMIN')" in SQL
    assert "FUNCTION elo_private.has_capability(p_code text)" in SQL
    assert "JOIN public.elo_role_capabilities rc" in SQL
    assert "JOIN public.elo_capabilities c" in SQL
    assert "AND c.code = p_code" in SQL
    has_capability_section = SQL.split(
        "CREATE OR REPLACE FUNCTION elo_private.has_capability(p_code text)", 1
    )[1].split("REVOKE ALL ON FUNCTION elo_private.has_capability", 1)[0]
    assert "ELO_ADMIN" not in has_capability_section
    assert "CANONICAL_ADMIN" not in has_capability_section


def test_candidate_does_not_create_or_assign_capabilities() -> None:
    lowered = SQL.lower()
    for forbidden in (
        "insert into public.elo_capabilities",
        "insert into public.elo_role_capabilities",
        "update public.elo_capabilities",
        "update public.elo_role_capabilities",
        "delete from public.elo_capabilities",
        "delete from public.elo_role_capabilities",
    ):
        assert forbidden not in lowered


def test_policy_rewrite_is_bound_to_audited_live_shape() -> None:
    assert "v_policy_count <> 38" in SQL
    assert "v_expression_count <> 50" in SQL
    assert "ALTER POLICY %I ON %I.%I" in SQL
    assert "PCP_ADMIN policy graph changed" in SQL
    assert "PCP_ADMIN policy references remain after rewrite" in SQL
    assert "elo_private.has_admin_role()" in SQL


def test_lista_mae_guard_no_longer_treats_security_definer_current_user_as_caller() -> None:
    guard = SQL.split("CREATE OR REPLACE FUNCTION public.lista_mae_guard()", 1)[1].split(
        "REVOKE ALL ON FUNCTION public.lista_mae_guard()", 1
    )[0]
    assert "elo_private.has_admin_role()" in guard
    assert "auth.jwt()" in guard
    assert "app.lista_mae_aprovada" in guard
    assert "current_user IN" not in guard
    assert "lista_mae_alteracoes" in guard


def test_trigger_acl_hardening_is_preserved() -> None:
    assert "REVOKE ALL ON FUNCTION public.lista_mae_guard() FROM PUBLIC, anon, authenticated" in SQL
    assert "GRANT EXECUTE ON FUNCTION public.lista_mae_guard() TO service_role" in SQL


def test_final_assertions_require_orphan_and_current_user_bypass_to_disappear() -> None:
    assert "PCP_ADMIN still referenced by RLS" in SQL
    assert "PCP_ADMIN still referenced by authorization function body" in SQL
    assert "lista_mae_guard still uses current_user as authorization evidence" in SQL


def test_decision_respects_existing_canonical_debt_classification() -> None:
    assert "PCP_ADMIN` fica como dívida técnica registrada" in ADR
    assert "never permission to create/assign" in HEALTH
    assert "Resolve the debt without creating a new capability." in DECISION
    assert "No role code bypasses capability materialization." in DECISION


def test_resolution_does_not_promote_strategic_authority() -> None:
    assert "does **not** grant `PROPOSE`, `REVIEW`, `APPROVE`, `ADMIN`, `CANONICAL_WRITE`" in DECISION
    assert "`elo-authz` remains the authorization authority" in DECISION
