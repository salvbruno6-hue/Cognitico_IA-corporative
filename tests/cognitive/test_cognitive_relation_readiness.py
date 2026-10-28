from elo.cognitive.cognitive_relation_readiness import (
    CognitiveRelationCandidate,
    CognitiveRelationReadinessFilter,
)
from elo.cognitive.symbiont_promotion_filter import PromotionRecommendation
from elo.core.evolution_gate import EvolutionClassification


def candidate(**overrides):
    data = dict(
        relation_id="rel-1",
        evidence_ids=("EV-1",),
        confidence=0.7,
        source_exists=True,
        target_exists=True,
        generalization_status=None,
        regression_status="NONE",
        risk="MEDIUM",
        evolution_classification=None,
        governed_candidate_available=False,
        duplicate_found=False,
        conflict_open=False,
    )
    data.update(overrides)
    return CognitiveRelationCandidate(**data)


def test_missing_generalization_strengthens_instead_of_promoting():
    result = CognitiveRelationReadinessFilter.assess(candidate())
    assert result.recommendation is PromotionRecommendation.STRENGTHEN
    assert result.canonical_mutation_allowed is False


def test_missing_endpoint_blocks():
    result = CognitiveRelationReadinessFilter.assess(candidate(source_exists=False))
    assert result.recommendation is PromotionRecommendation.BLOCK


def test_duplicate_reuses_existing_relation():
    result = CognitiveRelationReadinessFilter.assess(candidate(duplicate_found=True))
    assert result.recommendation is PromotionRecommendation.REUSE


def test_regression_blocks():
    result = CognitiveRelationReadinessFilter.assess(
        candidate(generalization_status="CONFIRMED", regression_status="REGRESSION")
    )
    assert result.recommendation is PromotionRecommendation.BLOCK


def test_confirmed_compatible_governed_candidate_is_only_eligible_for_review():
    result = CognitiveRelationReadinessFilter.assess(
        candidate(
            generalization_status="CONFIRMED",
            risk="LOW",
            evolution_classification=EvolutionClassification.COMPATIBLE.value,
            governed_candidate_available=True,
        )
    )
    assert result.recommendation is PromotionRecommendation.PROMOTE
    assert result.canonical_mutation_allowed is False
