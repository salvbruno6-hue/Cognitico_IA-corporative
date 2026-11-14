"""Behavioral regression: existing elo-authz owner resolves only for governed paths."""
from pathlib import Path
import tempfile

from automation.tasks.elo_canonical_reconciliation import reconcile_repository

MAP = "02-architecture-library/ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md"
CONTRACT = "docs/governance/ELO_OPERATOR_GITHUB_BINDING_RUNTIME.md"
OWNER = "supabase/functions/elo-authz/index.ts"
MIGRATION = "supabase/migrations/20260919220335_elo_operator_github_binding_runtime.sql"
ATOMIC = "supabase/migrations/20261114000000_elo_atomic_grant_audit_rpc.sql"


def fixture(root: Path) -> None:
    for path, content in (
        (MAP, "`supabase/functions/elo-authz/` | canonical owner"),
        (CONTRACT, "elo-authz owner: supabase/functions/elo-authz/index.ts"),
        (OWNER, "export const owner = 'elo-authz';"),
        (MIGRATION, "-- canonical persistence"),
        (ATOMIC, "-- existing migration candidate"),
    ):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def test_existing_authz_owner_resolves_without_new_authority():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        fixture(root)
        result = reconcile_repository(root, [OWNER, ATOMIC, "tests/security/sql/elo_atomic_grant_integration.sql"])
        assert result.source_of_truth == MAP
        assert result.canonical_identity == "elo-authz"
        assert result.duplicate_or_parallel is False
        assert result.reuse_analysis_complete is True


def test_unknown_path_or_unknown_migration_fail_closed():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        fixture(root)
        for paths in ([OWNER, "supabase/migrations/unknown.sql"], [OWNER, "src/other/core.py"]):
            result = reconcile_repository(root, paths)
            assert result.reuse_analysis_complete is False


def test_missing_owner_contract_or_map_fail_closed():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        fixture(root)
        for missing in (OWNER, CONTRACT, MAP, MIGRATION):
            target = root / missing
            saved = target.read_text()
            target.unlink()
            result = reconcile_repository(root, [OWNER])
            assert result.reuse_analysis_complete is False
            target.write_text(saved)


def test_self_review_exact_paths_only():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        fixture(root)
        paths = ["automation/tasks/elo_canonical_reconciliation.py", MAP, "tests/test_elo_authz_owner_reconciliation.py"]
        result = reconcile_repository(root, paths)
        assert result.reuse_analysis_complete is True
        assert result.canonical_identity == "elo-maintenance-governance"
        result = reconcile_repository(root, paths + ["src/other/new_core.py"])
        assert result.reuse_analysis_complete is False
