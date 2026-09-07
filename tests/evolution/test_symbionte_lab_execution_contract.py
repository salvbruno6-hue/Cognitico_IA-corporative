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
        observation_id="obs-exec-1",
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
    )
    values.update(overrides)
    return SymbiontLabObservation(**values)


def test_confirmed_ownerless_candidate_reaches_compatible_classification():
    memory = MemoryStub()
    service = GovernedLearningService(memory)
    result = SymbiontLabAdapter(service).evaluate(
        make_observation(), principal_id="principal-1", dataset_version="ds-1"
    )
    assert result.state == "LAB_ONLY"
    assert result.evolution_classification == "COMPATIBLE"
    assert result.disposition == "CANDIDATE_FOR_GOVERNED_LEARNING"
    assert len(memory.calls) == 1


def test_high_risk_does_not_gain_promotion_eligibility():
    service = GovernedLearningService(MemoryStub())
    result = SymbiontLabAdapter(service).evaluate(
        make_observation(risk="HIGH"), principal_id="principal-1", dataset_version="ds-1"
    )
    assert result.state == "LAB_ONLY"
    assert result.evolution_classification == "ADAPT_REQUIRED"
    assert result.disposition == "STRENGTHEN"


def test_fail_is_blocked_before_experience_capture():
    memory = MemoryStub()
    service = GovernedLearningService(memory)
    with pytest.raises(ValueError, match="regression blocks"):
        SymbiontLabAdapter(service).evaluate(
            make_observation(regression_status="FAIL"),
            principal_id="principal-1",
            dataset_version="ds-1",
        )
    assert memory.calls == []


def test_critical_risk_is_blocked_before_experience_capture():
    memory = MemoryStub()
    service = GovernedLearningService(memory)
    with pytest.raises(ValueError, match="critical risk"):
        SymbiontLabAdapter(service).evaluate(
            make_observation(risk="CRITICAL"),
            principal_id="principal-1",
            dataset_version="ds-1",
        )
    assert memory.calls == []
