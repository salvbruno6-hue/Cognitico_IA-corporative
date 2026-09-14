import pytest

from elo.cognitive.hermes_autonomous_observation import (
    HermesAutonomousIntake,
    HermesAutonomousObservation,
)
from elo.cognitive.hermes_domain_intelligence import (
    DomainIntelligenceObservation,
    HermesDomainIntelligence,
)


def domain(**overrides):
    values = dict(
        observation_id="domain-001",
        tenant_id="multiteiner",
        target="example.test",
        source_ref="salvbruno6-hue/ELO-Hermes-Agent",
        source_commit="b774519a1e6396f741e13fb6e81894044d66755e",
        evidence_ids=("ev-domain-001",),
        observations=("passive source observed",),
        limitations=("network availability may vary",),
    )
    values.update(overrides)
    return DomainIntelligenceObservation(**values)


def autonomous(**overrides):
    values = dict(
        observation_id="autonomy-001",
        tenant_id="multiteiner",
        agent_skill="hermes-agent",
        source_ref="salvbruno6-hue/ELO-Hermes-Agent",
        source_commit="b774519a1e6396f741e13fb6e81894044d66755e",
        objective="evaluate a bounded maintenance hypothesis",
        planned_actions=("inspect evidence", "run isolated validation"),
        observed_outcome="candidate evidence collected",
        evidence_ids=("ev-autonomy-001",),
        constraints=("no canonical writes", "bounded execution"),
        limitations=("provider execution not reproduced in this unit test",),
    )
    values.update(overrides)
    return HermesAutonomousObservation(**values)


def test_domain_intelligence_reaches_existing_evolution_spine():
    decision = HermesDomainIntelligence().classify(domain())
    assert decision.disposition == "LAB_CANDIDATE"
    assert decision.candidate_creation_allowed
    assert decision.pattern.scope == "symbiont-hermes-domain-intelligence"
    assert decision.proposal.provenance["source_commit"]


def test_domain_intelligence_rejects_missing_uncertainty():
    with pytest.raises(ValueError, match="requires limitations"):
        domain(limitations=())


def test_domain_intelligence_rejects_credentials():
    with pytest.raises(ValueError, match="credentials or secrets"):
        domain(metadata={"authorization": "secret"})


def test_autonomous_experience_reaches_gate_as_candidate_only():
    decision = HermesAutonomousIntake().classify(autonomous())
    assert decision.disposition == "LAB_CANDIDATE"
    assert decision.candidate_creation_allowed
    assert decision.pattern.scope == "symbiont-hermes-autonomous-agents"
    assert decision.proposal.provenance["source_kind"] == "hermes_autonomous_agent"


def test_autonomous_requires_bounds_and_evidence():
    with pytest.raises(ValueError, match="bounded planned actions"):
        autonomous(planned_actions=())
    with pytest.raises(ValueError, match="requires evidence"):
        autonomous(evidence_ids=())


def test_autonomous_requires_limits_to_prevent_false_certainty():
    with pytest.raises(ValueError, match="requires limitations"):
        autonomous(limitations=())
