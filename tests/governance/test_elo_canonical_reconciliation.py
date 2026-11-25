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



def _live_reconciliation_fixture(tmp_path: Path) -> None:
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_CONTRACT,
        LIVE_RECONCILIATION_RUNTIME,
        LIVE_RECONCILIATION_WORKFLOW,
    )

    samples = {
        CANONICAL_STRUCTURE_MAP: (
            "| `src/elo/` | Executable ELO | current implementation core"
            " | canonical executable root |\n"
        ),
        LIVE_RECONCILIATION_CONTRACT: (
            "---\n"
            "artifact_id: ELO-LIVE-STATE-RECONCILIATION-CONTRACT\n"
            "family: docs/governance\nlayer: governance\n"
            "type: contract\nowner: ELO Governance\n"
            "authority: reference\nstatus: defined\n---\n"
        ),
        LIVE_RECONCILIATION_RUNTIME: (
            "class LiveStateReconciliation:\n"
            "    def reconcile(self, reader):\n"
            "        return reader\n"
        ),
        LIVE_RECONCILIATION_CLI: (
            "\"\"\"Canonical runner fixture.\"\"\"\n"
            "from __future__ import annotations\n"
            "import json\nimport os\nimport sys\n"
            "from pathlib import Path\n"
            "ROOT = Path(__file__).resolve().parent.parent\n"
            "sys.path.insert(0, str(ROOT / 'src'))\n"
            "def result_exit_code(overall):\n"
            "    return 0 if overall == 'PASS' else 3\n"
            "def main():\n"
            "    url = os.environ.get('SUPABASE_URL', '').strip()\n"
            "    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '').strip()\n"
            "    if not url or not key:\n"
            "        print('missing credentials', file=sys.stderr)\n"
            "        return 1\n"
            "    from elo.infrastructure.live_state_reconciliation import LiveStateReconciliation\n"
            "    from elo.infrastructure.supabase_rls_reader import SupabaseRLSStateReader\n"
            "    reader = SupabaseRLSStateReader(url, key)\n"
            "    harness = LiveStateReconciliation()\n"
            "    try:\n"
            "        report = harness.reconcile(reader)\n"
            "    except Exception:\n"
            "        return 2\n"
            "    output = report.to_dict()\n"
            "    print(json.dumps(output, indent=2, ensure_ascii=False))\n"
            "    return result_exit_code(output.get('overall'))\n"
            "if __name__ == '__main__':\n"
            "    sys.exit(main())\n"
        ),
        LIVE_RECONCILIATION_WORKFLOW: (
            "name: ELO Live Reconciliation\n"
            "jobs:\n"
            "  reconcile:\n"
            "    steps:\n"
            "      - name: Run reconciliation\n"
            "        id: reconcile\n"
            "        run: |\n"
            "          set -o pipefail\n"
            "          python scripts/run_live_reconciliation.py \\\n"
            "            | tee reconciliation_report.json\n"
            "      - name: Show report\n"
        ),
    }
    for name, content in samples.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def test_live_reconciliation_existing_owner_is_proven(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_WORKFLOW,
        LIVE_RECONCILIATION_RUNTIME,
        LIVE_RECONCILIATION_CONTRACT,
    )
    _live_reconciliation_fixture(tmp_path)
    evidence = reconcile_repository(tmp_path, [
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_WORKFLOW,
        "tests/infrastructure/test_live_reconciliation_workflow.py",
        "automation/tasks/elo_canonical_reconciliation.py",
        "tests/governance/test_elo_canonical_reconciliation.py",
    ])
    assert evidence.source_of_truth == LIVE_RECONCILIATION_RUNTIME
    assert LIVE_RECONCILIATION_CONTRACT in evidence.owners
    assert evidence.canonical_identity == "elo-live-state-reconciliation"
    assert evidence.duplicate_or_parallel is False
    assert evidence.reuse_analysis_complete is True
    assert evidence.decision == "STRENGTHEN"


