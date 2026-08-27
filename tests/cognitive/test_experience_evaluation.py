from elo.cognitive.learning.experience_evaluation import (
    Experience,
    ExperienceEvaluator,
    LearningCandidateBuilder,
)


def test_verified_experience_becomes_candidate_not_canonical_knowledge():
    experience = Experience(
        tenant_id="tenant-a",
        capability="calculation",
        context={"domain": "budget"},
        model_id=None,
        tool_id="deterministic-calculator",
        result={"value": 10},
        verified=True,
    )
    evaluation = ExperienceEvaluator().evaluate(experience)
    candidate = LearningCandidateBuilder().build(experience, evaluation)
    assert candidate["promotion_state"] == "candidate"
    assert candidate["tenant_id"] == "tenant-a"


def test_unverified_experience_cannot_be_learning_candidate():
    experience = Experience(
        tenant_id="tenant-a",
        capability="calculation",
        context={},
        model_id=None,
        tool_id="calculator",
        result=None,
        verified=False,
    )
    evaluation = ExperienceEvaluator().evaluate(experience)
    assert LearningCandidateBuilder().build(experience, evaluation) is None
