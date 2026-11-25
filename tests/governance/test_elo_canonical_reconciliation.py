from pathlib import Path

from automation.tasks.elo_canonical_reconciliation import (
    CANONICAL_STRUCTURE_MAP,
    event_facts,
    reconcile_repository,
)
from automation.tasks.elo_maintenance_coordinator import Event, Outcome, audit


def test_no_changed_paths_is_waiting_for_evidence(tmp_path: Path):
    evidence = reconcile_repository(tmp_path, [])
    assert evidence.waiting_for_evidence
    facts = event_facts(evidence)
    assert facts["reuse_analysis_complete"] is False


def test_existing_equivalent_is_not_treated_as_create(tmp_path: Path):
    (tmp_path / "temporal_memory.py").write_text("class TemporalMemory: pass\n", encoding="utf-8")
    (tmp_path / "owner.md").write_text(
        "canonical owner: temporal_memory.py\nsource of truth: temporal_memory.py\n"
        "memory is the canonical temporal memory capability.\n",
        encoding="utf-8",
    )

    evidence = reconcile_repository(
        tmp_path,
        ["new_memory.py"],
        concept_terms=["memory"],
    )
    assert "temporal_memory.py" in evidence.candidates
    assert evidence.duplicate_or_parallel is True
    assert evidence.reuse_analysis_complete is True
    assert evidence.decision == "REUSE"


def test_candidate_without_duplicate_proof_remains_unknown(tmp_path: Path):
    (tmp_path / "temporal_memory.py").write_text("class TemporalMemory: pass\n", encoding="utf-8")
    (tmp_path / "references.md").write_text(
        "The existing temporal_memory capability may be related to the proposed memory change.\n",
        encoding="utf-8",
    )
    evidence = reconcile_repository(
        tmp_path,
        ["new_memory.py"],
        concept_terms=["memory"],
    )
    assert "temporal_memory.py" in evidence.candidates
    assert evidence.duplicate_or_parallel is None
    assert evidence.reuse_analysis_complete is False
    assert evidence.decision is None
    assert evidence.waiting_for_evidence


def test_unknown_owner_does_not_authorize_create(tmp_path: Path):
    (tmp_path / "unrelated.md").write_text("No canonical owner declared.\n", encoding="utf-8")
    evidence = reconcile_repository(tmp_path, ["new_capability.py"])
    assert evidence.reuse_analysis_complete is False
    assert evidence.decision is None
    assert evidence.waiting_for_evidence
    facts = event_facts(evidence)
    assert facts["canonical_target_resolved"] is False
    assert facts["reuse_analysis_complete"] is False


def test_unknown_duplicate_state_is_preserved(tmp_path: Path):
    (tmp_path / "owner.md").write_text(
        "canonical owner: new_capability.py\nsource of truth: new_capability.py\n",
        encoding="utf-8",
    )
    evidence = reconcile_repository(tmp_path, ["new_capability.py"])
    facts = event_facts(evidence)
    assert facts["duplicate_or_parallel_found"] is None
    assert facts["reuse_analysis_complete"] is False
    assert facts["contract_conflict"] is None


def test_reconciliation_blocks_parallel_memory_before_merge(tmp_path: Path):
    (tmp_path / "temporal_memory.py").write_text("class TemporalMemory: pass\n", encoding="utf-8")
    (tmp_path / "owner.md").write_text(
        "canonical owner: temporal_memory.py\nsource of truth: temporal_memory.py\n"
        "memory is the canonical temporal memory capability.\n",
        encoding="utf-8",
    )
    evidence = reconcile_repository(tmp_path, ["new_memory.py"], concept_terms=["memory"])
    facts = event_facts(evidence)
    event = Event(
        number=390,
        concept_id=facts["canonical_identity_valid"] and evidence.canonical_identity,
        event_class="memory",
        acceptance_pass=True,
        specialist_pass=True,
        ci_pass=True,
        reviews_clear=True,
        scope_compliant=True,
        forbidden_action=False,
        elo_approve_merge=True,
        evidence_complete=True,
        canonical_identity_valid=bool(facts["canonical_identity_valid"]),
        architectural_impact=True,
        experience_value=False,
        canonical_target_resolved=bool(facts["canonical_target_resolved"]),
        source_of_truth_resolved=bool(facts["source_of_truth_resolved"]),
        reuse_analysis_complete=bool(facts["reuse_analysis_complete"]),
        duplicate_or_parallel_found=facts["duplicate_or_parallel_found"],
        contract_conflict=facts["contract_conflict"],
    )
    outcome, reasons = audit(event)
    assert outcome is Outcome.BLOCKED
    assert "duplicate_or_parallel_capability_found" in reasons


