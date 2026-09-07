import pytest

from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabObservation
from elo.core.learning_governance import GovernedLearningService


class MemoryStub:
    def __init__(self):
        self.calls = []

    def remember(self, **kwargs):
        self.calls.append(kwargs)


def make_observation(**overrides):
    values = dict(
        observation_id="obs-boundary-1",
        tenant_id="tenant-a",
        domain="ORCAMENTO",
        decision_id="decision-1",
        expected_outcome="resultado reproduzivel",
        observed_outcome="resultado reproduzivel",
        evidence_ids=("e-1",),
        source_ref="pr:382",
        source_commit="abc123",
        hypothesis="combinação governada melhora resultado",
        baseline="fluxo atual",
        experiment="comparação pareada",
        result="resultado validado",
        regression_status="PASS",
        generalization_status="CONFIRMED",
        risk="LOW",
        existing_owner=None,
        scope="tenant-a",
        tenant_scope="tenant-a",
        source_kind="pr",
    )
    values.update(overrides)
    return SymbiontLabObservation(**values)


def test_tenant_scope_mismatch_blocks_before_learning_capture():
    memory = MemoryStub()
    service = GovernedLearningService(memory)
    with pytest.raises(ValueError, match="tenant scope"):
        SymbiontLabAdapter(service).evaluate(
            make_observation(tenant_scope="tenant-b"),
            principal_id="principal-1",
            dataset_version="ds-1",
        )
    assert memory.calls == []


def test_unsupported_source_kind_blocks_before_learning_capture():
    memory = MemoryStub()
    service = GovernedLearningService(memory)
    with pytest.raises(ValueError, match="source kind"):
        SymbiontLabAdapter(service).evaluate(
            make_observation(source_kind="unknown-source"),
            principal_id="principal-1",
            dataset_version="ds-1",
        )
    assert memory.calls == []


def test_source_and_tenant_metadata_are_preserved_in_evolution_provenance():
    service = GovernedLearningService(MemoryStub())
    result = SymbiontLabAdapter(service).evaluate(
        make_observation(), principal_id="principal-1", dataset_version="ds-1"
    )
    assert result.state == "LAB_ONLY"
    assert result.observation.source_ref == "pr:382"
    assert result.observation.source_commit == "abc123"
    assert result.observation.tenant_scope == "tenant-a"
