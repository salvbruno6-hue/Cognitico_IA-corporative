"""Regression guard for the unresolved MT tenant-authorization boundary.

Historical MT migrations intentionally remain immutable evidence. Until elo-authz
has a live ENTERPRISE/MULTITEINER membership contract, new migrations must not
expand authenticated MT access with literal-true RLS predicates.
"""
from __future__ import annotations

import re
from pathlib import Path

MIGRATIONS = Path("supabase/migrations")
CUTOFF_VERSION = "20261018200927"

# Scope this guard to policy statements that target an mt_* table and grant the
# authenticated role literal-unrestricted row access. The regex is deliberately
# formatting-tolerant but bounded to one CREATE POLICY statement.
PERMISSIVE_MT_AUTHENTICATED = re.compile(
    r"create\s+policy\b(?:(?!;).)*?\bon\s+(?:public\.)?mt_[a-z0-9_]+"
    r"(?:(?!;).)*?\bto\s+authenticated\b"
    r"(?:(?!;).)*?(?:\busing\s*\(\s*true\s*\)|\bwith\s+check\s*\(\s*true\s*\))",
    re.IGNORECASE | re.DOTALL,
)


def _migration_version(path: Path) -> str | None:
    match = re.match(r"(\d{14})_", path.name)
    return match.group(1) if match else None


def _post_cutoff_migrations() -> list[Path]:
    migrations: list[Path] = []
    for path in MIGRATIONS.glob("*.sql"):
        version = _migration_version(path)
        if version is not None and version > CUTOFF_VERSION:
            migrations.append(path)
    return sorted(migrations)


def test_no_new_authenticated_literal_true_mt_policy() -> None:
    offenders: list[str] = []
    for path in _post_cutoff_migrations():
        sql = path.read_text(encoding="utf-8")
        if PERMISSIVE_MT_AUTHENTICATED.search(sql):
            offenders.append(path.as_posix())

    assert not offenders, (
        "New MT authenticated literal-true RLS policies expand an unresolved "
        "tenant-authorization GAP. Route authorization through the canonical "
        "elo-authz identity/scope/capability contract first. Offenders: "
        + ", ".join(offenders)
    )


def test_guard_documents_current_authority_boundary() -> None:
    decision = Path(
        "docs/architecture/ELO_OKR_ENTERPRISE_TENANT_SCOPE_DECISION_20261009.md"
    ).read_text(encoding="utf-8")
    health = Path("docs/governance/ELO_SYSTEM_HEALTH_GATE.md").read_text(
        encoding="utf-8"
    )

    assert "Status: PREPARED / NOT LIVE" in decision
    assert "scope_type = ENTERPRISE" in decision
    assert "scope_key  = MULTITEINER" in decision
    assert "elo_identity_scopes" in decision
    assert "GAP_HIGH" in health
    assert "AUTHZ_MT_PERMISSIVE_TRUE" in health