def test_src_elo_uses_repository_canonical_map_as_runtime_ownership(tmp_path: Path):
    structure_map = tmp_path / CANONICAL_STRUCTURE_MAP
    structure_map.parent.mkdir(parents=True, exist_ok=True)
    structure_map.write_text(
        "# ELO Repository Canonical Structure Map\n\n"
        "`src/elo/` | Executable ELO | current implementation core | canonical executable root\n",
        encoding="utf-8",
    )

    evidence = reconcile_repository(
        tmp_path,
        ["src/elo/cognitive/agents/hermes_runtime.py"],
        concept_terms=["hermes_runtime"],
    )

    assert evidence.source_of_truth == CANONICAL_STRUCTURE_MAP
    assert evidence.canonical_identity == "src/elo"
    assert evidence.duplicate_or_parallel is False
    assert evidence.reuse_analysis_complete is True
    assert evidence.decision == "CREATE"
    assert not evidence.waiting_for_evidence


def test_src_elo_does_not_override_explicit_parallel_owner(tmp_path: Path):
    structure_map = tmp_path / CANONICAL_STRUCTURE_MAP
    structure_map.parent.mkdir(parents=True, exist_ok=True)
    structure_map.write_text(
        "# ELO Repository Canonical Structure Map\n\n"
        "`src/elo/` | Executable ELO | current implementation core | canonical executable root\n",
        encoding="utf-8",
    )
    (tmp_path / "parallel_runtime.py").write_text(
        "class ParallelRuntime: pass\n",
        encoding="utf-8",
    )
    (tmp_path / "owner.md").write_text(
        "canonical owner: parallel_runtime.py\n"
        "source of truth: parallel_runtime.py\n"
        "hermes_runtime capability is implemented here.\n",
        encoding="utf-8",
    )

    evidence = reconcile_repository(
        tmp_path,
        ["src/elo/cognitive/agents/hermes_runtime.py"],
        concept_terms=["hermes_runtime"],
    )

    assert evidence.duplicate_or_parallel is None
    assert evidence.reuse_analysis_complete is False
    assert evidence.decision is None
    assert evidence.waiting_for_evidence


def test_architecture_prose_does_not_create_false_explicit_owner(tmp_path: Path):
    """A generic canonical phrase must not become ownership evidence."""
    (tmp_path / "orchestrator.py").write_text(
        "class Orchestrator: pass\n",
        encoding="utf-8",
    )
    (tmp_path / "architecture.md").write_text(
        "The ELO Cognitivo is the canonical authority for orchestration.\n"
        "The orchestrator capability remains governed by existing architecture.\n",
        encoding="utf-8",
    )

    evidence = reconcile_repository(
        tmp_path,
        ["src/elo/agentic/context_assembly.py"],
        concept_terms=["orchestrator"],
    )

    assert "orchestrator.py" in evidence.candidates
    assert evidence.duplicate_or_parallel is None
    assert evidence.reuse_analysis_complete is False
    assert evidence.decision is None
    assert evidence.waiting_for_evidence


def test_generic_package_stem_does_not_create_false_parallel_owner(tmp_path: Path):
    """A generic package.json stem must not match unrelated canonical owners."""
    (tmp_path / "legacy_runtime.py").write_text(
        "# package metadata only; not related to the proposed sandbox runtime\n"
        "class LegacyRuntime: pass\n",
        encoding="utf-8",
    )
    (tmp_path / "owner.md").write_text(
        "canonical owner: legacy_runtime.py\n"
        "source of truth: legacy_runtime.py\n"
        "package metadata is maintained here.\n",
        encoding="utf-8",
    )

    evidence = reconcile_repository(
        tmp_path,
        ["apps/elo-web/package.json", "apps/elo-web/src/lib/elo-hermes-sandbox.ts"],
        concept_terms=["package", "elo_hermes_sandbox"],
    )

    assert evidence.duplicate_or_parallel is None
    assert evidence.reuse_analysis_complete is False
    assert evidence.decision is None
    assert "legacy_runtime.py" not in evidence.candidates



