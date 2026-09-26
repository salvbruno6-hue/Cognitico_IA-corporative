from elo.agent_intake.hermes_memory_provider_adapter import adapt_memory_provider
from elo.agent_intake.hermes_memory_provider_boundary import MemoryProviderDisposition, MemoryProviderSignal


def signal(**overrides):
    values = dict(
        provider_id="provider-test",
        tenant_scope="multiteiner",
        source_refs=("controlled-eval:memory/1",),
        operation="retrieve",
        evidence_digest="sha256:test",
        provenance_verified=True,
        explicit_activation=True,
        canonical_write=False,
        promotion_attempt=False,
    )
    values.update(overrides)
    return MemoryProviderSignal(**values)


def test_adapts_retrieval_provider_to_bounded_contract():
    contract = adapt_memory_provider(signal())
    assert contract is not None
    assert contract.disposition is MemoryProviderDisposition.CANDIDATE
    assert contract.memory_authority is False
    assert contract.mutation_permitted is False
    assert contract.promotion_permitted is False


def test_rejects_canonical_write():
    assert adapt_memory_provider(signal(canonical_write=True)) is None


def test_rejects_promotion_attempt():
    assert adapt_memory_provider(signal(promotion_attempt=True)) is None
