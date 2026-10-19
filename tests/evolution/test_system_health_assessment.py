import pytest

from elo.application.use_cases.system_health_symbiont_bridge import SystemHealthSymbiontBridge
from elo.cognitive.system_health_assessment import (
    HealthSeverity,
    HealthState,
    SystemHealthFinding,
    assess_system_health,
)


def finding(
    finding_id: str,
    severity: HealthSeverity,
    *,
    weight: float = 1.0,
    dimension: str = "architecture",
    owner: str | None = "canonical-owner",
) -> SystemHealthFinding:
    return SystemHealthFinding(
        finding_id=finding_id,
        dimension=dimension,
        severity=severity,
        weight=weight,
        evidence_refs=(f"evidence:{finding_id}",),
        owner=owner,
    )


def test_empty_health_input_is_not_measured_not_false_healthy():
    result = assess_system_health(())
    assert result.state is HealthState.NOT_MEASURED
    assert result.score_percent is None
    assert result.canonical_mutation is False


def test_health_score_is_reproducible_from_explicit_weight_and_severity():
    result = assess_system_health((
        finding("pass", HealthSeverity.PASS, weight=2.0),
        finding("review", HealthSeverity.REVIEW, weight=1.0),
        finding("gap", HealthSeverity.GAP_HIGH, weight=1.0),
    ))
    # debt=(0*2)+(0.25*1)+(0.60*1)=0.85 over total weight 4
    assert result.score_percent == 78.75
    assert result.state is HealthState.ATTENTION
    assert [item.finding_id for item in result.priority_findings] == ["gap", "review"]


def test_block_is_never_hidden_by_high_average_score():
    result = assess_system_health((
        finding("healthy-large", HealthSeverity.PASS, weight=99.0),
        finding("unsafe-boundary", HealthSeverity.BLOCK, weight=1.0),
    ))
    assert result.score_percent == 99.0
    assert result.state is HealthState.BLOCKED
    assert result.priority_findings[0].finding_id == "unsafe-boundary"


def test_findings_without_evidence_are_rejected():
    with pytest.raises(ValueError, match="explicit evidence"):
        SystemHealthFinding(
            finding_id="gap",
            dimension="security",
            severity=HealthSeverity.GAP_HIGH,
            weight=1.0,
            evidence_refs=(),
        )


def test_symbiont_bridge_prioritizes_gap_but_does_not_self_authorize_remediation():
    assessment = assess_system_health((
        finding("authz-mt", HealthSeverity.GAP_HIGH, dimension="authorization", owner="elo-authz"),
        finding("duplicate-index", HealthSeverity.REVIEW, dimension="performance", owner="database-governance"),
    ))
    orientations = SystemHealthSymbiontBridge().orient(assessment)

    assert [item.finding_id for item in orientations] == ["authz-mt", "duplicate-index"]
    assert orientations[0].action == "BOUNDED_REMEDIATION"
    assert orientations[0].authorized is False
    assert orientations[0].owner == "elo-authz"


def test_external_authorization_can_be_reflected_without_becoming_health_authority():
    assessment = assess_system_health((
        finding("review", HealthSeverity.REVIEW),
    ))
    orientations = SystemHealthSymbiontBridge().orient(
        assessment,
        authorized_actions=frozenset({"INVESTIGATE_PROVENANCE"}),
    )
    assert orientations[0].authorized is True
    assert assessment.canonical_mutation is False


def test_pass_only_assessment_preserves_verified_state():
    assessment = assess_system_health((finding("healthy", HealthSeverity.PASS),))
    orientation = SystemHealthSymbiontBridge().orient(assessment)[0]
    assert assessment.score_percent == 100.0
    assert assessment.state is HealthState.HEALTHY
    assert orientation.action == "PRESERVE_VERIFIED_STATE"
