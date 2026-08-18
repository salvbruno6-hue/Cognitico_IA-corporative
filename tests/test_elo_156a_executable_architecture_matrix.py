from pathlib import Path

from elo.core.execution_boundary import (
    ExecutionRequest,
    ExecutionStatus,
    execute_governed,
)


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_canonical_layers_exist_without_parallel_authority_names():
    required = (
        "src/elo/cognitive",
        "src/elo/core",
        "src/elo/domain",
        "src/elo/infrastructure",
        "src/elo/integrations",
        "forge",
    )
    for path in required:
        assert (ROOT / path).is_dir(), path

    source_paths = [p for p in (ROOT / "src/elo").rglob("*.py")]
    source_text = "\n".join(p.read_text(encoding="utf-8") for p in source_paths)
    forbidden_parallel_authorities = (
        "class SecondCore",
        "class ParallelCore",
        "class DuplicateScenarioEngine",
        "class ParallelExecutionAuthority",
    )
    assert not any(token in source_text for token in forbidden_parallel_authorities)


def test_critical_matrix_preserves_evidence_vocabulary_and_non_promotion_rule():
    matrix = _read("docs/testing/ELO_CRITICAL_ARCHITECTURAL_MATRIX_2026-08-18.md")
    for status in ("PASS", "FAIL", "UNKNOWN", "BLOCKED", "DEFINED"):
        assert f"`{status}`" in matrix
    assert "A criterion is `PASS` only when executable/reproducible evidence is tied to a commit/run." in matrix
    assert "No conversion of `DEFINED`, `UNKNOWN` or `BLOCKED` into `PASS` without reproducible evidence." in matrix
    assert "BASELINE v1.0 = NOT DECLARED" in matrix


def test_baseline_evidence_record_preserves_reproducibility_contract():
    record = _read("docs/governance/ELO_BASELINE_EVIDENCE_RECORD_2026-08-18.md")
    required = (
        "commit SHA",
        "workflow/run identifier",
        "executed test scope",
        "environment/runtime",
        "PASS/FAIL/UNKNOWN/BLOCKED/DEFINED",
        "known limitations",
        "decision or next action",
    )
    for item in required:
        assert item in record
    assert "No documentation-only status may be promoted to PASS." in record
    assert "BASELINE v1.0: NOT DECLARED" in record


def test_governed_execution_blocks_before_adapter_call_when_controls_are_missing():
    called = False

    class Adapter:
        def execute(self, _request):
            nonlocal called
            called = True
            return {"result": "must-not-run"}

    request = ExecutionRequest(
        request_id="req-156a",
        tenant_id="tenant-a",
        principal_id="principal-a",
        action_id="action-a",
        authorization_id=None,
        evidence_ids=(),
        correlation_id=None,
    )
    outcome = execute_governed(request, Adapter())
    assert outcome.status == ExecutionStatus.BLOCKED
    assert outcome.executed is False
    assert called is False
    assert "authorization_id" in outcome.reason
    assert "evidence_ids" in outcome.reason


def test_governed_execution_preserves_identity_and_correlation_after_authorization():
    class Adapter:
        def execute(self, _request):
            return {"provider": "fixture", "operation": "validated"}

    request = ExecutionRequest(
        request_id="req-156a",
        tenant_id="tenant-a",
        principal_id="principal-a",
        action_id="action-a",
        authorization_id="auth-a",
        evidence_ids=("evidence-a",),
        correlation_id="corr-a",
    )
    outcome = execute_governed(request, Adapter())
    assert outcome.status == ExecutionStatus.EXECUTED
    assert outcome.executed is True
    assert outcome.provenance["tenant_id"] == "tenant-a"
    assert outcome.provenance["principal_id"] == "principal-a"
    assert outcome.provenance["authorization_id"] == "auth-a"
    assert outcome.provenance["correlation_id"] == "corr-a"


def test_existing_adversarial_suite_is_part_of_the_executable_evidence_surface():
    adversarial = ROOT / "tests/test_elo_203_211_adversarial_closure.py"
    assert adversarial.exists()
    text = adversarial.read_text(encoding="utf-8")
    for marker in (
        "unauthorized_execution",
        "provider_failure",
        "scenario_gate",
        "conflicting_evidence",
    ):
        assert marker in text


def test_mt001_follow_up_remains_external_and_historical_record_is_protected():
    issue_registry = _read("docs/governance/ELO_ISSUE_REGISTRY_CURRENT_STATE.md")
    specialist_issue = _read("docs/governance/ELO_BASELINE_EVIDENCE_RECORD_2026-08-18.md")
    assert "#137" in issue_registry
    assert "BLOCKED ON EXTERNAL INPUT" in specialist_issue
    assert "No fabricated specialist evidence." in specialist_issue


def test_matrix_does_not_mark_known_operational_gaps_as_pass():
    matrix = _read("docs/testing/ELO_CRITICAL_ARCHITECTURAL_MATRIX_2026-08-18.md")
    expected_non_pass = {
        "BND-04": "DEFINED",
        "RUN-01": "DEFINED",
        "RUN-06": "DEFINED",
        "SPC-01": "DEFINED",
        "SPC-03": "DEFINED",
        "EVO-03": "DEFINED",
        "OPS-01": "DEFINED",
        "OPS-02": "DEFINED",
        "OPS-03": "BLOCKED",
    }
    rows = {line.split("|")[1].strip(): line for line in matrix.splitlines() if line.startswith("|")}
    for criterion, status in expected_non_pass.items():
        assert criterion in rows
        assert f"| {status} |" in rows[criterion]
