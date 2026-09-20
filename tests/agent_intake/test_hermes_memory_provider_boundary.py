from src.elo.agent_intake.hermes_memory_provider_boundary import MemoryProviderSignal,MemoryProviderDisposition,assess_memory_provider
def _signal(**kw):
    b=dict(provider_id="provider-a",tenant_scope="multiteiner",source_refs=("hermes:memory:1",),operation="retrieve",evidence_digest="sha256:abc",provenance_verified=True,explicit_activation=True); b.update(kw); return MemoryProviderSignal(**b)
def test_verified_provider_is_candidate_only():
    a=assess_memory_provider(_signal()); assert a.disposition is MemoryProviderDisposition.CANDIDATE and a.canonical_authority is False and a.mutation_permitted is False and a.promotion_permitted is False
def test_discovery_without_activation_is_observation(): assert assess_memory_provider(_signal(explicit_activation=False)).disposition is MemoryProviderDisposition.OBSERVATION
def test_missing_provenance_is_rejected(): assert assess_memory_provider(_signal(provenance_verified=False)).disposition is MemoryProviderDisposition.REJECTED
def test_canonical_write_is_rejected(): assert assess_memory_provider(_signal(canonical_write=True)).disposition is MemoryProviderDisposition.REJECTED
def test_promotion_attempt_is_rejected(): assert assess_memory_provider(_signal(promotion_attempt=True)).disposition is MemoryProviderDisposition.REJECTED
