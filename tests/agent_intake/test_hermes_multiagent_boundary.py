from src.elo.agent_intake.hermes_multiagent_boundary import (
    DelegationSignal, DelegationDisposition, assess_delegation,
)

def _signal(**kw):
    base = dict(delegation_id="del-001", tenant_scope="multiteiner",
                parent_agent_id="elo", child_agent_id="worker-1",
                goal_digest="abc", source_refs=("hermes:delegation:1",),
                provenance_verified=True, isolated_context=True)
    base.update(kw)
    return DelegationSignal(**base)

def test_isolated_verified_delegation_is_candidate_only():
    a = assess_delegation(_signal())
    assert a.disposition is DelegationDisposition.CANDIDATE
    assert a.canonical_authority is False
    assert a.promotion_permitted is False

def test_shared_context_remains_observation():
    a = assess_delegation(_signal(isolated_context=False))
    assert a.disposition is DelegationDisposition.OBSERVATION

def test_child_cannot_claim_authority():
    a = assess_delegation(_signal(child_authority=True))
    assert a.disposition is DelegationDisposition.REJECTED

def test_missing_provenance_is_rejected():
    a = assess_delegation(_signal(provenance_verified=False))
    assert a.disposition is DelegationDisposition.REJECTED

def test_missing_goal_is_rejected():
    a = assess_delegation(_signal(goal_digest=""))
    assert a.disposition is DelegationDisposition.REJECTED
