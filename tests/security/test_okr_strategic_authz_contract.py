from pathlib import Path


POLICY = Path("supabase/functions/elo-authz/strategic_write.ts")
AUTHZ_RUNTIME = Path("supabase/functions/elo-authz/index.ts")
WEB_BOUNDARY = Path("apps/elo-web/src/app/api/authorization/route.ts")
DECISION = Path("docs/architecture/ELO_OKR_ENTERPRISE_TENANT_SCOPE_DECISION_20261009.md")
AUTHORITY_DECISION = Path("docs/architecture/ELO_AUTHORITY_SEPARATION_DECISION_20261009.md")
AUDIT_BASELINE = Path("supabase/migrations/20260912195000_elo_authorization_schema_baseline.sql")


def test_strategic_policy_reuses_existing_capabilities_only() -> None:
    source = POLICY.read_text(encoding="utf-8")

    assert 'strategic_okr_propose: "PROPOSE"' in source
    assert 'strategic_okr_review: "REVIEW"' in source
    assert 'strategic_okr_approve: "APPROVE"' in source
    assert 'strategic_okr_write: "CANONICAL_WRITE"' in source
    assert "OKR_WRITE" not in source
    assert "PCP_UPDATE" not in source


def test_strategic_policy_requires_registered_google_identity() -> None:
    source = POLICY.read_text(encoding="utf-8")

    assert "isRegisteredGoogleIdentity" in source
    assert '=== "google"' in source
    assert "authorized_email" in source
    assert "auth_user_id" in source
    assert "identity?.active === true" in source
    assert "authorizedEmail === email" in source


def test_strategic_policy_requires_enterprise_scope_not_domain_or_repository() -> None:
    source = POLICY.read_text(encoding="utf-8")

    assert 'String(scope?.scope_type ?? "").trim() === "ENTERPRISE"' in source
    assert "scope?.scope_key" in source
    assert '=== "DOMAIN"' not in source
    assert '=== "REPOSITORY"' not in source
    assert "enterprise_context" not in source


def test_structural_strategic_write_is_not_delegable() -> None:
    source = POLICY.read_text(encoding="utf-8")

    assert 'STRUCTURAL_ONLY_CAPABILITIES = new Set(["ADMIN", "CANONICAL_WRITE"])' in source
    assert 'STRUCTURAL_ONLY_STRATEGIC_ACTIONS = new Set(["strategic_okr_write"])' in source
    assert "strategicActionRequiresStructuralAuthority" in source
    assert "isDelegableStrategicAction" in source


def test_authority_decision_keeps_admin_developer_boundary() -> None:
    text = AUTHORITY_DECISION.read_text(encoding="utf-8")

    assert "Only ADM/Developer authority" in text
    assert "PCP_UPDATE" in text
    assert "PROPOSE" in text
    assert "REVIEW" in text
    assert "APPROVE" in text
    assert "CANONICAL_WRITE" in text
    assert "Alter governed tables" in text
    assert "generic SQL/table mutation authority" in text


def test_strategic_policy_uses_short_bounded_receipt() -> None:
    source = POLICY.read_text(encoding="utf-8")

    assert "STRATEGIC_RECEIPT_TTL_SECONDS = 300" in source
    assert "strategicReceiptExpiry" in source
    assert "Date.now" in source


def test_resource_shapes_are_explicit_and_action_bound() -> None:
    source = POLICY.read_text(encoding="utf-8")

    assert "strategic_okr:objective:" in source
    assert "strategic_okr:key_result:" in source
    assert "strategic_okr:binding:" in source
    assert "strategicResourceMatchesAction" in source
    assert 'action === "strategic_okr_propose"' in source
    assert 'action === "strategic_okr_review"' in source
    assert 'action === "strategic_okr_approve"' in source
    assert 'action === "strategic_okr_write"' in source


def test_decision_explicitly_blocks_scope_and_identity_shortcuts() -> None:
    text = DECISION.read_text(encoding="utf-8")

    assert "enterprise_context" in text
    assert "DOMAIN" in text
    assert "REPOSITORY" in text
    assert "area_code" in text
    assert "GitHub operator binding" in text
    assert "No new tenant table" in text
    assert "email domain" in text
    assert "caller-supplied email" in text
    assert "successful Google authentication without a matching canonical identity record" in text
    assert "authorized_email = authenticated Google email" in text


