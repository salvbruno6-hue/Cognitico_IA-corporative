import pytest

from elo.application.use_cases.system_health_symbiont_bridge import SystemHealthSymbiontBridge
from elo.cognitive.mt_authorization_readiness import (
    MTAuthorizationSignals,
    assess_mt_authorization_readiness,
)
from elo.cognitive.system_health_assessment import assess_system_health


def live_gap_signals() -> MTAuthorizationSignals:
    return MTAuthorizationSignals(
        eligible_google_identities=1,
        enterprise_multiteiner_links=0,
        identities_with_domain_scope=0,
        identities_with_pcp_capability=0,
        fully_ready_identities=0,
        tenant_rows=0,
        repair_rows=133,
        repair_rows_with_tenant=0,
        legacy_policy_objects=168,
        legacy_tables=71,
    )


def test_live_gap_is_decomposed_in_prerequisite_order():
    readiness = assess_mt_authorization_readiness(live_gap_signals())

    assert readiness.next_required_condition == "enterprise_multiteiner_scope"
    assert readiness.operator_ready is False
    assert readiness.tenant_data_ready is False
    assert readiness.ready_for_policy_rewrite is False
    assert readiness.canonical_mutation is False

    findings = {item.finding_id: item for item in readiness.findings}
    assert findings["MT_AUTHZ_IDENTITY_BOUND"].severity.value == "PASS"
    assert findings["MT_AUTHZ_ENTERPRISE_SCOPE"].severity.value == "GAP_HIGH"
    assert findings["MT_TENANT_REGISTRY"].severity.value == "GAP_HIGH"
    assert findings["MT_REPAIR_TENANT_COVERAGE"].severity.value == "GAP_HIGH"
    assert findings["MT_LEGACY_LITERAL_TRUE_SURFACE"].severity.value == "GAP_HIGH"


def test_symbiont_can_observe_and_orchestrator_can_prioritize_without_self_authorization():
    readiness = assess_mt_authorization_readiness(live_gap_signals())
    health = assess_system_health(readiness.findings)
    orientations = SystemHealthSymbiontBridge().orient(health)

    assert orientations
    assert orientations[0].finding_id == "MT_AUTHZ_ENTERPRISE_SCOPE"
    assert orientations[0].owner == "elo-authz"
    assert orientations[0].authorized is False
    assert all(item.authorized is False for item in orientations)


def test_policy_rewrite_only_becomes_ready_when_operator_and_tenant_data_are_real():
    readiness = assess_mt_authorization_readiness(
        MTAuthorizationSignals(
            eligible_google_identities=1,
            enterprise_multiteiner_links=1,
            identities_with_domain_scope=1,
            identities_with_pcp_capability=1,
            fully_ready_identities=1,
            tenant_rows=1,
            repair_rows=133,
            repair_rows_with_tenant=133,
            legacy_policy_objects=168,
            legacy_tables=71,
        )
    )

    assert readiness.next_required_condition is None
    assert readiness.operator_ready is True
    assert readiness.tenant_data_ready is True
    assert readiness.ready_for_policy_rewrite is True
    assert readiness.canonical_mutation is False
    assert readiness.findings[-1].finding_id == "MT_LEGACY_LITERAL_TRUE_SURFACE"
    assert readiness.findings[-1].severity.value == "GAP_HIGH"


def test_no_legacy_surface_does_not_create_false_authority():
    readiness = assess_mt_authorization_readiness(
        MTAuthorizationSignals(
            eligible_google_identities=1,
            enterprise_multiteiner_links=0,
            identities_with_domain_scope=0,
            identities_with_pcp_capability=0,
            fully_ready_identities=0,
            tenant_rows=0,
            repair_rows=0,
            repair_rows_with_tenant=0,
            legacy_policy_objects=0,
            legacy_tables=0,
        )
    )

    assert readiness.ready_for_policy_rewrite is False
    assert readiness.next_required_condition == "enterprise_multiteiner_scope"
    assert readiness.findings[-1].severity.value == "PASS"


def test_invalid_signal_counts_fail_closed():
    with pytest.raises(ValueError, match="cannot be negative"):
        MTAuthorizationSignals(
            eligible_google_identities=-1,
            enterprise_multiteiner_links=0,
            identities_with_domain_scope=0,
            identities_with_pcp_capability=0,
            fully_ready_identities=0,
            tenant_rows=0,
            repair_rows=0,
            repair_rows_with_tenant=0,
            legacy_policy_objects=0,
            legacy_tables=0,
        )

    with pytest.raises(ValueError, match="cannot exceed"):
        MTAuthorizationSignals(
            eligible_google_identities=1,
            enterprise_multiteiner_links=0,
            identities_with_domain_scope=0,
            identities_with_pcp_capability=0,
            fully_ready_identities=0,
            tenant_rows=0,
            repair_rows=1,
            repair_rows_with_tenant=2,
            legacy_policy_objects=1,
            legacy_tables=1,
        )
