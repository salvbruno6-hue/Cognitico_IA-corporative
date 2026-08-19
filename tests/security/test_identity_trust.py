from elo.core.identity_trust import EloIdentity, EloRole, TrustDecision, TrustRequest, evaluate_trust


def identity(role=EloRole.CONSULTANT, repos=("salvbruno6-hue/Cognitico_IA-corporative",), capabilities=frozenset({"read_consultation"})):
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
        "repository": "salvbruno6-hue/Cognitico_IA-corporative",
        "action": "consult",
        "capability": "read_consultation",
    }
    values.update(overrides)
    return TrustRequest(**values)


def test_known_identity_scope_and_capability_are_allowed():
    assert evaluate_trust(req()).decision is TrustDecision.ALLOW


def test_different_repository_is_denied_even_when_authenticated():
    assert evaluate_trust(req(repository="other-owner/other-repo")).decision is TrustDecision.DENY


def test_ungranted_capability_is_denied():
    assert evaluate_trust(req(capability="write_repository")).decision is TrustDecision.DENY


def test_sensitive_core_changes_require_canonical_authority():
    assert evaluate_trust(req(action="modify_core")).decision is TrustDecision.DENY
    admin = identity(role=EloRole.CANONICAL_ADMIN, capabilities=frozenset({"core_change"}))
    assert evaluate_trust(req(identity=admin, action="modify_core", capability="core_change")).decision is TrustDecision.ALLOW


def test_inactive_identity_is_denied():
    inactive = EloIdentity(**{**identity().__dict__, "active": False})
    assert evaluate_trust(req(identity=inactive)).decision is TrustDecision.DENY
