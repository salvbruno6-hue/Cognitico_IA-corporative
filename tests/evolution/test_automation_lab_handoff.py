from elo.cognitive.automation_execution_contract import AutomationEvidence, ExecutionResult, ExecutionStatus
from elo.cognitive.automation_lab_handoff import prepare_automation_lab_handoff


def test_completed_execution_reenters_canonical_lab():
    execution = ExecutionResult(
        execution_id="exe-1", automation_id="automation-1",
        status=ExecutionStatus.COMPLETED, result_ref="runtime://exe-1",
        evidence_ids=("ev-1",), started_at="2026-09-23T00:00:00Z",
        finished_at="2026-09-23T00:01:00Z",
    )
    evidence = (AutomationEvidence(
        evidence_id="ev-1", execution_id="exe-1",
        source_ref="runtime://exe-1", source_kind="runtime",
        observed_at="2026-09-23T00:01:00Z", summary="explicit result",
    ),)
    handoff = prepare_automation_lab_handoff(
        execution, evidence,
        tenant_id="tenant-1", decision_id="decision-1", observation_id="obs-1",
        source_commit="commit-1", hypothesis="bounded improvement",
        baseline="FPY=0.70", experiment="controlled test", result="FPY=0.79",
        regression_status="NONE", generalization_status="PARTIAL", risk="LOW",
        scope="EVOLUÇÃO_DE_CAPACIDADES",
    )
    assert handoff.observation.decision_id == "decision-1"
    assert handoff.observation.evidence_ids == ("ev-1",)


def test_failed_execution_cannot_enter_lab():
    execution = ExecutionResult(
        execution_id="exe-2", automation_id="automation-1",
        status=ExecutionStatus.FAILED, result_ref="runtime://exe-2",
        evidence_ids=("ev-2",), started_at=None, finished_at=None,
    )
    evidence = (AutomationEvidence(
        evidence_id="ev-2", execution_id="exe-2",
        source_ref="runtime://exe-2", source_kind="runtime",
        observed_at="2026-09-23T00:01:00Z", summary="failure evidence",
    ),)
    try:
        prepare_automation_lab_handoff(
            execution, evidence,
            tenant_id="tenant-1", decision_id="decision-2", observation_id="obs-2",
            source_commit="commit-1", hypothesis="h", baseline="b",
            experiment="e", result="r", regression_status="FAIL",
            generalization_status="PARTIAL", risk="LOW", scope="test",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("failed execution must not enter laboratory")
