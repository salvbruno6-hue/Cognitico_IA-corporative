from elo.agent_intake.hermes_batch_adapter import adapt_batch
from elo.agent_intake.hermes_batch_boundary import BatchDisposition, BatchSignal

def signal(**overrides):
    v=dict(batch_id="batch-test",tenant_scope="multiteiner",source_refs=("controlled-eval:batch/1",),
           task_digest="task-1",item_count=5,bounded=True,explicit_authorization=True,
           result_schema_digest="schema-v1",canonical_mutation=False,promotion_attempt=False)
    v.update(overrides); return BatchSignal(**v)

def test_adapts_bounded_batch():
    c=adapt_batch(signal())
    assert c is not None
    assert c.disposition is BatchDisposition.CANDIDATE
    assert not c.execution_permitted and not c.canonical_authority and not c.promotion_permitted

def test_rejects_canonical_mutation():
    assert adapt_batch(signal(canonical_mutation=True)) is None

def test_rejects_promotion_attempt():
    assert adapt_batch(signal(promotion_attempt=True)) is None
