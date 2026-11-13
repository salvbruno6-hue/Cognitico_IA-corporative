from elo.agent_intake.hermes_current_delta_20261004 import CURRENT_DELTAS, validate_current_deltas

def test_registry():
    assert validate_current_deltas() == 9

def test_unique_ids():
    assert len({x.mechanism_id for x in CURRENT_DELTAS}) == 9

def test_candidate_state():
    assert all(x.candidate_only for x in CURRENT_DELTAS)
    assert all(not x.canonical_mutation for x in CURRENT_DELTAS)

def test_owner_reuse():
    owners = {x.elo_owner for x in CURRENT_DELTAS}
    assert "ELO Agent Delegation" in owners
    assert "ELO Workflow/Automation" in owners
    assert "ELO External Capability Gateway" in owners
