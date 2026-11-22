"""PERF-01: scope work without creating a second evidence or gate authority.

This is a structural safety check: one targeted suite does not substitute for
full-suite validation elsewhere in the canonical CI architecture.
"""
from pathlib import Path
import yaml


WORKFLOWS = Path(".github/workflows")


def _workflow(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def _steps(name: str, job: str) -> list[dict]:
    return _workflow(name)["jobs"][job]["steps"]


def _run(name: str, job: str, step_name: str) -> str:
    matches = [step["run"] for step in _steps(name, job)
               if step.get("name") == step_name and "run" in step]
    assert len(matches) == 1, (name, step_name)
    return matches[0]


def test_full_suite_remains_in_two_independent_canonical_gates() -> None:
    pr1 = _run("elo-pr1-validation.yml", "test", "Run tests")
    evolution = _run("elo-evolution-gate.yml", "validation", "Run full test suite")
    assert "python -m pytest" in pr1
    assert "tests/" not in pr1
    assert "python -m pytest" in evolution
    assert "tests/" not in evolution


def test_behavioral_job_runs_only_explicit_relevant_tests_and_oauth() -> None:
    name = "elo-behavioral-validation.yml"
    job = "test"
    script = _run(name, job, "Run focused behavioral tests (full suite remains in PR1 and Evolution)")
    for path in (
        "tests/test_core_behavioral_baseline.py",
        "tests/test_next_behavioral_hardening.py",
        "tests/agentic/test_agentic_safety_and_context.py",
        "tests/agentic/test_graph_runtime_contract.py",
        "tests/agentic/test_orchestrator_contract.py",
    ):
        assert path in script
    assert "python -m pytest -ra --tb=short" in script
    assert "node --test apps/elo-web/tests/oauthFlow.test.mjs" in str(_steps(name, job))


def test_scoped_result_cannot_masquerade_as_full_suite_or_authorization() -> None:
    name = "elo-behavioral-validation.yml"
    script = _run(name, "test", "Record scoped evidence provenance")
    for token in (
        "elo.ci-observation.v1", "behavioral-focused", "git rev-parse HEAD",
        "pr_head_sha", "run_attempt", "gate_authority:false",
        "reusable_as_full_suite:false",
    ):
        assert token in script
    upload = [step for step in _steps(name, "test")
              if step.get("name") == "Upload test evidence"]
    assert len(upload) == 1
    assert upload[0]["with"]["name"] == "elo-behavioral-test-evidence"
    assert "pytest-scope.json" in upload[0]["with"]["path"]


def test_stale_pr_runs_cancel_without_cancelling_main_push_validation() -> None:
    """Cancel only superseded PR revisions; preserve required current SHA evidence."""
    for filename in ("elo-pr1-validation.yml", "elo-behavioral-validation.yml"):
        workflow = _workflow(filename)
        concurrency = workflow.get("concurrency")
        assert concurrency is not None, filename
        assert concurrency["group"] == (
            "${{ github.workflow }}-${{ github.event.pull_request.number || github.sha }}"
        )
        assert concurrency["cancel-in-progress"] == (
            "${{ github.event_name == 'pull_request' }}"
        )
        # Cancellations cannot promote results; PR1 still runs its full suite,
        # and Behavioral remains focused with provenance marked non-authoritative.
        assert "test" in workflow["jobs"]