def _live_reconciliation_fixture(root: Path) -> None:
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI, LIVE_RECONCILIATION_CONTRACT,
        LIVE_RECONCILIATION_RUNTIME, LIVE_RECONCILIATION_WORKFLOW,
    )
    samples = {
        CANONICAL_STRUCTURE_MAP: (
            "| `src/elo/` | Executable ELO | current implementation core"
            " | canonical executable root |\n"
        ),
        LIVE_RECONCILIATION_CONTRACT: (
            "---\nartifact_id: ELO-LIVE-STATE-RECONCILIATION-CONTRACT\n"
            "family: docs/governance\nlayer: governance\n"
            "type: contract\nowner: ELO Governance\n"
            "authority: reference\nstatus: defined\n---\n"
        ),
        LIVE_RECONCILIATION_RUNTIME: (
            "class LiveStateReconciliation:\n"
            "    def reconcile(self, reader):\n        return reader\n"
            "def run_reconciliation_cli():\n    return 0\n"
        ),
        LIVE_RECONCILIATION_CLI: Path(LIVE_RECONCILIATION_CLI).read_text(encoding="utf-8"),
        LIVE_RECONCILIATION_WORKFLOW: Path(LIVE_RECONCILIATION_WORKFLOW).read_text(encoding="utf-8"),
    }
    for name, value in samples.items():
        p = root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value, encoding="utf-8")


def _live_evidence(root: Path, changed: list[str] | None = None):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    return reconcile_repository(root, changed or [LIVE_RECONCILIATION_CLI])


def test_canonical_live_owner_reuses_existing_contract_and_runtime(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI, LIVE_RECONCILIATION_RUNTIME,
        LIVE_RECONCILIATION_WORKFLOW, LIVE_RECONCILIATION_CONTRACT,
        _verified_live_reconciliation_owner,
    )
    _live_reconciliation_fixture(tmp_path)
    assert _verified_live_reconciliation_owner(Path("."), {LIVE_RECONCILIATION_CLI})
    changed = [LIVE_RECONCILIATION_RUNTIME, LIVE_RECONCILIATION_CLI,
               LIVE_RECONCILIATION_WORKFLOW,
               "automation/tasks/elo_canonical_reconciliation.py",
               "tests/governance/test_elo_canonical_reconciliation.py",
               "tests/infrastructure/test_live_reconciliation_workflow.py"]
    proof = _live_evidence(tmp_path, changed)
    assert proof.source_of_truth == LIVE_RECONCILIATION_RUNTIME
    assert LIVE_RECONCILIATION_CONTRACT in proof.owners
    assert proof.canonical_identity == "elo-live-state-reconciliation"
    assert proof.decision == "STRENGTHEN"
    assert proof.duplicate_or_parallel is False


