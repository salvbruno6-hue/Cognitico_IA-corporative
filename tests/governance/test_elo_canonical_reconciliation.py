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



def _make_existing_authz_owner(tmp_path: Path) -> None:
    """Fixture for the pre-existing single authorization issuer."""
    from automation.tasks.elo_canonical_reconciliation import (
        AUTHZ_CANONICAL_RUNTIME, AUTHZ_OWNER_CONTRACT,
    )
    runtime = tmp_path / AUTHZ_CANONICAL_RUNTIME
    runtime.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_text("async function resolveAuthorizationGrant() {}\n", encoding="utf-8")
    owner = tmp_path / AUTHZ_OWNER_CONTRACT
    owner.parent.mkdir(parents=True, exist_ok=True)
    owner.write_text(
        "# ELO Operator GitHub Binding Runtime\n"
        "elo-authz remains the sole issuer; issue_authorization_grant is governed.\n",
        encoding="utf-8",
    )
    structure = tmp_path / CANONICAL_STRUCTURE_MAP
    structure.parent.mkdir(parents=True, exist_ok=True)
    structure.write_text(
        "# ELO Repository Canonical Structure Map\n"
        "| supabase/functions/elo-authz/ | ELO Governance | "
        "owner contract docs/governance/ELO_OPERATOR_GITHUB_BINDING_RUNTIME.md | canonical |\n",
        encoding="utf-8",
    )


def test_authz_session_fix_reconciles_existing_owner(tmp_path: Path) -> None:
    _make_existing_authz_owner(tmp_path)
    evidence = reconcile_repository(tmp_path, [
        "supabase/functions/elo-authz/index.ts",
        "tests/security/test_operator_github_binding_runtime.py",
    ])
    assert evidence.canonical_identity == "elo-authz"
    assert evidence.source_of_truth == "docs/governance/ELO_OPERATOR_GITHUB_BINDING_RUNTIME.md"
    assert evidence.duplicate_or_parallel is False
    assert evidence.reuse_analysis_complete
    assert evidence.decision == "STRENGTHEN"


def test_authz_atomicity_fix_reconciles_same_owner(tmp_path: Path) -> None:
    _make_existing_authz_owner(tmp_path)
    evidence = reconcile_repository(tmp_path, [
        "supabase/functions/elo-authz/index.ts",
        "tests/security/test_operator_github_binding_runtime.py",
        "tests/security/test_elo_atomic_grant_issuance_contract.py",
        "tests/security/sql/elo_atomic_grant_integration.sql",
        "supabase/migrations/20261110185000_elo_atomic_grant_audit_rpc.sql",
        ".github/workflows/elo-authz-atomic-db-test.yml",
    ])
    assert evidence.canonical_identity == "elo-authz"
    assert evidence.source_of_truth == "docs/governance/ELO_OPERATOR_GITHUB_BINDING_RUNTIME.md"
    assert evidence.duplicate_or_parallel is False
    assert evidence.reuse_analysis_complete
    assert evidence.decision == "STRENGTHEN"


def test_authz_scope_does_not_infer_missing_contract(tmp_path: Path) -> None:
    _make_existing_authz_owner(tmp_path)
    (tmp_path / "docs/governance/ELO_OPERATOR_GITHUB_BINDING_RUNTIME.md").unlink()
    evidence = reconcile_repository(tmp_path, ["supabase/functions/elo-authz/index.ts"])
    assert evidence.waiting_for_evidence
    assert evidence.source_of_truth is None


def test_authz_scope_rejects_unlisted_migration(tmp_path: Path) -> None:
    _make_existing_authz_owner(tmp_path)
    evidence = reconcile_repository(tmp_path, [
        "supabase/functions/elo-authz/index.ts",
        "supabase/migrations/20261111120000_unreviewed_authz.sql",
    ])
    assert evidence.waiting_for_evidence
    assert evidence.source_of_truth is None


