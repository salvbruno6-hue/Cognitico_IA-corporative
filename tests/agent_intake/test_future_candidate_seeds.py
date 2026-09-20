from elo.agent_intake.future_candidate_seeds import prepare_future_candidate
from elo.agent_intake.hermes_current_extensions import build_candidate


def test_prepare_future_candidate_reuses_existing_elo_candidate_contract():
    result = prepare_future_candidate(
        build_candidate("EXT-CHECKPOINT-HERMES"),
        tenant_id="tenant-test",
        source_ref="hermes-checkpoint",
        source_commit="abc123",
        evidence_ids=("controlled-test:checkpoint",),
        validation_contract="controlled test -> measured gain -> repeatability -> Evolution Gate",
    )

    assert result.capability_id == "EXT-CHECKPOINT-HERMES"
    assert result.domain == "ELO State Recovery"
    assert result.state.value == "CANDIDATE"
    assert result.provenance["provider"] == "Hermes"


def test_prepare_future_candidate_rejects_missing_evidence():
    try:
        prepare_future_candidate(
            build_candidate("EXT-CHECKPOINT-HERMES"),
            tenant_id="tenant-test",
            source_ref="hermes-checkpoint",
            source_commit="abc123",
            evidence_ids=(),
            validation_contract="controlled evaluation",
        )
    except ValueError as exc:
        assert "evidence" in str(exc)
    else:
        raise AssertionError("missing evidence must be rejected")


def test_prepare_future_candidate_rejects_non_candidate_records():
    candidate = build_candidate("EXT-CHECKPOINT-HERMES")
    candidate = candidate.__class__(
        candidate.candidate_id,
        candidate.mechanism,
        candidate.owner,
        candidate.adaptation,
        candidate.evidence_state,
        "promoted",
        False,
    )

    try:
        prepare_future_candidate(
            candidate,
            tenant_id="tenant-test",
            source_ref="hermes-checkpoint",
            source_commit="abc123",
            evidence_ids=("evidence:1",),
            validation_contract="controlled evaluation",
        )
    except ValueError as exc:
        assert "candidate-only" in str(exc)
    else:
        raise AssertionError("non-candidate record must be rejected")


def test_prepare_future_candidate_never_marks_canonical_mutation():
    result = prepare_future_candidate(
        build_candidate("EXT-LEARN-HERMES"),
        tenant_id="tenant-test",
        source_ref="hermes-learn",
        source_commit="def456",
        evidence_ids=("controlled-test:learn",),
        validation_contract="incremental learning gain",
    )

    assert result.state.value == "CANDIDATE"
    assert result.provenance["origin"] == "hermes-future-candidate-adapter"
