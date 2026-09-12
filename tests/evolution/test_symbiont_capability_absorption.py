import pytest
from dataclasses import replace

from elo.cognitive.symbiont_capability_absorption import (
    ExternalCapabilityObservation,
    SymbiontCapabilityAbsorber,
)
from elo.cognitive.symbiont_pattern_intake import ExternalPatternInput, SymbiontPatternIntake
from elo.core.evolution_gate import EvolutionClassification


def _inputs():
    pattern = ExternalPatternInput(
        pattern_id="pat-hermes-research-001",
        tenant_id="multiteiner",
        domain="research",
        source_ref="hermes:skill:multi-step-research",
        source_commit="abc123",
        problem="research requires multi-step decomposition",
        mechanism="decompose, research, cross-check, synthesize",
        evidence_ids=("ev-001", "ev-002"),
        source_kind="runtime",
    )
    decision = SymbiontPatternIntake().classify(pattern)
    observation = ExternalCapabilityObservation(
        capability_id="cap-multi-step-research",
        provider="hermes",
        capability="multi-step research",
        purpose="produce evidence-backed research",
        mechanism="decompose, research, cross-check, synthesize",
        interface_contract="accept mission and return evidence-backed result",
        evidence_ids=("ev-001", "ev-002"),
        source_ref="hermes:skill:multi-step-research",
        source_commit="abc123",
        tenant_id="multiteiner",
        domain="research",
    )
    return decision, observation


def test_absorbs_external_capability_as_noncanonical_candidate():
    decision, observation = _inputs()
    candidate = SymbiontCapabilityAbsorber.absorb(
        observation,
        decision,
        validation_contract="benchmark multi-step research against baseline",
    )

    assert candidate is not None
    assert candidate.state is not None
    assert candidate.state.value == "CANDIDATE"
    assert candidate.portable_principle == observation.mechanism
    assert candidate.provenance["provider"] == "hermes"
    assert candidate.provenance["origin"] == "symbiont-external-capability"


def test_does_not_absorb_noncompatible_external_capability():
    decision, observation = _inputs()
    blocked = replace(
        decision,
        classification=EvolutionClassification.ADAPT_REQUIRED,
        disposition="LAB_EXPERIMENT",
        rationale="insufficient maturity",
    )

    assert SymbiontCapabilityAbsorber.absorb(
        observation,
        blocked,
        validation_contract="benchmark against baseline",
    ) is None


def test_rejects_cross_source_capability():
    decision, observation = _inputs()
    mismatched = replace(observation, source_commit="different")

    with pytest.raises(ValueError, match="source commit"):
        SymbiontCapabilityAbsorber.absorb(
            mismatched,
            decision,
            validation_contract="benchmark against baseline",
        )


def test_rejects_existing_canonical_owner_even_if_decision_is_tampered():
    decision, observation = _inputs()
    tampered = replace(
        decision,
        classification=EvolutionClassification.COMPATIBLE,
        proposal=replace(decision.proposal, existing_owner="elo.core.canonical_capability"),
    )

    with pytest.raises(ValueError, match="existing canonical owner"):
        SymbiontCapabilityAbsorber.absorb(
            observation,
            tampered,
            validation_contract="benchmark against baseline",
        )


def test_rejects_evidence_mismatch_against_evolution_proposal():
    decision, observation = _inputs()
    mismatched = replace(observation, evidence_ids=("ev-other",))

    with pytest.raises(ValueError, match="evidence"):
        SymbiontCapabilityAbsorber.absorb(
            mismatched,
            decision,
            validation_contract="benchmark against baseline",
        )


def test_rejects_critical_risk():
    decision, observation = _inputs()
    critical = replace(observation, risk="CRITICAL")

    with pytest.raises(ValueError, match="critical-risk"):
        SymbiontCapabilityAbsorber.absorb(
            critical,
            decision,
            validation_contract="benchmark against baseline",
        )
