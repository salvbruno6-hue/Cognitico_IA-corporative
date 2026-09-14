import pytest

from src.elo.core.devops_operation import DevOpsOperationError, NativeDevOpsOperation


def provenance():
    return {"source_ref": "github://repo", "source_commit": "abc123"}


def test_valid_operation_requires_health_and_rollback():
    op = NativeDevOpsOperation()
    cycle = op.prepare(cycle_id="c1", tenant_id="t1", target="main", change_ref="sha",
                       evidence_ids=("e1",), provenance=provenance(), rollback_ref="rollback/sha")
    assert op.advance(cycle=cycle, health_passed=True, rollback_tested=True).state == "READY_FOR_GOVERNANCE"


def test_unhealthy_operation_requires_recovery():
    op = NativeDevOpsOperation()
    cycle = op.prepare(cycle_id="c1", tenant_id="t1", target="main", change_ref="sha",
                       evidence_ids=("e1",), provenance=provenance(), rollback_ref="rollback/sha")
    assert op.advance(cycle=cycle, health_passed=False, rollback_tested=True).state == "RECOVERY_REQUIRED"


def test_missing_evidence_blocks():
    with pytest.raises(DevOpsOperationError):
        NativeDevOpsOperation().prepare(cycle_id="c1", tenant_id="t1", target="main", change_ref="sha",
                                        evidence_ids=(), provenance=provenance(), rollback_ref="rollback/sha")
