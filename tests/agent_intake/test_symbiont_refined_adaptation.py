"""Controlled tests for refined Symbiont adaptation into existing ELO capacities."""

import pytest

from elo.agent_intake.native_capabilities import CAPABILITY_IDS
from elo.agent_intake.symbiont_adaptation import (
    EXPERIENCE_SOURCES,
    PROFILES,
    refine_capability,
    refinement_is_eligible_for_test,
)


@pytest.mark.parametrize("capability_id", CAPABILITY_IDS)
def test_every_candidate_attaches_to_one_existing_elo_capacity(capability_id):
    adaptation = refine_capability(
        capability_id,
        {"controlled_test": True, "outcome": {"passed": True}},
    )

    assert adaptation.existing_capacity == PROFILES[capability_id].existing_capacity
    assert adaptation.capability_id == capability_id
    assert adaptation.mechanism
    assert adaptation.adjustment
    assert adaptation.rationale
    assert adaptation.expected_gain
    assert adaptation.source_experience == EXPERIENCE_SOURCES[capability_id]
    assert adaptation.promotion_state == "candidate_only"
    assert adaptation.canonical_mutation is False
    assert refinement_is_eligible_for_test(adaptation) is True


def test_symbiont_refinement_is_conservative_when_only_source_code_is_available():
    adaptation = refine_capability(
        "HERMES-MEMORY",
        {"source_reference": "OpenClaw: extensions/memory-core/index.ts"},
    )

    assert adaptation.evidence_quality == "reference_only"
    assert refinement_is_eligible_for_test(adaptation) is False
    assert adaptation.promotion_state == "candidate_only"
    assert adaptation.canonical_mutation is False


def test_live_execution_requires_outcome_evidence_before_refinement_test():
    adaptation = refine_capability(
        "HERMES-SKILLS",
        {"live_execution": True},
    )

    assert adaptation.evidence_quality == "insufficient"
    assert refinement_is_eligible_for_test(adaptation) is False


def test_failed_or_missing_evidence_cannot_become_canonical():
    for capability_id in CAPABILITY_IDS:
        adaptation = refine_capability(capability_id, {})
        assert adaptation.evidence_quality == "insufficient"
        assert adaptation.promotion_state == "candidate_only"
        assert adaptation.canonical_mutation is False


def test_eight_experiences_map_one_to_one_without_new_capability_authority():
    assert set(PROFILES) == set(CAPABILITY_IDS)
    assert set(EXPERIENCE_SOURCES) == set(CAPABILITY_IDS)
    assert len(PROFILES) == len(EXPERIENCE_SOURCES) == len(CAPABILITY_IDS) == 8
    assert len({profile.existing_capacity for profile in PROFILES.values()}) == 8
