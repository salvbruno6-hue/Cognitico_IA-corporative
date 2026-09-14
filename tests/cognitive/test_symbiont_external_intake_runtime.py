import pytest

from elo.contracts.absorption_envelope import AbsorptionEnvelope, AbsorptionEnvelopeError, GovernedAbsorptionEnvelope
from elo.cognitive.symbiont_external_intake_runtime import NativeSymbiontExternalIntake


def envelope(**overrides):
    values = {
        "candidate_id": "ext-lab-001",
        "tenant_id": "multiteiner",
        "source_ref": "salvbruno6-hue/ELO-Hermes-Agent",
        "source_commit": "45ac26a217cc93603d19db8e4b9b064ca57d6806",
        "mechanism": "evidence-first bounded experimentation",
        "evidence_ids": ("ev-001",),
        "scope": "symbiont-external-intake",
        "risk": "LOW",
        "provenance": {
            "source_ref": "salvbruno6-hue/ELO-Hermes-Agent",
            "source_commit": "45ac26a217cc93603d19db8e4b9b064ca57d6806",
        },
    }
    values.update(overrides)
    return GovernedAbsorptionEnvelope().prepare(**values)


def test_valid_envelope_reaches_classified_lab_observation():
    result = NativeSymbiontExternalIntake().classify_for_lab(
        envelope(),
        problem="external mechanism needs controlled comparison",
        expected_outcome="reproducible observation",
        observed_outcome="reproducible observation",
        decision_id="decision-001",
        baseline="existing ELO intake",
        experiment="isolated comparison",
        result="mechanism generalized",
        regression_status="PASS",
        generalization_status="CONFIRMED",
    )
    assert result.decision.candidate_creation_allowed
    assert result.lab_observation is not None
    assert result.lab_observation.source_commit == envelope().source_commit
    assert result.lab_observation.evidence_ids == ("ev-001",)


def test_blocked_classification_does_not_create_lab_observation():
    result = NativeSymbiontExternalIntake().classify_for_lab(
        envelope(),
        problem="conflicting mechanism",
        expected_outcome="none",
        observed_outcome="none",
        decision_id="decision-002",
        baseline="existing",
        experiment="conflict",
        result="blocked",
        regression_status="PASS",
        generalization_status="CONFIRMED",
        existing_owner="canonical-owner",
    )
    assert result.lab_observation is None
    assert result.decision.disposition in {"REUSE", "BLOCK", "LAB_EXPERIMENT"}


def test_envelope_rejects_lineage_mismatch():
    with pytest.raises(AbsorptionEnvelopeError):
        envelope(provenance={"source_ref": "other", "source_commit": "45ac26a217cc93603d19db8e4b9b064ca57d6806"})


def test_envelope_rejects_missing_evidence():
    with pytest.raises(AbsorptionEnvelopeError):
        envelope(evidence_ids=())