def test_authz_scope_rejects_unrelated_workflow(tmp_path: Path) -> None:
    _make_existing_authz_owner(tmp_path)
    evidence = reconcile_repository(tmp_path, [
        "supabase/functions/elo-authz/index.ts",
        ".github/workflows/elo-merge-coordinator.yml",
    ])
    assert evidence.waiting_for_evidence
    assert evidence.source_of_truth is None


def test_authz_scope_rejects_test_only_change(tmp_path: Path) -> None:
    _make_existing_authz_owner(tmp_path)
    evidence = reconcile_repository(tmp_path, [
        "tests/security/test_operator_github_binding_runtime.py",
    ])
    assert evidence.waiting_for_evidence


def test_authz_scope_rejects_unknown_owner_map(tmp_path: Path) -> None:
    _make_existing_authz_owner(tmp_path)
    (tmp_path / CANONICAL_STRUCTURE_MAP).write_text(
        "# unrelated structure map\n", encoding="utf-8"
    )
    evidence = reconcile_repository(tmp_path, ["supabase/functions/elo-authz/index.ts"])
    assert evidence.waiting_for_evidence


def test_authz_scope_scans_executable_automation_for_parallel_issuers(tmp_path: Path) -> None:
    """An automation task can issue grants and cannot be excluded wholesale."""
    _make_existing_authz_owner(tmp_path)
    writer = tmp_path / "automation/tasks/parallel_authz.py"
    writer.parent.mkdir(parents=True, exist_ok=True)
    writer.write_text(
        'import requests\n'
        'requests.post("/rest/v1/elo_authorization_grants")\n',
        encoding="utf-8",
    )
    evidence = reconcile_repository(
        tmp_path, ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["index", "test_operator_github_binding_runtime"],
    )
    assert "automation/tasks/parallel_authz.py" in evidence.candidates
    assert evidence.waiting_for_evidence
    assert evidence.decision != "STRENGTHEN"


def test_authz_scope_allows_workflow_that_only_reads_grants(tmp_path: Path) -> None:
    """Read-only ELO workflow consumers must not become synthetic issuers."""
    _make_existing_authz_owner(tmp_path)
    workflow = tmp_path / ".github/workflows/elo-agent-loop.yml"
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(
        'steps:\n  - run: curl -fsS "$SUPABASE_URL/rest/v1/elo_authorization_grants?select=grant_id"\n',
        encoding="utf-8",
    )
    evidence = reconcile_repository(
        tmp_path, ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["index"],
    )
    assert evidence.decision == "STRENGTHEN", evidence.reasons
    assert evidence.duplicate_or_parallel is False


def test_authz_scope_rejects_grant_write_in_known_workflow(tmp_path: Path) -> None:
    """Even the canonical Agent Loop cannot secretly issue its own grants."""
    _make_existing_authz_owner(tmp_path)
    workflow = tmp_path / ".github/workflows/elo-agent-loop.yml"
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(
        'steps:\n  - run: curl -X POST "$SUPABASE_URL/rest/v1/elo_authorization_grants"\n',
        encoding="utf-8",
    )
    evidence = reconcile_repository(
        tmp_path, ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["index"],
    )
    assert ".github/workflows/elo-agent-loop.yml" in evidence.candidates
    assert evidence.waiting_for_evidence
    assert evidence.decision != "STRENGTHEN"


def test_authz_scope_scans_unreviewed_workflow_grant_writer(tmp_path: Path) -> None:
    """A workflow that writes authorization grants is not a read-only consumer."""
    _make_existing_authz_owner(tmp_path)
    writer = tmp_path / ".github/workflows/parallel-authz.yml"
    writer.parent.mkdir(parents=True, exist_ok=True)
    writer.write_text(
        'name: parallel-authz\n'
        'steps:\n'
        '  - run: curl -X POST /rest/v1/elo_authorization_grants\n',
        encoding="utf-8",
    )
    evidence = reconcile_repository(
        tmp_path, ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["index"],
    )
    assert ".github/workflows/parallel-authz.yml" in evidence.candidates
    assert evidence.waiting_for_evidence
    assert evidence.decision != "STRENGTHEN"


