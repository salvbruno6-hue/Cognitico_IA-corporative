from src.elo.core.authorization_enforcement import (
    AuthMethod,
    AuthorizationRegistry,
    Capability,
    Decision,
    Environment,
    IdentityAssertion,
    classify_external_session,
)


REPO = "salvbruno6-hue/Cognitico_IA-corporative"
OTHER_REPO = "salvbruno6-hue/other-repository"


def admin_binding(registry: AuthorizationRegistry):
    challenge = registry.begin_admin_authorization(AuthMethod.DIRECT)
    assertion = IdentityAssertion(
        provider="github",
        subject="planning-session",
        authenticated=True,
        github_subject="salvbruno6-hue",
    )
    return registry.establish_admin_binding(
        challenge,
        assertion,
        github_subject="salvbruno6-hue",
        repository_scope={REPO},
    )


def test_admin_direct_authorization_is_persistent_and_scoped():
    registry = AuthorizationRegistry()
    binding = admin_binding(registry)
    assert binding.environment == Environment.ADM
    assert registry.authorize(binding.binding_id, Capability.COMMIT, REPO).decision == Decision.ALLOW
    assert registry.authorize(binding.binding_id, Capability.MERGE_OPERATIONAL, REPO).decision == Decision.ALLOW
    assert registry.authorize(binding.binding_id, Capability.COMMIT, OTHER_REPO).decision == Decision.DENY


def test_qr_and_direct_are_only_challenge_methods():
    registry = AuthorizationRegistry()
    direct = registry.begin_admin_authorization(AuthMethod.DIRECT)
    qr = registry.begin_admin_authorization(AuthMethod.QR)
    assert direct != qr
    assert direct in registry.pending_challenges
    assert qr in registry.pending_challenges


def test_challenge_does_not_authorize_without_authenticated_matching_identity():
    registry = AuthorizationRegistry()
    challenge = registry.begin_admin_authorization(AuthMethod.DIRECT)
    assertion = IdentityAssertion(
        provider="github",
        subject="untrusted-session",
        authenticated=False,
        github_subject="someone-else",
    )
    try:
        registry.establish_admin_binding(challenge, assertion, "salvbruno6-hue", {REPO})
    except PermissionError as exc:
        assert str(exc) == "identity_assertion_mismatch"
    else:
        raise AssertionError("unauthenticated identity must not become ADM")


def test_unproven_external_session_fails_closed_to_visitor():
    assert classify_external_session(authenticated_identity=False, specialist_authorized=False) == Environment.VISITOR
    assert classify_external_session(authenticated_identity=True, specialist_authorized=False) == Environment.VISITOR
    assert classify_external_session(authenticated_identity=True, specialist_authorized=True) == Environment.SPECIALIST


def test_specialist_cannot_merge_or_expose_internal_architecture():
    registry = AuthorizationRegistry()
    challenge = registry.begin_admin_authorization(AuthMethod.DIRECT)
    assertion = IdentityAssertion("github", "specialist-session", True, "specialist-github")
    binding = registry.establish_admin_binding(challenge, assertion, "specialist-github", {REPO})
    # Downgrade the binding to the specialist environment for policy testing.
    specialist = binding.__class__(
        binding_id=binding.binding_id,
        identity_subject=binding.identity_subject,
        github_subject=binding.github_subject,
        environment=Environment.SPECIALIST,
        capabilities=frozenset({Capability.CONSULT, Capability.SPECIALIST_CONTRIBUTE, Capability.COMMIT}),
        repository_scope=frozenset({REPO}),
    )
    registry.bindings[binding.binding_id] = specialist
    assert registry.authorize(binding.binding_id, Capability.COMMIT, REPO).decision == Decision.ALLOW
    assert registry.authorize(binding.binding_id, Capability.MERGE_OPERATIONAL, REPO).decision == Decision.DENY
    assert registry.authorize(binding.binding_id, Capability.VIEW_INTERNAL_ARCHITECTURE, REPO).decision == Decision.DENY


def test_structural_change_requires_separate_governed_authorization():
    registry = AuthorizationRegistry()
    binding = admin_binding(registry)
    result = registry.authorize(
        binding.binding_id,
        Capability.MERGE_OPERATIONAL,
        REPO,
        structural_change=True,
    )
    assert result.decision == Decision.DENY
