from elo.agent_intake.hermes_hook_boundary import HookDisposition, HookSignal, assess_hook
def signal(**changes):
    data = dict(signal_id="s1", tenant_scope="t1", lifecycle_event="controlled.guardrail",
                source_refs=("ref:1",), provenance_verified=True, guardrail_triggered=True)
    data.update(changes)
    return HookSignal(**data)
def test_verified_guardrail_hook_is_candidate_only():
    r = assess_hook(signal())
    assert r.disposition is HookDisposition.CANDIDATE
    assert r.canonical_authority is False and r.execution_authority is False and r.merge_permitted is False
def test_missing_provenance_is_rejected():
    assert assess_hook(signal(provenance_verified=False)).disposition is HookDisposition.REJECTED
def test_execution_or_bypass_is_rejected():
    assert assess_hook(signal(execution_authority=True)).disposition is HookDisposition.REJECTED
    assert assess_hook(signal(authorization_bypass=True)).disposition is HookDisposition.REJECTED