def test_canonical_elo_authz_integrates_strategic_policy_without_new_authority() -> None:
    runtime = AUTHZ_RUNTIME.read_text(encoding="utf-8")

    assert 'from "./strategic_write.ts"' in runtime
    assert 'if(action==="authorize_strategic_write")' in runtime
    assert "strategicCapabilityForAction" in runtime
    assert "strategicResourceMatchesAction" in runtime
    assert "isRegisteredGoogleIdentity" in runtime
    assert "hasEnterpriseTenantScope" in runtime
    assert "hasCapability(auth.roleIds,capability)" in runtime
    assert "strategicActionRequiresStructuralAuthority" in runtime
    assert 'auth.roles.includes("CANONICAL_ADMIN")' in runtime


def test_only_active_roles_can_contribute_capabilities() -> None:
    runtime = AUTHZ_RUNTIME.read_text(encoding="utf-8")

    assert "const activeRoleRows = (roleRows ?? []).filter((r:any)=>r.elo_roles?.active===true)" in runtime
    assert "const roles = activeRoleRows.map((r:any)=>String(r.elo_roles.code))" in runtime
    assert "roleIds:activeRoleRows.map((r:any)=>r.role_id).filter(Boolean)" in runtime
    assert "roleIds:(roleRows ?? [])" not in runtime


def test_strategic_path_uses_google_bound_identity_and_active_session() -> None:
    runtime = AUTHZ_RUNTIME.read_text(encoding="utf-8")

    assert "authorized_email,auth_user_id" in runtime
    assert ".eq(\"auth_user_id\", data.user.id).eq(\"active\", true)" in runtime
    assert "const session=await resolveActiveSession(auth.identity.identity_id)" in runtime
    assert 'registered_google_identity_required' in runtime
    assert 'enterprise_tenant_scope_not_granted' in runtime
    assert 'strategic_capability_not_granted' in runtime


def test_every_strategic_decision_is_audited_and_receipt_is_resource_bound() -> None:
    runtime = AUTHZ_RUNTIME.read_text(encoding="utf-8")

    assert "const strategicAuditAction=strategicAction?`${action}:${strategicAction}`:action" in runtime
    assert 'const strategicAuditResource=`tenant:${tenantId||"UNBOUND"}|resource:${strategicResource}`' in runtime
    assert 'strategicAuditAction,strategicAuditResource,"DENY",reason,requestId' in runtime
    assert 'strategicAuditAction,strategicAuditResource,"ALLOW","strategic_identity_tenant_scope_capability_verified",requestId' in runtime
    for token in (
        'authorization_authority:"elo-authz"',
        'action,',
        'strategic_action:strategicAction',
        'capability,',
        'tenant_id:tenantId',
        'resource_ref:resourceRef',
        'identity_id:auth.identity.identity_id',
        'session_id:session.session.session_id',
        'evidence_ref:evidenceRef',
        'grant_ref:grantRef',
        'expires_at:expiresAt',
    ):
        assert token in runtime


def test_strategic_audit_provenance_uses_only_versioned_audit_fields() -> None:
    runtime = AUTHZ_RUNTIME.read_text(encoding="utf-8")
    baseline = AUDIT_BASELINE.read_text(encoding="utf-8")
    strategic = runtime.split('if(action==="authorize_strategic_write")', 1)[1].split('if(action==="check_authorization_state")', 1)[0]

    assert "scope_key" not in baseline.split("create table if not exists public.elo_authorization_audit", 1)[1].split(";", 1)[0]
    assert "scope_key" not in strategic
    assert "strategicAuditAction" in strategic
    assert "strategicAuditResource" in strategic
    assert "tenant:${tenantId" in strategic
    assert "resource:${strategicResource}" in strategic


def test_strategic_receipt_does_not_reuse_github_authorization_grants_as_parallel_owner() -> None:
    runtime = AUTHZ_RUNTIME.read_text(encoding="utf-8")
    strategic = runtime.split('if(action==="authorize_strategic_write")', 1)[1].split('if(action==="check_authorization_state")', 1)[0]

    assert "elo_authorization_grants" not in strategic
    assert "strategicReceiptExpiry()" in strategic
    assert "const grantRef=evidenceRef" in strategic


def test_elo_web_boundary_explicitly_proxies_strategic_fields() -> None:
    route = WEB_BOUNDARY.read_text(encoding="utf-8")

    assert '"authorize_strategic_write"' in route
    assert "strategic_action?: unknown" in route
    assert "tenant_id?: unknown" in route
    assert "resource_ref?: unknown" in route
    assert "strategic_action:typeof body.strategic_action" in route
    assert "tenant_id:typeof body.tenant_id" in route
    assert "resource_ref:typeof body.resource_ref" in route
