from dataclasses import replace

from elo.cognitive.symbiont_promotion_filter import PromotionRecommendation, SymbiontPromotionFilter
from elo.cognitive.symbionte_lab import SymbiontLabEvaluation, SymbiontLabObservation
from elo.core.learning_governance import LearningCandidate


def observation(**overrides):
    data = dict(
        observation_id="obs-1",
        tenant_id="tenant-a",
        domain="EVOLUTION",
        decision_id="decision-1",
        expected_outcome="expected",
        observed_outcome="observed",
        evidence_ids=("e-1",),
        source_ref="runtime://obs/1",
        source_commit="abc123",
        hypothesis="hypothesis",
        baseline="baseline",
        experiment="experiment",
        result="result",
        regression_status="NO_REGRESSION",
        generalization_status="CONFIRMED",
        risk="LOW",
        existing_owner=None,
        scope="EAIF_ANALYTICAL_ANTI_PATTERN",
        tenant_scope="tenant-a",
        source_kind="experience",
    )
    data.update(overrides)
    return SymbiontLabObservation(**data)


def candidate(state="CANDIDATE"):
    return LearningCandidate(
        candidate_id="cand-1",
        experience_id="exp-1",
        tenant_id="tenant-a",
        domain="EVOLUTION",
        hypothesis="hypothesis",
        dataset_version="ds-1",
        provenance={"experience_id": "exp-1"},
        state=state,
    )


def evaluation(**overrides):
    data = dict(
        observation=observation(),
        experience=None,
        candidate=candidate(),
        evolution_classification="COMPATIBLE",
        disposition="CANDIDATE_FOR_GOVERNED_LEARNING",
    )
    data.update(overrides)
    return SymbiontLabEvaluation(**data)


def test_confirmed_low_risk_compatible_candidate_recommends_promote():
    result = SymbiontPromotionFilter.assess(evaluation())
    assert result.recommendation is PromotionRecommendation.PROMOTE
    assert result.canonical_mutation_allowed is False


def test_partial_generalization_recommends_strengthen():
    ev = evaluation(observation=observation(generalization_status="PARTIAL"))
    assert SymbiontPromotionFilter.assess(ev).recommendation is PromotionRecommendation.STRENGTHEN


def test_duplicate_recommends_reuse():
    ev = evaluation(candidate=None, evolution_classification="DUPLICATE/SUPERSEDED", disposition="REUSE")
    assert SymbiontPromotionFilter.assess(ev).recommendation is PromotionRecommendation.REUSE


def test_conflict_recommends_block():
    ev = evaluation(candidate=None, evolution_classification="EVOLUTIONARY_CONFLICT", disposition="BLOCK")
    assert SymbiontPromotionFilter.assess(ev).recommendation is PromotionRecommendation.BLOCK


def test_high_risk_never_recommends_promote():
    ev = evaluation(observation=observation(risk="HIGH"))
    assert SymbiontPromotionFilter.assess(ev).recommendation is PromotionRecommendation.STRENGTHEN


def test_missing_candidate_requires_strengthening():
    ev = evaluation(candidate=None)
    assert SymbiontPromotionFilter.assess(ev).recommendation is PromotionRecommendation.STRENGTHEN