def test_live_owner_fails_closed_for_missing_or_impostor_contract(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CONTRACT
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CONTRACT
    original = path.read_text(encoding="utf-8")
    path.write_text(original.replace("owner: ELO Governance", "owner: impostor"), encoding="utf-8")
    assert _live_evidence(tmp_path).waiting_for_evidence
    path.unlink()
    assert _live_evidence(tmp_path).waiting_for_evidence


def test_live_owner_rejects_parallel_candidate_and_missing_runtime(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_RUNTIME
    _live_reconciliation_fixture(tmp_path)
    candidate = tmp_path / "legacy/run_live_reconciliation.py"
    candidate.parent.mkdir()
    candidate.write_text("def run_live_reconciliation(): pass\n", encoding="utf-8")
    evidence = _live_evidence(tmp_path)
    assert "legacy/run_live_reconciliation.py" in evidence.candidates
    assert evidence.waiting_for_evidence
    candidate.unlink()
    runtime = tmp_path / LIVE_RECONCILIATION_RUNTIME
    runtime.write_text("class LiveStateReconciliation:\n    pass\n", encoding="utf-8")
    assert _live_evidence(tmp_path).waiting_for_evidence


def test_live_owner_rejects_unknown_file_outside_canonical_scope(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    assert _live_evidence(tmp_path, [LIVE_RECONCILIATION_CLI, "shadow/executor.py"]).waiting_for_evidence


def test_entire_cli_bootstrap_is_guarded_not_just_main_function(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    original = path.read_text(encoding="utf-8")
    cases = [
        original.replace("sys.exit(main())", "sys.exit(0)\n    sys.exit(main())"),
        original.replace("if __name__ == \"__main__\":", "sys.exit(0)\nif __name__ == \"__main__\":"),
        original.replace("run_reconciliation_cli as main", "run_reconciliation_cli as other"),
        original.replace("from pathlib import Path", "from pathlib import Path\nimport os"),
        original.replace("sys.path.insert(0, str(ROOT / \"src\"))",
                         "sys.path.insert(0, str(ROOT / \"src\"))\nsys.exit(0)"),
        original.replace("if __name__ == \"__main__\":",
                         "def main(unused=(print('PASS'), sys.exit(0))):\n    return 0\n"
                         "if __name__ == \"__main__\":"),
        original.replace("sys.exit(main())", "print('PASS')"),
        original + "\nif __name__ == '__main__':\n    sys.exit(0)\n",
    ]
    for case in cases:
        assert case != original
        path.write_text(case, encoding="utf-8")
        evidence = _live_evidence(tmp_path)
        assert evidence.waiting_for_evidence
        assert evidence.decision is None
    path.write_text(original, encoding="utf-8")
    assert _live_evidence(tmp_path).decision == "STRENGTHEN"


def test_workflow_must_execute_canonical_step_not_only_mention_it(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_WORKFLOW
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_WORKFLOW
    original = path.read_text(encoding="utf-8")
    cases = [
        original.replace("  reconcile:\n", "  reconcile:\n    if: ${{ false }}\n"),
        original.replace("      - name: Run reconciliation\n",
                         "      - name: Run reconciliation\n        if: false\n"),
        original.replace("python scripts/run_live_reconciliation.py",
                         "echo python scripts/run_live_reconciliation.py"),
        original.replace("          set -o pipefail\n", ""),
        original.replace("      - name: Run reconciliation\n",
                         "      - name: Unrelated action\n"),
        original.replace("      - name: Run reconciliation\n",
                         "      - name: Run reconciliation\n        continue-on-error: true\n"),
    ]
    for case in cases:
        assert case != original
        path.write_text(case, encoding="utf-8")
        assert _live_evidence(tmp_path).waiting_for_evidence
    path.write_text(original, encoding="utf-8")
    assert _live_evidence(tmp_path).decision == "STRENGTHEN"


def test_known_rls_expected_state_is_not_a_parallel_executable(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI, LIVE_RECONCILIATION_RUNTIME,
        LIVE_RECONCILIATION_EXPECTED_STATE, LIVE_RECONCILIATION_WORKFLOW,
    )
    _live_reconciliation_fixture(tmp_path)
    config = tmp_path / LIVE_RECONCILIATION_EXPECTED_STATE
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(
        Path(LIVE_RECONCILIATION_EXPECTED_STATE).read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    changed = [LIVE_RECONCILIATION_RUNTIME, LIVE_RECONCILIATION_CLI,
               LIVE_RECONCILIATION_WORKFLOW,
               "automation/tasks/elo_canonical_reconciliation.py",
               "tests/governance/test_elo_canonical_reconciliation.py",
               "tests/infrastructure/test_live_reconciliation_workflow.py"]
    terms = [Path(path).stem.replace("-", "_").lower() for path in changed]
    proof = reconcile_repository(tmp_path, changed, terms)
    assert proof.candidates == (LIVE_RECONCILIATION_EXPECTED_STATE,)
    assert proof.canonical_identity == "elo-live-state-reconciliation"
    assert proof.decision == "STRENGTHEN"
    assert not proof.waiting_for_evidence

    # A second executable candidate is never hidden by the config exception.
    competing = tmp_path / "legacy" / "run_live_reconciliation.py"
    competing.parent.mkdir()
    competing.write_text("def run_live_reconciliation(): pass\n", encoding="utf-8")
    blocked = reconcile_repository(tmp_path, changed, terms)
    assert blocked.waiting_for_evidence
    assert blocked.decision is None
