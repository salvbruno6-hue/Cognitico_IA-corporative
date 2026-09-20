"""Tests for the evaluation-to-implementation evidence adapter."""
from src.elo.agent_intake.hermes_current_extensions import build_candidate, evaluate_candidate
from src.elo.agent_intake.implementation_evidence_adapter import (
    measurement_to_implementation_evidence,
)


def test_adapter_preserves_existing_measurement_and_owner():
    candidate = build_candidate("EXT-CONTEXTREF-HERMES")
    measurement = evaluate_candidate(
        candidate,
        {"context_success": 1.0},
        {"context_success": 1.0},
        repeatable=True,
        metric_directions={"context_success": "maximize"},
    )

    evidence = measurement_to_implementation_evidence(
        candidate,
        measurement,
        metric_directions={"context_success": "maximize"},
        provenance_refs=("controlled-eval:628",),
        boundary_integrity=True,
    )

    assert evidence.candidate_id == candidate.candidate_id
    assert evidence.owner == "ELO Context"
    assert evidence.baseline == measurement.baseline
    assert evidence.adapted == measurement.adapted
    assert evidence.decision == measurement.result
    assert evidence.is_complete() is True


def test_adapter_does_not_fabricate_missing_provenance():
    candidate = build_candidate("EXT-CONTEXTREF-HERMES")
    measurement = evaluate_candidate(
        candidate,
        {"context_success": 1.0},
        {"context_success": 1.0},
        repeatable=True,
        metric_directions={"context_success": "maximize"},
    )

    evidence = measurement_to_implementation_evidence(
        candidate,
        measurement,
        metric_directions={"context_success": "maximize"},
        provenance_refs=(),
        boundary_integrity=True,
    )

    assert evidence.is_complete() is False


def test_adapter_rejects_mismatched_candidate():
    candidate = build_candidate("EXT-CONTEXTREF-HERMES")
    other = build_candidate("EXT-CHECKPOINT-HERMES")
    measurement = evaluate_candidate(
        candidate,
        {"context_success": 1.0},
        {"context_success": 1.0},
        repeatable=True,
        metric_directions={"context_success": "maximize"},
    )

    try:
        measurement_to_implementation_evidence(
            other,
            measurement,
            metric_directions={"context_success": "maximize"},
            provenance_refs=("controlled-eval:628",),
            boundary_integrity=True,
        )
    except ValueError as exc:
        assert "identifiers do not match" in str(exc)
    else:
        raise AssertionError("mismatched candidate must be rejected")
