import pytest

from elo.contracts.absorption_envelope import AbsorptionEnvelopeError, GovernedAbsorptionEnvelope


def test_valid_envelope_preserves_lineage():
    envelope = GovernedAbsorptionEnvelope().prepare(
        candidate_id="c-1", tenant_id="t-1", source_ref="repo", source_commit="abc",
        mechanism="retry", evidence_ids=["e-1"], scope="lab", risk="LOW",
        provenance={"source_ref": "repo", "source_commit": "abc"},
    )
    assert envelope.state == "CANDIDATE"
    assert envelope.provenance["source_commit"] == "abc"


def test_mismatched_lineage_and_missing_evidence_block():
    with pytest.raises(AbsorptionEnvelopeError):
        GovernedAbsorptionEnvelope().prepare(
            candidate_id="c", tenant_id="t", source_ref="repo", source_commit="abc",
            mechanism="x", evidence_ids=["e"], scope="lab", risk="LOW",
            provenance={"source_ref": "other", "source_commit": "abc"},
        )
    with pytest.raises(AbsorptionEnvelopeError):
        GovernedAbsorptionEnvelope().prepare(
            candidate_id="c", tenant_id="t", source_ref="repo", source_commit="abc",
            mechanism="x", evidence_ids=[], scope="lab", risk="LOW",
            provenance={"source_ref": "repo", "source_commit": "abc"},
        )


def test_secret_metadata_is_fail_closed():
    with pytest.raises(AbsorptionEnvelopeError):
        GovernedAbsorptionEnvelope().prepare(
            candidate_id="c", tenant_id="t", source_ref="repo", source_commit="abc",
            mechanism="x", evidence_ids=["e"], scope="lab", risk="HIGH",
            provenance={"source_ref": "repo", "source_commit": "abc", "api_key": "x"},
        )
