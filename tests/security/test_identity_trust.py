from elo.core.identity_trust import (
    EloIdentity,
    EloRole,
    TrustDecision,
    TrustRequest,
    TrustedIdentityRegistry,
    evaluate_trust,
)


REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative"
REGISTRY = TrustedIdentityRegistry({"github:github-subject-1": "principal-1"})


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


def req(**overrides):
    values = {
        "identity": identity(),
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
    foreign = identity()
    foreign = EloIdentity(**{**foreign.__dict__, "provider_subject": "another-github-account"})
    assert evaluate_trust(req(identity=foreign), REGISTRY).decision is TrustDecision.DENY


def test_sensitive_core_changes_require_canonical_authority():
    assert evaluate_trust(req(action="modify_core"), REGISTRY).decision is TrustDecision.DENY
    admin = identity(role=EloRole.CANONICAL_ADMIN, capabilities=frozenset({"core_change"}))
    assert evaluate_trust(req(identity=admin, action="modify_core", capability="core_change"), REGISTRY).decision is TrustDecision.ALLOW


def test_inactive_identity_is_denied():
    inactive = EloIdentity(**{**identity().__dict__, "active": False})
    assert evaluate_trust(req(identity=inactive), REGISTRY).decision is TrustDecision.DENY
