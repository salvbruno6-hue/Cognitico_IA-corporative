from elo.core import AccessDecision, AccessRequest, SessionMode, authorize


def request(**overrides):
    values = {
        "principal_id": "principal-1",
        "role": "external-user",
        "domain": "pcp",
        "enterprise_context": "tenant-a",
        "scope": "pcp-read",
        "action": "consult",
    }
    values.update(overrides)
    return AccessRequest(**values)


def test_external_consultation_defaults_to_read_only():
    result = authorize(request())
    assert result.decision is AccessDecision.ALLOW
    assert result.reason == "read_only_consultation_allowed"


def test_consultation_cannot_gain_write_or_external_action_authority():
    assert authorize(request(write_permission=True)).decision is AccessDecision.DENY
    assert authorize(request(external_action_permission=True)).decision is AccessDecision.DENY


def test_consultation_cannot_modify_core_or_access_unrelated_repository():
    for action in (
        "modify_core",
        "modify_canonical_memory",
        "change_permissions",
        "access_unrelated_repository",
        "access_owner_site",
        "access_secrets",
    ):
        assert authorize(request(action=action)).decision is AccessDecision.DENY


def test_specialist_can_contribute_domain_feedback_without_core_promotion():
    result = authorize(
        request(
            role="pcp-specialist",
            session_mode=SessionMode.AUTHORIZED_SPECIALIST,
            action="provide_feedback",
        )
    )
    assert result.decision is AccessDecision.ALLOW

    assert authorize(
        request(
            role="pcp-specialist",
            session_mode=SessionMode.AUTHORIZED_SPECIALIST,
            action="promote_to_core",
        )
    ).decision is AccessDecision.DENY


def test_specialist_production_execution_stays_with_governed_execution_boundary():
    for external_permission in (False, True):
        result = authorize(
            request(
                session_mode=SessionMode.AUTHORIZED_SPECIALIST,
                action="execute_production_action",
                external_action_permission=external_permission,
            )
        )
        assert result.decision is AccessDecision.DENY


def test_missing_identity_or_scope_fails_closed():
    assert authorize(request(principal_id="")).decision is AccessDecision.DENY
    assert authorize(request(domain="")).decision is AccessDecision.DENY
    assert authorize(request(scope="")).decision is AccessDecision.DENY
