from elo.agent_intake.hermes_learning_boundary import (
    CAPABILITY_ID, GRAPH_CAPABILITY_ID, LearningGraphRelation, SkillLearningSignal,
    evaluate_skill_learning, validate_graph_relation,
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

def test_learning_graph_requires_evidence():
    try:
        validate_graph_relation(LearningGraphRelation("rel-001", "memory:1", "skill:x", "SUPPORTS", ()))
    except ValueError as exc:
        assert "evidence" in str(exc)
    else:
        raise AssertionError("relation without evidence must fail")

def test_learning_graph_is_not_authority():
    relation = validate_graph_relation(LearningGraphRelation("rel-002", "memory:1", "skill:x", "DERIVED_FROM", ("evidence-1",)))
    assert relation.canonical_authority is False
    assert GRAPH_CAPABILITY_ID.startswith("EXT-LEARNING-GRAPH")
