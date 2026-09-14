import pytest

from elo.cognitive.autonomous_reasoning import AutonomousExecutionPlan, AutonomousReasoning
from elo.cognitive.domain_intelligence import DomainIntelligence, DomainIntelligenceObservation


def domain(**overrides):
    values = dict(
        observation_id="domain-001",
        tenant_id="multiteiner",
        target="example.test",
        source_ref="external-evidence/domain-intel",
        source_commit="source-commit-001",
        evidence_ids=("ev-domain-001",),
        observations=("passive source observed",),
        limitations=("acquisition availability may vary",),
    )
    values.update(overrides)
    return DomainIntelligenceObservation(**values)


def autonomous(**overrides):
    values = dict(
        plan_id="autonomy-001",
        tenant_id="multiteiner",
        objective="evaluate a bounded maintenance hypothesis",
        planned_actions=("inspect evidence", "run isolated validation"),
        expected_outcome="candidate evidence collected",
        evidence_ids=("ev-autonomy-001",),
        constraints=("no canonical writes", "bounded execution"),
        limitations=("execution provider is not part of the native contract",),
        source_ref="external-evidence/autonomous-plan",
        source_commit="source-commit-001",
    )
    values.update(overrides)
    return AutonomousExecutionPlan(**values)


def test_domain_intelligence_is_native_and_provider_neutral():
    decision = DomainIntelligence().classify(domain())
    assert decision.disposition == "LAB_CANDIDATE"
    assert decision.candidate_creation_allowed
    assert decision.pattern.scope == "elo-domain-intelligence"
    assert decision.pattern.source_kind == "external_evidence"


def test_domain_intelligence_rejects_missing_uncertainty():
    with pytest.raises(ValueError, match="requires limitations"):
        domain(limitations=())


def test_domain_intelligence_rejects_credentials():
    with pytest.raises(ValueError, match="credentials or secrets"):
        domain(metadata={"authorization": "secret"})


def test_autonomous_reasoning_is_native_and_bounded():
    decision = AutonomousReasoning().classify(autonomous(), "candidate evidence collected")
    assert decision.disposition == "LAB_CANDIDATE"
    assert decision.candidate_creation_allowed
    assert decision.pattern.scope == "elo-autonomous-reasoning"
    assert decision.pattern.source_kind == "external_evidence"


def test_autonomous_requires_bounds_and_evidence():
    with pytest.raises(ValueError, match="bounded planned actions"):
        autonomous(planned_actions=())
    with pytest.raises(ValueError, match="requires evidence"):
        autonomous(evidence_ids=())


def test_autonomous_requires_limits_to_prevent_false_certainty():
    with pytest.raises(ValueError, match="requires limitations"):
        autonomous(limitations=())


def test_autonomous_requires_observed_outcome():
    with pytest.raises(ValueError, match="observed_outcome is required"):
        AutonomousReasoning().classify(autonomous(), "")
