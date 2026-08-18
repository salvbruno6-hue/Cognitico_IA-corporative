from elo.core import AccessDecision, AccessRequest, SessionMode, authorize


def request(**overrides):
    values = {
        "principal_id": "principal-1",
        "role": "external-user",
        "domain": "pcp",
        "enterprise_context": "tenant-a",
        "scope": "pcp-read",
        "action": "consult",
        "session_mode": SessionMode.READ_ONLY_CONSULTATION,
    }
    values.update(overrides)
    return AccessRequest(**values)


def test_read_only_boundary_is_fail_closed():
    blocked = (
        "modify_core",
        "modify_canonical_memory",
        "change_permissions",
        "access_unrelated_repository",
        "access_owner_site",
        "access_secrets",
        "execute_production_action",
    )
    for action in blocked:
        result = authorize(request(action=action))
        assert result.decision is AccessDecision.DENY


def test_specialist_feedback_is_scoped_but_core_promotion_is_not():
    specialist = request(
        role="pcp-specialist",
        session_mode=SessionMode.AUTHORIZED_SPECIALIST,
        action="provide_feedback",
    )
    assert authorize(specialist).decision is AccessDecision.ALLOW
    assert authorize(
        request(
            role="pcp-specialist",
            session_mode=SessionMode.AUTHORIZED_SPECIALIST,
            action="promote_to_core",
        )
    ).decision is AccessDecision.DENY


def test_missing_identity_scope_or_domain_fails_closed():
    for field in ("principal_id", "scope", "domain"):
        assert authorize(request(**{field: ""})).decision is AccessDecision.DENY
