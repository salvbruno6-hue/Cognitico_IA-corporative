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
        "provider": "github",
        "provider_subject": "github-subject-1",
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
    assert evaluate_trust(req(provider_subject="another-github-account"), REGISTRY).decision is TrustDecision.DENY


def test_request_has_no_privileged_identity_attributes():
    request_fields = set(TrustRequest.__dataclass_fields__)
    assert request_fields.isdisjoint({"principal_id", "role", "enterprise_context", "repository_scope", "capabilities", "active"})


def test_registered_subject_uses_authoritative_role_for_sensitive_actions():
    result = evaluate_trust(
        req(action="modify_core", capability="core_change"),
        REGISTRY,
    )
    assert result.decision is TrustDecision.DENY
    assert result.reason == "capability_not_granted"


def test_authoritative_canonical_admin_can_pass_sensitive_role_gate():
    admin = identity(role=EloRole.CANONICAL_ADMIN, capabilities=frozenset({"core_change"}))
    admin_registry = TrustedIdentityRegistry({"github:github-subject-1": admin})
    result = evaluate_trust(
        req(action="modify_core", capability="core_change"),
        admin_registry,
    )
    assert result.decision is TrustDecision.ALLOW


def test_inactive_authoritative_identity_is_denied():
    inactive = replace(AUTHORITATIVE_IDENTITY, active=False)
    inactive_registry = TrustedIdentityRegistry({"github:github-subject-1": inactive})
    assert evaluate_trust(req(), inactive_registry).decision is TrustDecision.DENY


# Keep the regression suite explicit: trust-boundary changes must remain fail-closed.
