from src.elo.agent_intake.hermes_batch_boundary import BatchDisposition, BatchSignal, assess_batch

def _signal(**overrides):
    values = dict(batch_id="batch-001", tenant_scope="tenant-a", source_refs=("hermes://batch",),
                  task_digest="sha256:task", item_count=4, bounded=True, explicit_authorization=True,
                  result_schema_digest="sha256:schema", canonical_mutation=False, promotion_attempt=False)
    values.update(overrides)
    return BatchSignal(**values)

def test_valid_bounded_batch_is_candidate():
    result = assess_batch(_signal())
    assert result.disposition is BatchDisposition.CANDIDATE
    assert result.canonical_authority is False
    assert result.execution_permitted is False
    assert result.promotion_permitted is False

def test_missing_identity_or_schema_is_rejected():
    assert assess_batch(_signal(batch_id="")).disposition is BatchDisposition.REJECTED
    assert assess_batch(_signal(result_schema_digest="")).disposition is BatchDisposition.REJECTED

def test_missing_provenance_is_rejected():
    assert assess_batch(_signal(source_refs=())).disposition is BatchDisposition.REJECTED

def test_canonical_mutation_or_promotion_is_rejected():
    assert assess_batch(_signal(canonical_mutation=True)).disposition is BatchDisposition.REJECTED
    assert assess_batch(_signal(promotion_attempt=True)).disposition is BatchDisposition.REJECTED

def test_unbounded_or_unauthorized_batch_is_observation():
    assert assess_batch(_signal(bounded=False)).disposition is BatchDisposition.OBSERVATION
    assert assess_batch(_signal(explicit_authorization=False)).disposition is BatchDisposition.OBSERVATION
