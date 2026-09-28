from types import SimpleNamespace

import pytest

from elo.agent_intake.hermes_symbiont_loop import apply_candidate_through_symbiont


def _implementation(*, result="READY_FOR_ELO_REVIEW", next_state="ELO_REVIEW", canonical_mutation=False):
    return SimpleNamespace(
        result=result,
        next_state=next_state,
        canonical_mutation=canonical_mutation,
    )


def test_candidate_enters_persistent_symbiont_boundary_and_stops_at_review():
    evidence = SimpleNamespace(candidate_id="EXT-PROFILE-HERMES")

    result = apply_candidate_through_symbiont(
        "EXT-PROFILE-HERMES",
        lambda: (_implementation(), evidence),
    )

    assert result.candidate_id == "EXT-PROFILE-HERMES"
    assert result.status == "ACTIVE"
    assert result.next_state == "ELO_REVIEW"
    assert result.evidence is evidence
    assert result.canonical_mutation is False


def test_symbiont_fails_closed_when_candidate_attempts_canonical_mutation():
    evidence = SimpleNamespace(candidate_id="EXT-PROFILE-HERMES")

    result = apply_candidate_through_symbiont(
        "EXT-PROFILE-HERMES",
        lambda: (
            _implementation(
                result="IMPLEMENTATION_AUTHORIZED",
                next_state="IMPLEMENTATION_AUTHORIZED",
                canonical_mutation=True,
            ),
            evidence,
        ),
    )

    assert result.status == "HUMAN_APPROVAL_REQUIRED"
    assert result.canonical_mutation is True


def test_symbiont_fails_closed_when_candidate_self_authorizes_without_mutation():
    evidence = SimpleNamespace(candidate_id="EXT-PROFILE-HERMES")

    result = apply_candidate_through_symbiont(
        "EXT-PROFILE-HERMES",
        lambda: (
            _implementation(
                result="IMPLEMENTATION_AUTHORIZED",
                next_state="IMPLEMENTATION_AUTHORIZED",
                canonical_mutation=False,
            ),
            evidence,
        ),
    )

    assert result.status == "HUMAN_APPROVAL_REQUIRED"
    assert result.next_state == "HUMAN_APPROVAL_REQUIRED"
    assert result.canonical_mutation is False
