import pytest

from elo.core.productivity_execution import (
    NativeProductivityBoundary,
    ProductivityExecutionError,
    ProductivityOutcome,
)


def _workflow():
    return NativeProductivityBoundary().prepare(
        workflow_id="wf-1", tenant_id="tenant-a", execution_id="exec-1",
        steps=("collect", "report"), idempotency_key="tenant-a:wf-1:1",
        evidence_ids=("ev-plan",), provenance={"source_ref": "elo", "source_commit": "abc"},
    )


def test_productivity_success_requires_evidence_and_matches_execution():
    outcome = NativeProductivityBoundary().validate_outcome(
        _workflow(), ProductivityOutcome("exec-1", "SUCCESS", ("ev-result",), "report generated")
    )
    assert outcome.status == "SUCCESS"


def test_productivity_rejects_mismatched_execution():
    with pytest.raises(ProductivityExecutionError):
        NativeProductivityBoundary().validate_outcome(
            _workflow(), ProductivityOutcome("other", "SUCCESS", ("ev-result",), "report generated")
        )


def test_productivity_rejects_success_without_evidence():
    with pytest.raises(ProductivityExecutionError):
        NativeProductivityBoundary().validate_outcome(
            _workflow(), ProductivityOutcome("exec-1", "SUCCESS", (), "report generated")
        )
