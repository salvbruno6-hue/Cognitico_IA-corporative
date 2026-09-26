from elo.agent_intake.hermes_learning_adapter import adapt_skill_learning
from elo.agent_intake.hermes_learning_boundary import LearningState, SkillLearningSignal

def signal(**overrides):
    v=dict(signal_id="learn-test",tenant_scope="multiteiner",source_refs=("controlled-eval:learn/1",),
           skill_name="skill-test",instruction_digest="digest-test",user_directed=True,verified=True)
    v.update(overrides); return SkillLearningSignal(**v)

def test_admits_verified_skill_as_candidate_contract():
    c=adapt_skill_learning(signal())
    assert c is not None
    assert c.state is LearningState.CANDIDATE
    assert not c.promotion_authority and not c.canonical_mutation

def test_unverified_skill_is_not_admitted():
    assert adapt_skill_learning(signal(verified=False)) is None

def test_requires_provenance():
    assert adapt_skill_learning(signal(source_refs=())) is None
