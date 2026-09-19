from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTHZ = (ROOT / "supabase/functions/elo-authz/index.ts").read_text(encoding="utf-8")
MIGRATION = (ROOT / "supabase/migrations/20260919000000_elo_operator_github_binding_runtime.sql").read_text(
    encoding="utf-8"
)


def test_binding_is_persistent_and_repository_scoped() -> None:
    assert "elo_operator_github_bindings" in MIGRATION
    assert "identity_id uuid not null" in MIGRATION
    assert "github_user_id bigint not null" in MIGRATION
    assert "repository_full_name text not null" in MIGRATION
    assert "unique (identity_id, repository_full_name)" in MIGRATION
    assert "unique (github_user_id, repository_full_name)" in MIGRATION


def test_authorization_states_are_explicit_and_expiring() -> None:
    for state in (
        "elo-execution-authorized",
        "elo-commit-authorized",
        "elo-merge-authorized",
    ):
        assert state in MIGRATION
    assert "elo_authorization_grants" in MIGRATION
    assert "expires_at timestamptz not null" in MIGRATION
    assert "revoked_at timestamptz" in MIGRATION


def test_authorization_audit_remains_canonical() -> None:
    assert 'supabase.from("elo_authorization_audit").insert' in AUTHZ
    assert "authorization_authority:" in AUTHZ


def test_codex_cannot_emit_authorization_states() -> None:
    workflow = (ROOT / ".github/workflows/elo-agent-loop.yml").read_text(encoding="utf-8")
    assert "ELO_DECISION=APPROVE_COMMIT" in workflow
    assert "authorization_state:" not in workflow
    assert "create_operator_binding" not in workflow
    assert "issue_authorization_grant" not in workflow


def test_canonical_issuer_is_required_for_binding_and_grants():
    source = Path("supabase/functions/elo-authz/index.ts").read_text(encoding="utf-8")
    assert 'action==="create_operator_binding" || action==="issue_authorization_grant"' in source
    assert 'auth.roles.includes("CANONICAL_ADMIN")' in source
    assert "canonical_admin_created_operator_binding" in source
    assert "canonical_admin_issued_authorization_state" in source
    assert "expires_in_seconds" in source
    assert "86400" in source


def test_web_boundary_exposes_only_canonical_issuer_actions():
    route = Path("apps/elo-web/src/app/api/authorization/route.ts").read_text(encoding="utf-8")
    assert '"create_operator_binding","issue_authorization_grant"' in route


def test_collaborator_and_visitor_tiers_are_separated():
    migration = Path("supabase/migrations/20260919010000_elo_access_tiers.sql").read_text(encoding="utf-8")
    assert "'COLABORADOR'" in migration
    assert "'VISITANTE'" in migration
    assert "'LISTA_MAE_INSERT'" in migration
    assert "('COLABORADOR'" in migration
    assert "('VISITANTE'" in migration
    assert "elo_private.has_capability('LISTA_MAE_INSERT')" in migration
    assert "FOR INSERT" in migration
    assert "FOR UPDATE" not in migration
    assert "FOR DELETE" not in migration


def test_collaborator_has_no_github_binding_by_definition():
    migration = Path("supabase/migrations/20260919010000_elo_access_tiers.sql").read_text(encoding="utf-8")
    assert "No identity is auto-provisioned by this migration." in migration
    assert "A collaborator does not receive a GitHub operator binding." in migration
