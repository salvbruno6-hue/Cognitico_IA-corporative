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
        observation_id="obs-order-1",
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


def test_evidence_gate_runs_before_learning_capture():
    memory = MemoryStub()
    service = GovernedLearningService(memory)
    with pytest.raises(ValueError, match="requires evidence"):
        SymbiontLabAdapter(service).evaluate(
            make_observation(evidence_ids=()),
            principal_id="principal-1",
            dataset_version="ds-1",
        )
    assert memory.calls == []


def test_unknown_generalization_runs_before_learning_capture():
    memory = MemoryStub()
    service = GovernedLearningService(memory)
    with pytest.raises(ValueError, match="unconfirmed generalization"):
        SymbiontLabAdapter(service).evaluate(
            make_observation(generalization_status="UNCONFIRMED"),
            principal_id="principal-1",
            dataset_version="ds-1",
        )
    assert memory.calls == []


def test_existing_owner_is_reuse_not_new_capability_candidate():
    service = GovernedLearningService(MemoryStub())
    result = SymbiontLabAdapter(service).evaluate(
        make_observation(existing_owner="canonical-budget-capability"),
        principal_id="principal-1",
        dataset_version="ds-1",
    )
    assert result.evolution_classification == "DUPLICATE/SUPERSEDED"
    assert result.disposition == "REUSE"
    assert result.state == "LAB_ONLY"
