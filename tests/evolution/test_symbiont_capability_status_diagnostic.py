from elo.cognitive.symbiont_capability_evolution import (
    CapabilityConditionStatus,
    CapabilityReadinessStatus,
    diagnose_capability_status,
)


def _base(**overrides):
    values = dict(
        capability_id="EXT-TEST",
        capability_name="Test Capability",
        owner="test-owner",
        authority="existing-owner",
        contract_present=True,
        implementation_present=True,
        tests_present=True,
        evidence_present=True,
        runtime_integrated=True,
        operational_evidence=True,
        production_outcome=False,
        governance_approved=False,
        contract_refs=("contract:1",),
        implementation_refs=("impl:1",),
        test_refs=("test:1",),
        evidence_refs=("evidence:1",),
        runtime_refs=("runtime:1",),
        operational_refs=("ops:1",),
    )
    values.update(overrides)
    return diagnose_capability_status(**values)


def test_status_reports_runtime_without_fabricating_production():
    report = _base()
    assert report.status is CapabilityReadinessStatus.OPERATIONALLY_EVIDENCED
    assert report.production_proven is False
    assert report.conditions[-2].status is CapabilityConditionStatus.VERIFIED
    assert report.conditions[-3].status is CapabilityConditionStatus.VERIFIED
    assert "PRODUCTION_OUTCOME" in report.missing_conditions


def test_status_reports_real_runtime_gap():
    report = _base(runtime_integrated=False, runtime_refs=())
    assert report.status is CapabilityReadinessStatus.EVIDENCED_NOT_RUNTIME
    assert "RUNTIME_INTEGRATION" in report.missing_conditions
    assert report.production_proven is False


def test_status_reports_blocker_before_other_states():
    report = _base(blockers=("canonical runtime entrypoint not located",))
    assert report.status is CapabilityReadinessStatus.BLOCKED
    assert report.blockers == ("canonical runtime entrypoint not located",)


def test_production_outcome_does_not_self_authorize():
    report = _base(production_outcome=True, production_refs=("prod:1",))
    assert report.status is CapabilityReadinessStatus.READY_FOR_EVOLUTION_GATE
    assert report.production_proven is False
    assert "GOVERNANCE_APPROVAL" in report.missing_conditions


def test_production_proven_requires_explicit_governance_evidence():
    report = _base(
        production_outcome=True,
        production_refs=("prod:1",),
        governance_approved=True,
        governance_refs=("gate:1",),
    )
    assert report.status is CapabilityReadinessStatus.PRODUCTION_PROVEN
    assert report.production_proven is True
    assert report.missing_conditions == ()


def test_missing_evidence_is_not_inferred_from_present_implementation():
    report = _base(evidence_present=False, evidence_refs=())
    assert report.status is CapabilityReadinessStatus.TESTED_NOT_EVIDENCED
    assert "EVIDENCE" in report.missing_conditions
    assert report.production_proven is False
