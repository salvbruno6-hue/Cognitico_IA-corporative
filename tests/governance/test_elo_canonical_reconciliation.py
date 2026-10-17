from pathlib import Path

from automation.tasks.elo_canonical_reconciliation import (
    CANONICAL_APPLICATION_REGISTRY,
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


def _application_registry(tmp_path: Path, **overrides):
    import json
    registry = tmp_path / CANONICAL_APPLICATION_REGISTRY
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps({
        "rule": "ELO-VRC-001",
        "canonical_project": "elo-web",
        "canonical_path": "apps/elo-web",
        **overrides,
    }), encoding="utf-8")
    return registry


def test_registered_elo_web_reuses_existing_application_owner(tmp_path: Path):
    _application_registry(tmp_path)
    evidence = reconcile_repository(tmp_path, [
        "apps/elo-web/src/components/elo-dashboard.tsx",
        "apps/elo-web/tests/workspace.test.mjs",
        "docs/evolution/workspace.md",
    ])
    assert evidence.source_of_truth == CANONICAL_APPLICATION_REGISTRY
    assert evidence.canonical_identity == "apps/elo-web"
    assert evidence.duplicate_or_parallel is False
    assert evidence.decision == "REUSE"
    assert not evidence.waiting_for_evidence


def test_application_cannot_supply_its_own_ownership_registry(tmp_path: Path):
    _application_registry(tmp_path)
    evidence = reconcile_repository(tmp_path, [
        "apps/elo-web/src/components/elo-dashboard.tsx",
        CANONICAL_APPLICATION_REGISTRY,
    ])
    assert evidence.waiting_for_evidence


def test_application_registry_does_not_admit_mixed_core_or_backend(tmp_path: Path):
    _application_registry(tmp_path)
    for outside in ("src/elo/new_core.py", "supabase/functions/new-reader/index.ts", "apps/other/page.tsx"):
        evidence = reconcile_repository(tmp_path, ["apps/elo-web/src/new.ts", outside])
        assert evidence.waiting_for_evidence


def test_application_registry_does_not_override_explicit_parallel_owner(tmp_path: Path):
    _application_registry(tmp_path)
    (tmp_path / "second_workspace.ts").write_text("export const workspace = {};\n", encoding="utf-8")
    (tmp_path / "owner.md").write_text(
        "canonical owner: second_workspace.ts\nsource of truth: second_workspace.ts\n",
        encoding="utf-8",
    )
    evidence = reconcile_repository(tmp_path, ["apps/elo-web/src/workspace.ts"], ["workspace"])
    assert evidence.duplicate_or_parallel is True
    assert evidence.source_of_truth == "owner.md"


def test_application_registry_missing_malformed_or_unrecognized_fails_closed(tmp_path: Path):
    changed = ["apps/elo-web/src/workspace.ts"]
    assert reconcile_repository(tmp_path, changed).waiting_for_evidence
    registry = _application_registry(tmp_path)
    for text in ("invalid", "[]", '{}'):
        registry.write_text(text, encoding="utf-8")
        assert reconcile_repository(tmp_path, changed).waiting_for_evidence
    for override in ({"canonical_path": "apps/other"}, {"rule": "unknown"}, {"canonical_project": "second-app"}):
        _application_registry(tmp_path, **override)
        assert reconcile_repository(tmp_path, changed).waiting_for_evidence


def test_registry_prevents_deprecated_frontend_ownership_fallback(tmp_path: Path):
    _application_registry(tmp_path)
    (tmp_path / "owner.md").write_text("canonical owner: frontend\n", encoding="utf-8")
    assert reconcile_repository(tmp_path, ["frontend/src/workspace.ts"], ["frontend"]).waiting_for_evidence


def test_application_does_not_clear_an_unclassified_executable(tmp_path: Path):
    _application_registry(tmp_path)
    (tmp_path / "other_workspace.ts").write_text("export const workspace = {};\n", encoding="utf-8")
    evidence = reconcile_repository(tmp_path, ["apps/elo-web/src/workspace.ts"], ["workspace"])
    assert "other_workspace.ts" in evidence.candidates
    assert evidence.waiting_for_evidence


def test_application_candidates_require_existing_core_and_deprecation_evidence(tmp_path: Path):
    _application_registry(tmp_path)
    for directory in ("frontend", "src/elo"):
        path = tmp_path / directory / "workspace.ts"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("export const workspace = {};\n", encoding="utf-8")
    changed = ["apps/elo-web/src/workspace.ts"]
    assert reconcile_repository(tmp_path, changed, ["workspace"]).waiting_for_evidence
    _application_registry(tmp_path, deprecated_noncanonical_projects=[{
        "path": "frontend", "status": "DEPRECATED", "replacement": "apps/elo-web",
    }])
    assert reconcile_repository(tmp_path, changed, ["workspace"]).waiting_for_evidence
    structure_map = tmp_path / CANONICAL_STRUCTURE_MAP
    structure_map.parent.mkdir(parents=True, exist_ok=True)
    structure_map.write_text("`src/elo/` | Executable ELO | canonical executable root\n", encoding="utf-8")
    assert not reconcile_repository(tmp_path, changed, ["workspace"]).waiting_for_evidence
    assert reconcile_repository(tmp_path, changed + [CANONICAL_STRUCTURE_MAP], ["workspace"]).waiting_for_evidence
