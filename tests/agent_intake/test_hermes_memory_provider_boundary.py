from src.elo.agent_intake.hermes_memory_provider_boundary import (
    MemoryProviderSignal, MemoryProviderDisposition, assess_memory_provider,
)

def _signal(**kw):
    base = dict(provider_id="openviking", tenant_scope="multiteiner",
                source_refs=("hermes:memory:1",), operation="retrieve",
                evidence_digest="sha256:abc", provenance_verified=True,
                explicit_activation=True)
    base.update(kw)
    return MemoryProviderSignal(**base)

def test_verified_explicit_provider_is_candidate_only():
    a = assess_memory_provider(_signal())
    assert a.disposition is MemoryProviderDisposition.CANDIDATE
    assert a.canonical_authority is False
    assert a.mutation_permitted is False
    assert a.promotion_permitted is False

def test_provider_discovery_without_activation_is_observation():
    a = assess_memory_provider(_signal(explicit_activation=False))
    assert a.disposition is MemoryProviderDisposition.OBSERVATION

def test_missing_provenance_is_rejected():
    a = assess_memory_provider(_signal(provenance_verified=False))
    assert a.disposition is MemoryProviderDisposition.REJECTED

def test_canonical_write_is_rejected():
    a = assess_memory_provider(_signal(canonical_write=True))
    assert a.disposition is MemoryProviderDisposition.REJECTED

def test_promotion_attempt_is_rejected():
    a = assess_memory_provider(_signal(promotion_attempt=True))
    assert a.disposition is MemoryProviderDisposition.REJECTED
