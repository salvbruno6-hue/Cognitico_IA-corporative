from pathlib import Path


AUTHZ = Path("supabase/functions/elo-authz/index.ts").read_text(encoding="utf-8")


def test_authorization_audit_write_is_checked():
    assert 'const { error: auditError } = await supabase.from("elo_authorization_audit").insert' in AUTHZ
    assert "if (auditError)" in AUTHZ
    assert "authorization_audit_write_failed" in AUTHZ


def test_allow_path_fails_closed_when_audit_write_fails():
    allow_marker = 'await audit(auth.identity.identity_id, session.session.session_id, action, repository || null, "ALLOW"'
    allow_pos = AUTHZ.index(allow_marker)
    tail = AUTHZ[allow_pos:]
    assert "catch {\n    return json({ authorized: false, reason: \"authorization_audit_write_failed\"" in tail
    assert 'return json({ authorized: true' in tail


def test_deny_paths_remain_audited():
    assert AUTHZ.count('await audit(') >= 5
    assert '"DENY"' in AUTHZ
