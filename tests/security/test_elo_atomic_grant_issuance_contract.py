"""ELO #1172 — atomic grant/audit adapter source contracts.

These are source-contract checks, NOT a live PostgreSQL transaction test.
A staging rollback/permission/idempotency probe remains mandatory before deploy.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MIGRATION=(ROOT/"supabase/migrations/20261110185000_elo_atomic_grant_audit_rpc.sql").read_text(encoding="utf-8")
AUTHZ=(ROOT/"supabase/functions/elo-authz/index.ts").read_text(encoding="utf-8")


def test_issuer_calls_single_transaction_rpc() -> None:
    issuer=AUTHZ.split('const bindingId=typeof body.binding_id',1)[1].split('if(action==="portal_access")',1)[0]
    assert 'supabase.rpc("elo_atomic_issue_authorization_grant"' in issuer
    assert 'supabase.from("elo_authorization_grants").insert' not in issuer
    assert 'audit(auth.identity.identity_id,session.session.session_id,action,repository,"ALLOW"' not in issuer
    assert "p_session_id:targetSession.session.session_id" in issuer
    assert "p_issuer_session_id:session.session.session_id" in issuer
    assert "p_metadata:grantMetadata" in issuer
    assert "if(grantError||!grant" in issuer
    assert 'reason:"authorization_grant_create_failed"' in issuer


def test_atomic_function_is_service_role_only_and_invoker() -> None:
    assert "security invoker" in MIGRATION.lower()
    assert "security definer" not in MIGRATION.lower().split("as $elo_atomic$")[0]
    assert "set search_path = ''" in MIGRATION
    assert "from public, anon, authenticated;" in MIGRATION.lower()
    assert ") to service_role;" in MIGRATION.lower()
    assert "returns public.elo_authorization_grants" in MIGRATION
    assert "on public.elo_authorization_grants (issued_by_identity_id, request_id)" in MIGRATION


def test_grant_and_audit_insert_inside_one_unhandled_transaction() -> None:
    body=MIGRATION.split("as $elo_atomic$",1)[1].split("$elo_atomic$;",1)[0]
    assert "insert into public.elo_authorization_grants" in body
    assert "insert into public.elo_authorization_audit" in body
    assert body.index("insert into public.elo_authorization_grants") < body.index("insert into public.elo_authorization_audit")
    assert "exception when" not in body.lower()
    assert "commit;" not in body.lower()
    assert "on conflict (issued_by_identity_id, request_id) do nothing" in body
    assert "a.decision = 'ALLOW'" in body
    assert "v_grant.revoked_at is not null" in body
    assert "v_grant.expires_at <= v_now" in body


def test_session_and_grant_invariants_are_not_relaxed() -> None:
    for required in (
      "p_issued_by_identity_id", "p_issuer_session_id", "p_session_id",
      "r.code = 'CANONICAL_ADMIN'", "r.active",
      "b.repository_full_name = p_repository_full_name and b.active",
      "s.revoked_at is null", "s.expires_at > v_now",
      "p_metadata->>'resource_id'", "p_metadata->>'tenant_id'",
      "elo_authz_atomic_grant_request_replay_mismatch",
    ):
      assert required in MIGRATION


def test_migration_guard_and_rollback_path_exist() -> None:
    assert MIGRATION.strip().lower().startswith("-- elo")
    assert "\nbegin;\n" in MIGRATION.lower()
    assert MIGRATION.rstrip().endswith("commit;")
    assert "elo_authz_issue_request_duplicates_require_reconciliation" in MIGRATION
    assert "uq_elo_authz_grant_issuer_request" in MIGRATION
