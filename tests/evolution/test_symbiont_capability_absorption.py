from elo.cognitive.symbiont_capability_absorption import (
    ExternalCapabilityObservation,
    SymbiontCapabilityAbsorber,
)
from elo.cognitive.symbiont_pattern_intake import ExternalPatternInput, SymbiontPatternIntake


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
    return pattern, decision, observation


def test_absorbs_external_capability_as_noncanonical_candidate():
    _, decision, observation = _inputs()
    candidate = SymbiontCapabilityAbsorber.absorb(
        observation,
        decision,
        validation_contract="benchmark multi-step research against baseline",
    )

    assert candidate is not None
    assert candidate.state.value == "CANDIDATE"
    assert candidate.portable_principle == observation.mechanism
    assert candidate.provenance["provider"] == "hermes"
    assert candidate.provenance["origin"] == "symbiont-external-capability"


def test_does_not_absorb_noncompatible_external_capability():
    _, decision, observation = _inputs()
    blocked = decision.__class__(
        pattern=decision.pattern,
        classification=decision.classification.ADAPT_REQUIRED,
        disposition="LAB_EXPERIMENT",
        rationale="insufficient maturity",
        proposal=decision.proposal,
    )

    assert SymbiontCapabilityAbsorber.absorb(
        observation,
        blocked,
        validation_contract="benchmark against baseline",
    ) is None


def test_rejects_cross_source_capability():
    _, decision, observation = _inputs()
    mismatched = ExternalCapabilityObservation(
        **{**observation.__dict__, "source_commit": "different"}
    )

    try:
        SymbiontCapabilityAbsorber.absorb(
            mismatched,
            decision,
            validation_contract="benchmark against baseline",
        )
    except ValueError as exc:
        assert "source commit" in str(exc)
    else:
        raise AssertionError("cross-source capability must be rejected")
