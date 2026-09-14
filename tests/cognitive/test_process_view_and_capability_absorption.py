import pytest

from elo.cognitive.capability_absorption import NativeCapabilityAbsorption
from elo.cognitive.process_view import (
    GovernedProcessView,
    ProcessViewRequest,
    ProcessViewResponse,
    ProcessViewState,
)
from elo.cognitive.symbionte_lab import SymbiontLabObservation


class Provider:
    def __init__(self, response):
        self.response = response

    def read(self, request):
        return self.response


def request():
    return ProcessViewRequest("tenant-a", "proc-1", "principal-1", scope="tenant-a")


def test_current_requires_evidence_and_source():
    response = ProcessViewResponse(
        "tenant-a", "proc-1", ProcessViewState.CURRENT, (), None, "10", "10", None
    )
    with pytest.raises(ValueError, match="evidence"):
        GovernedProcessView(Provider(response)).resolve(request())


def test_unknown_requires_gap_and_does_not_fabricate_telemetry():
    response = ProcessViewResponse(
        "tenant-a", "proc-1", ProcessViewState.UNKNOWN, (), None, None, None, "GAP:NO_GOVERNED_SOURCE"
    )
    assert GovernedProcessView(Provider(response)).resolve(request()).state == ProcessViewState.UNKNOWN


def test_deviation_requires_gap():
    response = ProcessViewResponse(
        "tenant-a", "proc-1", ProcessViewState.DEVIATION, ("ev-1",), "runtime://p1", "12", "10", "GAP:12!=10"
    )
    assert GovernedProcessView(Provider(response)).resolve(request()).gap == "GAP:12!=10"


def observation(**overrides):
    values = dict(
        observation_id="obs-1", tenant_id="tenant-a", domain="research", decision_id="d-1",
        expected_outcome="expected", observed_outcome="observed", evidence_ids=("ev-1",),
        source_ref="repo:hermes", source_commit="abc123", hypothesis="bounded retry with jitter",
        baseline="baseline-1", experiment="exp-1", result="pass", regression_status="PASS",
        generalization_status="CONFIRMED", risk="LOW", existing_owner=None, scope="tenant-a",
        tenant_scope="tenant-a", source_kind="repository",
    )
    values.update(overrides)
    return SymbiontLabObservation(**values)


def test_capability_absorption_preserves_lineage_and_stays_candidate_only():
    candidate = NativeCapabilityAbsorption().propose(observation())
    assert candidate.status == "CANDIDATE_ONLY"
    assert candidate.source_ref == "repo:hermes"
    assert candidate.source_commit == "abc123"
    assert candidate.evidence_ids == ("ev-1",)


def test_capability_absorption_blocks_without_regression_pass():
    with pytest.raises(ValueError, match="regression PASS"):
        NativeCapabilityAbsorption().propose(observation(regression_status="FAIL"))


def test_capability_absorption_blocks_unconfirmed_generalization():
    with pytest.raises(ValueError, match="confirmed generalization"):
        NativeCapabilityAbsorption().propose(observation(generalization_status="UNCONFIRMED"))