def test_live_reconciliation_missing_contract_stays_unknown(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_CONTRACT,
    )
    _live_reconciliation_fixture(tmp_path)
    (tmp_path / LIVE_RECONCILIATION_CONTRACT).unlink()
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_live_reconciliation_unrelated_file_is_not_approved(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    evidence = reconcile_repository(tmp_path, [
        LIVE_RECONCILIATION_CLI,
        "src/other/shadow_reconciler.py",
    ])
    # Generic src/elo fallback is unavailable; unrelated additions are not approved.
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_live_reconciliation_owner_claim_is_not_enough(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_CONTRACT,
    )
    _live_reconciliation_fixture(tmp_path)
    (tmp_path / LIVE_RECONCILIATION_CONTRACT).write_text(
        "owner: newly-invented-authority\\n", encoding="utf-8"
    )
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence


def test_live_reconciliation_parallel_candidate_is_not_auto_cleared(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    candidate = tmp_path / "legacy" / "run_live_reconciliation.py"
    candidate.parent.mkdir(parents=True)
    candidate.write_text("def run_live_reconciliation(): pass\\n", encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert "legacy/run_live_reconciliation.py" in evidence.candidates
    assert evidence.waiting_for_evidence


def test_live_reconciliation_real_files_are_wired():
    """Use the actual repo contract, CLI, runtime and workflow together."""
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        _verified_live_reconciliation_owner,
    )
    assert _verified_live_reconciliation_owner(
        Path("."), {LIVE_RECONCILIATION_CLI}
    )


def test_commented_import_does_not_prove_live_reconciliation(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    (tmp_path / LIVE_RECONCILIATION_CLI).write_text(
        "# from elo.infrastructure.live_state_reconciliation import LiveStateReconciliation\n"
        "def main():\n    print('PASS')\n    return 0\n",
        encoding="utf-8",
    )
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_real_import_but_disconnected_execution_fails(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    (tmp_path / LIVE_RECONCILIATION_CLI).write_text(
        "from elo.infrastructure.live_state_reconciliation import LiveStateReconciliation\n"
        "def main():\n    print('PASS')\n    return 0\n",
        encoding="utf-8",
    )
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence


def test_impostor_owner_metadata_fails(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_CONTRACT,
    )
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CONTRACT
    path.write_text(path.read_text().replace(
        "owner: ELO Governance",
        "# owner: ELO Governance Impostor",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence


def test_workflow_echo_is_not_executable_wiring(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_WORKFLOW,
    )
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_WORKFLOW
    path.write_text(path.read_text().replace(
        "python scripts/run_live_reconciliation.py",
        "echo python scripts/run_live_reconciliation.py",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence


def test_missing_canonical_runtime_method_stays_unknown(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_RUNTIME,
    )
    _live_reconciliation_fixture(tmp_path)
    (tmp_path / LIVE_RECONCILIATION_RUNTIME).write_text(
        "class LiveStateReconciliation:\n    pass\n", encoding="utf-8"
    )
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence


def test_false_pass_exit_code_is_not_certified(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text().replace(
        "return 0 if overall == 'PASS' else 3",
        "return 0",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence


def test_unreachable_import_and_fake_pass_do_not_prove_owner(tmp_path: Path):
    """Imports and calls hidden under if False cannot certify execution."""
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    (tmp_path / LIVE_RECONCILIATION_CLI).write_text(
        "import sys\n"
        "def result_exit_code(overall):\n"
        "    return 0 if overall == 'PASS' else 3\n"
        "def main():\n"
        "    if False:\n"
        "        from elo.infrastructure.live_state_reconciliation import LiveStateReconciliation\n"
        "        from elo.infrastructure.supabase_rls_reader import SupabaseRLSStateReader\n"
        "        reader = SupabaseRLSStateReader(url, key)\n"
        "        harness = LiveStateReconciliation()\n"
        "        try:\n"
        "            report = harness.reconcile(reader)\n"
        "        except Exception:\n"
        "            return 2\n"
        "        output = report.to_dict()\n"
        "        return result_exit_code(output.get('overall'))\n"
        "    print('PASS')\n"
        "    return 0\n"
        "if __name__ == '__main__':\n"
        "    sys.exit(main())\n",
        encoding="utf-8",
    )
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_inert_yaml_example_cannot_claim_active_reconciliation(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_WORKFLOW,
    )
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_WORKFLOW
    # The expected step exists only as text in env.EXAMPLE, not a job.
    path.write_text(
        "name: ELO Live Reconciliation\n"
        "env:\n"
        "  EXAMPLE: |\n"
        "      - name: Run reconciliation\n"
        "        id: reconcile\n"
        "        run: |\n"
        "          set -o pipefail\n"
        "          python scripts/run_live_reconciliation.py \\\n"
        "            | tee reconciliation_report.json\n"
        "      - name: Show report\n"
        "jobs:\n"
        "  reconcile:\n"
        "    steps:\n"
        "      - name: Real step\n"
        "        run: echo PASS\n",
        encoding="utf-8",
    )
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_early_return_pass_before_reconcile_is_rejected(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text().replace(
        "def main():\n",
        "def main():\n    print('{\"overall\": \"PASS\"}')\n    return 0\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_entrypoint_cannot_exit_success_before_main(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text(encoding="utf-8").replace(
        "    sys.exit(main())\n",
        "    print('{\"overall\": \"PASS\"}')\n    sys.exit(0)\n"
        "    sys.exit(main())\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_duplicate_entrypoint_cannot_certify_owner(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text(encoding="utf-8") +
        "\nif __name__ == '__main__':\n    sys.exit(0)\n", encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence


def test_disabled_reconciliation_job_cannot_certify_owner(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_WORKFLOW,
    )
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_WORKFLOW
    path.write_text(path.read_text(encoding="utf-8").replace(
        "  reconcile:\n",
        "  reconcile:\n    if: ${{ false }}\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_disabled_run_step_cannot_certify_owner(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import (
        LIVE_RECONCILIATION_CLI,
        LIVE_RECONCILIATION_WORKFLOW,
    )
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_WORKFLOW
    path.write_text(path.read_text(encoding="utf-8").replace(
        "      - name: Run reconciliation\n",
        "      - name: Run reconciliation\n        if: false\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_module_level_early_exit_cannot_certify_owner(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text(encoding="utf-8").replace(
        "if __name__ == '__main__':\n",
        "print('{\"overall\": \"PASS\"}')\nsys.exit(0)\n"
        "if __name__ == '__main__':\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_credentials_guard_else_cannot_certify_owner(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text(encoding="utf-8").replace(
        "        return 1\n",
        "        return 1\n"
        "    else:\n"
        "        print('{\"overall\": \"PASS\"}')\n"
        "        return 0\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_exception_handler_early_success_cannot_certify_owner(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text(encoding="utf-8").replace(
        "    except Exception:\n"
        "        return 2\n",
        "    except Exception:\n"
        "        return 0\n"
        "        return 2\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence


def test_unreviewed_python_decorator_cannot_certify_owner(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text(encoding="utf-8").replace(
        "def main():\n",
        "@some_noncanonical_wrapper\n"
        "def main():\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence


def test_evaluated_default_argument_cannot_fake_pass(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text(encoding="utf-8").replace(
        "def main():\n",
        "def main(unused=(print('{\"overall\": \"PASS\"}'), sys.exit(0))):\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_credentials_guard_cannot_exit_zero_before_return_one(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text(encoding="utf-8").replace(
        "    if not url or not key:\n",
        "    if not url or not key:\n"
        "        print('{\"overall\": \"PASS\"}')\n"
        "        sys.exit(0)\n",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_error_print_cannot_call_exit_zero(tmp_path: Path):
    from automation.tasks.elo_canonical_reconciliation import LIVE_RECONCILIATION_CLI
    _live_reconciliation_fixture(tmp_path)
    path = tmp_path / LIVE_RECONCILIATION_CLI
    path.write_text(path.read_text(encoding="utf-8").replace(
        "print('missing credentials', file=sys.stderr)",
        "print(sys.exit(0), file=sys.stderr)",
    ), encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [LIVE_RECONCILIATION_CLI])
    assert evidence.waiting_for_evidence
