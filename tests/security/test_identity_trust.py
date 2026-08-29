from dataclasses import replace

from elo.core.identity_trust import (
    EloIdentity,
    EloRole,
    TrustDecision,
    TrustRequest,
    TrustedIdentityRegistry,
    evaluate_trust,
)


REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative"


def identity(role=EloRole.CONSULTANT, repos=(REPOSITORY,), capabilities=frozenset({"read_consultation"})):
    return EloIdentity(
        principal_id="principal-1",
        provider="github",
        provider_subject="github-subject-1",
        role=role,
        enterprise_context="tenant-a",
        repository_scope=repos,
        capabilities=capabilities,
    )


AUTHORITATIVE_IDENTITY = identity()
REGISTRY = TrustedIdentityRegistry({"github:github-subject-1": AUTHORITATIVE_IDENTITY})


def req(**overrides):
    values = {
        "identity": AUTHORITATIVE_IDENTITY,
        "repository": REPOSITORY,
        "action": "consult",
        "capability": "read_consultation",
    }
    values.update(overrides)
    return TrustRequest(**values)


def test_known_registered_identity_scope_and_capability_are_allowed():
    assert evaluate_trust(req(), REGISTRY).decision is TrustDecision.ALLOW


def test_different_repository_is_denied_even_when_authenticated():
    assert evaluate_trust(req(repository="other-owner/other-repo"), REGISTRY).decision is TrustDecision.DENY


def test_ungranted_capability_is_denied():
    assert evaluate_trust(req(capability="write_repository"), REGISTRY).decision is TrustDecision.DENY


def test_unregistered_provider_subject_is_denied():
    foreign = replace(AUTHORITATIVE_IDENTITY, provider_subject="another-github-account")
    assert evaluate_trust(req(identity=foreign), REGISTRY).decision is TrustDecision.DENY


def test_role_escalation_in_request_is_denied_even_when_subject_is_registered():
    forged_admin = replace(AUTHORITATIVE_IDENTITY, role=EloRole.CANONICAL_ADMIN, capabilities=frozenset({"core_change"}))
    result = evaluate_trust(req(identity=forged_admin, action="modify_core", capability="core_change"), REGISTRY)
    assert result.decision is TrustDecision.DENY
    assert result.reason == "identity_claims_do_not_match_authority"


def test_repository_scope_escalation_in_request_is_denied():
    forged_scope = replace(AUTHORITATIVE_IDENTITY, repository_scope=(REPOSITORY, "other-owner/other-repo"))
    result = evaluate_trust(req(identity=forged_scope, repository="other-owner/other-repo"), REGISTRY)
    assert result.decision is TrustDecision.DENY
    assert result.reason == "identity_claims_do_not_match_authority"


def test_sensitive_core_changes_require_authoritative_canonical_authority():
    admin = identity(role=EloRole.CANONICAL_ADMIN, capabilities=frozenset({"core_change"}))
    admin_registry = TrustedIdentityRegistry({"github:github-subject-1": admin})
    result = evaluate_trust(
        TrustRequest(identity=admin, repository=REPOSITORY, action="modify_core", capability="core_change"),
        admin_registry,
    )
    assert result.decision is TrustDecision.ALLOW


def test_inactive_authoritative_identity_is_denied():
    inactive = replace(AUTHORITATIVE_IDENTITY, active=False)
    inactive_registry = TrustedIdentityRegistry({"github:github-subject-1": inactive})
    assert evaluate_trust(req(identity=inactive), inactive_registry).decision is TrustDecision.DENY


# Keep the regression suite explicit: trust-boundary changes must remain fail-closed.
