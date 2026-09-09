import pytest

from elo.core.mature_interaction import (
    InteractionPosture,
    MatureInteractionProfile,
    choose_interaction_posture,
)


def test_default_profile_is_mature_and_contextual() -> None:
    profile = MatureInteractionProfile()

    assert profile.tone == "mature"
    assert profile.guidance == "orienting"
    assert profile.wisdom == "evidence_based"
    assert profile.immersion == "continuous_context"
    assert "never_invent_evidence" in profile.principles()
    assert "never_replace_authorized_human_decision" in profile.principles()


def test_explaining_ambiguous_context_prefers_listening() -> None:
    assert (
        choose_interaction_posture(
            user_is_explaining=True,
            ambiguity=0.7,
            decision_relevance=0.4,
            risk=0.1,
            evidence_gap=0.2,
            user_requested_recommendation=False,
        )
        == InteractionPosture.LISTEN
    )


def test_high_risk_prefers_guard() -> None:
    assert (
        choose_interaction_posture(
            user_is_explaining=False,
            ambiguity=0.2,
            decision_relevance=0.8,
            risk=0.9,
            evidence_gap=0.1,
            user_requested_recommendation=False,
        )
        == InteractionPosture.GUARD
    )


def test_evidence_gap_or_ambiguity_drives_investigation() -> None:
    assert (
        choose_interaction_posture(
            user_is_explaining=False,
            ambiguity=0.7,
            decision_relevance=0.7,
            risk=0.2,
            evidence_gap=0.2,
            user_requested_recommendation=False,
        )
        == InteractionPosture.INVESTIGATE
    )


def test_requested_recommendation_is_respected() -> None:
    assert (
        choose_interaction_posture(
            user_is_explaining=False,
            ambiguity=0.2,
            decision_relevance=0.5,
            risk=0.1,
            evidence_gap=0.1,
            user_requested_recommendation=True,
        )
        == InteractionPosture.RECOMMEND
    )


def test_invalid_signals_fail_closed() -> None:
    with pytest.raises(ValueError):
        choose_interaction_posture(
            user_is_explaining=False,
            ambiguity=1.1,
            decision_relevance=0.5,
            risk=0.1,
            evidence_gap=0.1,
            user_requested_recommendation=False,
        )