def test_authz_scope_finds_direct_rest_grant_writer_without_name_match(tmp_path: Path) -> None:
    """Actual Maintenance terms are filenames; they must not hide another issuer."""
    _make_existing_authz_owner(tmp_path)
    writer = tmp_path / "providers/parallel_authz.ts"
    writer.parent.mkdir(parents=True, exist_ok=True)
    writer.write_text(
        'export async function issue() { return fetch("/rest/v1/elo_authorization_grants", '
        '{method:"POST"}); }\n',
        encoding="utf-8",
    )
    evidence = reconcile_repository(
        tmp_path, ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["index", "test_operator_github_binding_runtime"],
    )
    assert "providers/parallel_authz.ts" in evidence.candidates
    assert evidence.waiting_for_evidence
    assert evidence.duplicate_or_parallel is None
    assert evidence.decision != "STRENGTHEN"
    assert event_facts(evidence)["contract_conflict"] is None


def test_authz_scope_finds_unreviewed_sql_grant_writer(tmp_path: Path) -> None:
    """A differently named SQL source cannot issue grants outside the owner."""
    _make_existing_authz_owner(tmp_path)
    writer = tmp_path / "sql/another_writer.sql"
    writer.parent.mkdir(parents=True, exist_ok=True)
    writer.write_text(
        "INSERT INTO public.elo_authorization_grants (grant_id) VALUES (gen_random_uuid());\n",
        encoding="utf-8",
    )
    evidence = reconcile_repository(
        tmp_path, ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["index"],
    )
    assert "sql/another_writer.sql" in evidence.candidates
    assert evidence.waiting_for_evidence
    assert evidence.decision is None


def test_authz_scope_rejects_unresolved_executable_candidate_without_owner(tmp_path: Path) -> None:
    """P2 regression: a candidate needs investigation even without owner claim."""
    _make_existing_authz_owner(tmp_path)
    (tmp_path / "parallel_authz.py").write_text(
        "elo_authz capability\n", encoding="utf-8"
    )
    evidence = reconcile_repository(
        tmp_path, ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["elo_authz"],
    )
    assert "parallel_authz.py" in evidence.candidates
    assert evidence.waiting_for_evidence
    assert evidence.duplicate_or_parallel is None
    assert evidence.decision != "STRENGTHEN"
    assert evidence.source_of_truth is None


def test_authz_scope_ignores_only_verified_existing_consumers(tmp_path: Path) -> None:
    """Proven MCP and data-gateway consumers are not duplicate grant issuers."""
    _make_existing_authz_owner(tmp_path)
    for name in ("elo-mcp", "elo-data-gateway"):
        candidate = tmp_path / f"supabase/functions/{name}/index.ts"
        candidate.parent.mkdir(parents=True, exist_ok=True)
        candidate.write_text(
            'const AUTHZ_URL="/functions/v1/elo-authz";\n'
            'export async function consult() { return fetch(AUTHZ_URL); }\n',
            encoding="utf-8",
        )
    evidence = reconcile_repository(
        tmp_path, ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["elo-authz"],
    )
    assert evidence.decision == "STRENGTHEN", evidence.reasons
    assert evidence.duplicate_or_parallel is False
    assert len(evidence.candidates) == 2


def test_authz_scope_blocks_consumer_that_starts_issuing_grants(tmp_path: Path) -> None:
    """A known consumer stops being exempt when it contains issuer behavior."""
    _make_existing_authz_owner(tmp_path)
    consumer = tmp_path / "supabase/functions/elo-mcp/index.ts"
    consumer.parent.mkdir(parents=True, exist_ok=True)
    consumer.write_text(
        'const AUTHZ_URL="/functions/v1/elo-authz";\n'
        'const issue_authorization_grant = true;\n',
        encoding="utf-8",
    )
    evidence = reconcile_repository(
        tmp_path, ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["elo-authz"],
    )
    assert "supabase/functions/elo-mcp/index.ts" in evidence.candidates
    assert evidence.waiting_for_evidence
    assert evidence.decision != "STRENGTHEN"


