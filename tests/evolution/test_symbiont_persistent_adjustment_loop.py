"""Tests for the Symbiont persistent adjustment signal."""

from elo.cognitive.symbiont_capability_evolution import CapabilityMetric, review_capabilities


def strong_metric():
    return CapabilityMetric.from_indirect_experience(
        item="EXT-CANDIDATE:capability-evolution",
        baseline=0.70,
        current=0.90,
        direction="maximize",
        evidence_refs=("performance-evidence:validated-downstream",),
        measurement_period="2026-09-LAB",
        observer_capability="ExecutionRouter",
        experience_ref="experience:validated-downstream-001",
        evidence_strength="STRONG",
        evolution_impact="STRONG",
    )


def test_strong_indirect_gain_keeps_adjustment_loop_active_until_production():
    review = review_capabilities(metrics=(strong_metric(),))
    assert review.ready_for_analysis is True
    assert review.persistent_adjustment_required is True
    assert review.production_pending is True
    assert "production execution" in review.next_intervention
    assert review.canonical_mutation is False


def test_persistent_adjustment_does_not_claim_production():
    review = review_capabilities(metrics=(strong_metric(),))
    assert review.production_pending is True
    assert all("cannot be relabeled as production evidence" in a.rationale for a in review.actions)


def test_standard_indirect_evidence_does_not_trigger_persistent_loop():
    metric = CapabilityMetric.from_indirect_experience(
        item="candidate:standard",
        baseline=0.70,
        current=0.90,
        direction="maximize",
        evidence_refs=("evidence:lab",),
        measurement_period="2026-09-LAB",
        observer_capability="ExecutionRouter",
        experience_ref="experience:001",
    )
    review = review_capabilities(metrics=(metric,))
    assert review.persistent_adjustment_required is False
    assert review.production_pending is False
