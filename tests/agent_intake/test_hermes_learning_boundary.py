from src.elo.agent_intake.hermes_learning_boundary import (
    CAPABILITY_ID, SkillLearningSignal, evaluate_skill_learning,
)

def signal(*, refs=("source-1",), verified=True):
    return SkillLearningSignal("learn-001", "tenant-a", refs, "example-skill", "digest-001", True, verified)

def test_verified_learning_becomes_candidate_only():
    result = evaluate_skill_learning(signal())
    assert result.capability_id == CAPABILITY_ID
    assert result.state == "CANDIDATE"
    assert result.admitted is True
    assert result.promotion_authority is False

def test_unverified_learning_stays_observation():
    result = evaluate_skill_learning(signal(verified=False))
    assert result.state == "OBSERVED"
    assert result.admitted is False

def test_missing_provenance_is_rejected():
    result = evaluate_skill_learning(signal(refs=()))
    assert result.state == "REJECTED"
    assert result.admitted is False

def test_learning_identity_is_required():
    try:
        evaluate_skill_learning(SkillLearningSignal("", "tenant-a", ("source-1",), "skill", "digest", True, True))
    except ValueError as exc:
        assert "identity" in str(exc)
    else:
        raise AssertionError("missing signal identity must fail")
