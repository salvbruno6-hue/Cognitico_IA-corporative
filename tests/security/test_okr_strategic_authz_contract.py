from pathlib import Path


POLICY = Path("supabase/functions/elo-authz/strategic_write.ts")
DECISION = Path("docs/architecture/ELO_OKR_ENTERPRISE_TENANT_SCOPE_DECISION_20261009.md")


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


def test_strategic_policy_uses_short_bounded_receipt() -> None:
    source = POLICY.read_text(encoding="utf-8")

    assert "STRATEGIC_RECEIPT_TTL_SECONDS = 300" in source
    assert "strategicReceiptExpiry" in source
    assert "Date.now" in source


def test_resource_shapes_are_explicit_and_scoped() -> None:
    source = POLICY.read_text(encoding="utf-8")

    assert "strategic_okr:objective:" in source
    assert "strategic_okr:key_result:" in source
    assert "strategic_okr:binding:" in source


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
