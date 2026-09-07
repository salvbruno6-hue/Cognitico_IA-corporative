import pytest

from elo.core.learning_governance import GovernedLearningService
from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabObservation


class MemoryStub:
    def remember(self, **kwargs):
        return None


def observation(**overrides):
    values = dict(
        observation_id="obs-1",
        tenant_id="tenant-a",
        domain="ORCAMENTO",
        decision_id="decision-1",
        expected_outcome="budget reproduced",
        observed_outcome="budget reproduced",
        evidence_ids=("e-1",),
        source_ref="pr:382",
        source_commit="abc123",
        hypothesis="governed specialist/model/tool combination improves quality",
        baseline="existing budget flow",
        experiment="paired execution against baseline",
        result="improved evidence completeness",
        regression_status="PASS",
        generalization_status="PARTIAL",
        risk="LOW",
        existing_owner="existing budget capability",
        scope="tenant-a budget experiments",
    )
    values.update(overrides)
    return SymbiontLabObservation(**values)


def test_adapter_records_experience_and_stays_lab_only():
    service = GovernedLearningService(MemoryStub())
    result = SymbiontLabAdapter(service).evaluate(
        observation(), principal_id="principal-1", dataset_version="ds-1"
    )
    assert result.state == "LAB_ONLY"
    assert result.experience.tenant_id == "tenant-a"
    assert result.candidate.experience_id == result.experience.experience_id
    assert result.evolution_classification == "DUPLICATE/SUPERSEDED"
    assert result.disposition == "REUSE"


def test_adapter_blocks_regression_before_recording_learning():
    service = GovernedLearningService(MemoryStub())
    with pytest.raises(ValueError, match="regression blocks"):
        SymbiontLabAdapter(service).evaluate(
            observation(regression_status="REGRESSION"),
            principal_id="principal-1",
            dataset_version="ds-1",
        )


def test_adapter_keeps_unconfirmed_generalization_lab_only():
    service = GovernedLearningService(MemoryStub())
    with pytest.raises(ValueError, match="unconfirmed generalization"):
        SymbiontLabAdapter(service).evaluate(
            observation(generalization_status="UNCONFIRMED", existing_owner=None),
            principal_id="principal-1",
            dataset_version="ds-1",
        )
