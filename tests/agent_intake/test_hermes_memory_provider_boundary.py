from src.elo.agent_intake.hermes_memory_provider_boundary import (
    ALLOWED_OPERATIONS,
    MAX_SOURCE_REFS,
    MemoryProviderDisposition,
    MemoryProviderSignal,
    assess_memory_provider,
)


def _signal(**kw):
    b = dict(
        provider_id="provider-a",
        tenant_scope="multiteiner",
        source_refs=("hermes:memory:1",),
        operation="retrieve",
        evidence_digest="sha256:abc",
        provenance_verified=True,
        explicit_activation=True,
    )
    b.update(kw)
    return MemoryProviderSignal(**b)


def test_verified_provider_is_candidate_only():
    a = assess_memory_provider(_signal())
    assert a.disposition is MemoryProviderDisposition.CANDIDATE
    assert a.canonical_authority is False
    assert a.mutation_permitted is False
    assert a.promotion_permitted is False


def test_discovery_without_activation_is_observation():
    assert assess_memory_provider(_signal(explicit_activation=False)).disposition is MemoryProviderDisposition.OBSERVATION


def test_missing_provenance_is_rejected():
    assert assess_memory_provider(_signal(provenance_verified=False)).disposition is MemoryProviderDisposition.REJECTED


def test_canonical_write_is_rejected():
    assert assess_memory_provider(_signal(canonical_write=True)).disposition is MemoryProviderDisposition.REJECTED


def test_promotion_attempt_is_rejected():
    assert assess_memory_provider(_signal(promotion_attempt=True)).disposition is MemoryProviderDisposition.REJECTED


def test_non_retrieval_operation_is_rejected():
    assert "retrieve" in ALLOWED_OPERATIONS
    assert assess_memory_provider(_signal(operation="write")).disposition is MemoryProviderDisposition.REJECTED


def test_excessive_source_refs_are_rejected():
    refs = tuple(f"hermes:memory:{i}" for i in range(MAX_SOURCE_REFS + 1))
    assert assess_memory_provider(_signal(source_refs=refs)).disposition is MemoryProviderDisposition.REJECTED


def test_boundary_accepts_maximum_source_refs():
    refs = tuple(f"hermes:memory:{i}" for i in range(MAX_SOURCE_REFS))
    assert assess_memory_provider(_signal(source_refs=refs)).disposition is MemoryProviderDisposition.CANDIDATE
