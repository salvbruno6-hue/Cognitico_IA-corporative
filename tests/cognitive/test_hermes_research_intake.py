import pytest

from elo.cognitive.hermes_research_intake import (
    HermesResearchIntake,
    HermesResearchObservation,
)


def observation(**overrides):
    values = {
        "observation_id": "research-001",
        "tenant_id": "multiteiner",
        "skill": "domain-intel",
        "domain": "research",
        "source_ref": "salvbruno6-hue/ELO-Hermes-Agent",
        "source_commit": "1b38e71ffe3b3ee4b334e174eff6df72ce2fd08",
        "evidence_ids": ("ev-research-001",),
        "question": "assess the passive domain intelligence capability",
        "findings": ("structured JSON output", "passive sources"),
        "limitations": ("WHOIS may be blocked", "availability is heuristic"),
    }
    values.update(overrides)
    return HermesResearchObservation(**values)


def test_research_observation_enters_existing_evolution_intake():
    decision = HermesResearchIntake().classify(observation())

    assert decision.disposition == "LAB_CANDIDATE"
    assert decision.candidate_creation_allowed
    assert decision.proposal.provenance["source_ref"] == "salvbruno6-hue/ELO-Hermes-Agent"
    assert decision.proposal.provenance["source_commit"] == "1b38e71ffe3b3ee4b334e174eff6df72ce2fd08"
    assert decision.pattern.scope == "symbiont-hermes-research"


def test_research_requires_evidence_before_gate():
    with pytest.raises(ValueError, match="requires evidence"):
        observation(evidence_ids=())


def test_research_requires_limitations_to_preserve_uncertainty():
    with pytest.raises(ValueError, match="requires limitations"):
        observation(limitations=())


def test_research_rejects_credentials_in_metadata():
    with pytest.raises(ValueError, match="credentials or secrets"):
        observation(metadata={"authorization": "Bearer secret"})
