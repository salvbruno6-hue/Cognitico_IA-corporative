from elo.agent_intake.capability_policy_resolution import resolve_capability_policy


def test_allowlist_authorized_same_scope_low_risk_is_authorized():
    result = resolve_capability_policy(
        request_id="policy-allow-01",
        tenant_scope="multiteiner",
        capability_id="HERMES-TOOLSETS",
        policy="allowlist",
        authorized=True,
        requested_scope="commercial",
        allowed_scope="commercial",
        risk="low",
    )
    assert result.status == "authorized"
    assert result.authorized is True
    assert result.scope_ok is True
    assert result.approval_required is False
    assert result.learning_candidate["promotion_state"] == "candidate_only"
    assert result.learning_candidate["canonical_mutation"] is False


def test_deny_policy_blocks_even_when_authorized():
    result = resolve_capability_policy(
        request_id="policy-deny-01",
        tenant_scope="multiteiner",
        capability_id="HERMES-TOOLSETS",
        policy="deny",
        authorized=True,
        requested_scope="commercial",
        allowed_scope="commercial",
    )
    assert result.status == "blocked"
    assert result.authorized is False


def test_scope_mismatch_blocks():
    result = resolve_capability_policy(
        request_id="policy-scope-01",
        tenant_scope="multiteiner",
        capability_id="HERMES-DELEGATION",
        policy="allowlist",
        authorized=True,
        requested_scope="production",
        allowed_scope="commercial",
    )
    assert result.status == "blocked"
    assert result.scope_ok is False
    assert result.authorized is False


def test_high_risk_requires_approval_and_does_not_grant_execution_authority():
    result = resolve_capability_policy(
        request_id="policy-risk-01",
        tenant_scope="multiteiner",
        capability_id="HERMES-MCP",
        policy="allowlist",
        authorized=True,
        requested_scope="commercial",
        allowed_scope="commercial",
        risk="high",
    )
    assert result.status == "blocked"
    assert result.approval_required is True
    assert result.authorized is False


def test_unauthorized_request_is_blocked():
    result = resolve_capability_policy(
        request_id="policy-auth-01",
        tenant_scope="multiteiner",
        capability_id="HERMES-SKILLS",
        policy="allowlist",
        authorized=False,
        requested_scope="commercial",
        allowed_scope="commercial",
    )
    assert result.status == "blocked"
    assert result.authorized is False


def test_unknown_capability_does_not_infer_or_grant():
    result = resolve_capability_policy(
        request_id="policy-unknown-01",
        tenant_scope="multiteiner",
        capability_id="UNKNOWN-CAPABILITY",
        policy="allowlist",
        authorized=True,
        requested_scope="commercial",
        allowed_scope="commercial",
    )
    assert result.status == "unresolved"
    assert result.capability_id is None
    assert result.authorized is False
    assert result.scope_ok is False


def test_full_policy_is_not_implicitly_trusted():
    result = resolve_capability_policy(
        request_id="policy-full-01",
        tenant_scope="multiteiner",
        capability_id="HERMES-TOOLSETS",
        policy="full",
        authorized=True,
        requested_scope="commercial",
        allowed_scope="commercial",
    )
    assert result.status == "blocked"
    assert result.authorized is False


def test_policy_evaluation_is_deterministic_and_preserves_tenant_scope():
    kwargs = dict(
        request_id="policy-repeat-01",
        tenant_scope="tenant-a",
        capability_id="HERMES-AUTOMATION",
        policy="allowlist",
        authorized=True,
        requested_scope="operations",
        allowed_scope="operations",
        risk="low",
    )
    first = resolve_capability_policy(**kwargs)
    second = resolve_capability_policy(**kwargs)
    assert first == second
    assert first.tenant_scope == "tenant-a"
    assert second.tenant_scope == "tenant-a"
    assert first.learning_candidate == {
        "promotion_state": "candidate_only",
        "canonical_mutation": False,
    }
