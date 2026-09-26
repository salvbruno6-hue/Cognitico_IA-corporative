from src.elo.agent_intake.hermes_curator_lifecycle import (
    CuratorSignal, LifecycleState, IntakeDisposition, assess_curator_signal,
)

def _signal(**kw):
    base = dict(signal_id="cur-001", tenant_scope="multiteiner", skill_id="skill-a",
                observed_state=LifecycleState.ACTIVE, source_refs=("hermes:curator:run:1",),
                curator_managed=True)
    base.update(kw)
    return CuratorSignal(**base)

def test_stale_requires_review_not_mutation():
    a = assess_curator_signal(_signal(observed_state=LifecycleState.STALE))
    assert a.disposition is IntakeDisposition.REVIEW_REQUIRED
    assert a.canonical_authority is False and a.mutation_permitted is False

def test_archived_is_retirement_candidate_only():
    a = assess_curator_signal(_signal(observed_state=LifecycleState.ARCHIVED))
    assert a.disposition is IntakeDisposition.RETIREMENT_CANDIDATE
    assert a.mutation_permitted is False

def test_pinned_skill_remains_observation():
    a = assess_curator_signal(_signal(observed_state=LifecycleState.ARCHIVED, pinned=True))
    assert a.disposition is IntakeDisposition.OBSERVATION

def test_user_directed_learning_is_not_curator_authority():
    a = assess_curator_signal(_signal(user_directed=True))
    assert a.disposition is IntakeDisposition.OBSERVATION

def test_missing_provenance_is_rejected():
    a = assess_curator_signal(_signal(source_refs=()))
    assert a.disposition is IntakeDisposition.REJECTED