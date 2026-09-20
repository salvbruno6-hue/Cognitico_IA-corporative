"""Controlled validation bridge for EXT-CHECKPOINT-HERMES.

This test proves the candidate maps to an existing native ELO capability
instead of introducing a parallel checkpoint authority.
"""

from src.elo.agent_intake.hermes_current_extensions import build_candidate, evaluate_candidate
from src.elo.agent_intake.native_capabilities import execute_candidate
from src.elo.agent_intake.state_recovery_integrity import evaluate_state_recovery


def test_checkpoint_candidate_maps_to_existing_native_recovery_without_promotion():
    candidate = build_candidate("EXT-CHECKPOINT-HERMES")

    assert candidate.owner == "ELO State Recovery"
    assert candidate.promotion_state == "candidate_only"
    assert candidate.canonical_mutation is False

    evidence = execute_candidate(
        "HERMES-CHECKPOINT",
        request_id="hermes-checkpoint-validation-01",
        tenant_scope="multiteiner",
    )

    assert evidence.status == "completed"
    assert evidence.outcome == {"restored": True}
    assert evidence.learning_candidate == {
        "promotion_state": "candidate_only",
        "canonical_mutation": False,
    }

    recovery = evaluate_state_recovery(
        request_id="hermes-checkpoint-validation-01",
        tenant_scope="multiteiner",
        state={"tenant_scope": "multiteiner", "value": "safe"},
    )

    assert recovery.status == "recovered"
    assert recovery.integrity_verified is True
    assert recovery.continuity_verified is True
    assert recovery.learning_candidate == {
        "promotion_state": "candidate_only",
        "canonical_mutation": False,
    }


def test_checkpoint_candidate_requires_repeatable_gain_before_evolution_gate():
    candidate = build_candidate("EXT-CHECKPOINT-HERMES")

    first = evaluate_candidate(
        candidate,
        {"recovery_integrity": 1.0},
        {"recovery_integrity": 1.0},
        repeatable=False,
    )
    repeatable = evaluate_candidate(
        candidate,
        {"recovery_integrity": 1.0},
        {"recovery_integrity": 1.0},
        repeatable=True,
    )

    assert first.result == "RETEST"
    assert repeatable.result == "RETEST"