def test_authz_scope_does_not_override_competing_owner(tmp_path: Path) -> None:
    _make_existing_authz_owner(tmp_path)
    (tmp_path / "rogue_authz.py").write_text("elo_authz capability\n", encoding="utf-8")
    (tmp_path / "rogue_owner.md").write_text(
        "canonical owner: rogue_authz.py\n"
        "source of truth: rogue_authz.py\n"
        "elo_authz capability\n", encoding="utf-8",
    )
    evidence = reconcile_repository(
        tmp_path,
        ["supabase/functions/elo-authz/index.ts"],
        concept_terms=["elo_authz"],
    )
    assert evidence.decision != "STRENGTHEN"
    assert evidence.duplicate_or_parallel is not False


def test_maintenance_map_and_test_changes_share_existing_owner(tmp_path: Path) -> None:
    structure = tmp_path / CANONICAL_STRUCTURE_MAP
    structure.parent.mkdir(parents=True, exist_ok=True)
    structure.write_text("# ELO canonical map\n", encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [
        "automation/tasks/elo_canonical_reconciliation.py",
        CANONICAL_STRUCTURE_MAP,
        "tests/governance/test_elo_canonical_reconciliation.py",
    ])
    assert evidence.source_of_truth == CANONICAL_STRUCTURE_MAP
    assert evidence.reuse_analysis_complete
    assert evidence.duplicate_or_parallel is False


def test_maintenance_map_cannot_override_unrelated_runtime(tmp_path: Path) -> None:
    structure = tmp_path / CANONICAL_STRUCTURE_MAP
    structure.parent.mkdir(parents=True, exist_ok=True)
    structure.write_text("# ELO canonical map\n", encoding="utf-8")
    evidence = reconcile_repository(tmp_path, [
        "automation/tasks/elo_canonical_reconciliation.py",
        CANONICAL_STRUCTURE_MAP,
        "supabase/functions/unrelated/index.ts",
    ])
    assert evidence.waiting_for_evidence



def test_authz_owner_reconciles_real_pr1171_paths_in_repository() -> None:
    """Integration: work on the full canonical tree, not a synthetic fixture."""
    root = Path(__file__).resolve().parents[2]
    evidence = reconcile_repository(root, [
        "supabase/functions/elo-authz/index.ts",
        "tests/security/test_operator_github_binding_runtime.py",
    ])
    assert evidence.reuse_analysis_complete, evidence.reasons
    assert evidence.source_of_truth == "docs/governance/ELO_OPERATOR_GITHUB_BINDING_RUNTIME.md"
    assert evidence.canonical_identity == "elo-authz"
    assert evidence.duplicate_or_parallel is False
    assert evidence.decision == "STRENGTHEN"


def test_authz_owner_reconciles_real_pr1173_paths_in_repository() -> None:
    """Integration: the stacked atomicity PR remains the same governed owner."""
    root = Path(__file__).resolve().parents[2]
    evidence = reconcile_repository(root, [
        ".github/workflows/elo-authz-atomic-db-test.yml",
        "supabase/functions/elo-authz/index.ts",
        "supabase/migrations/20261110185000_elo_atomic_grant_audit_rpc.sql",
        "tests/security/sql/elo_atomic_grant_integration.sql",
        "tests/security/test_elo_atomic_grant_issuance_contract.py",
        "tests/security/test_operator_github_binding_runtime.py",
    ])
    assert evidence.reuse_analysis_complete, evidence.reasons
    assert evidence.source_of_truth == "docs/governance/ELO_OPERATOR_GITHUB_BINDING_RUNTIME.md"
    assert evidence.canonical_identity == "elo-authz"
    assert evidence.duplicate_or_parallel is False
    assert evidence.decision == "STRENGTHEN"
