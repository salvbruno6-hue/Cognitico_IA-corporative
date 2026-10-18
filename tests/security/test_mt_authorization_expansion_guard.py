"""Regression guard for the unresolved MT tenant-authorization boundary.

Historical checked-in migrations remain immutable evidence. Until elo-authz has a
live ENTERPRISE/MULTITEINER membership contract, no *new migration file* may
expand authenticated/PUBLIC MT access with literal-true RLS predicates.
"""
from __future__ import annotations

import re
from pathlib import Path

MIGRATIONS = Path("supabase/migrations")

# Explicit checked-in baseline at introduction of this guard. This is path based,
# not timestamp based, so a concurrent branch cannot evade the guard by carrying
# an older migration timestamp. Additions require a governed review of this test.
LEGACY_PERMISSIVE_MT_POLICY_FILES = {
    "20261016174348_protege_tabelas_m01_rls_admin_canonico.sql",
}

CREATE_POLICY = re.compile(r"create\s+policy\b(?:(?!;).)*?;", re.IGNORECASE | re.DOTALL)
MT_TABLE = re.compile(r"\bon\s+(?:public\.)?mt_[a-z0-9_]+\b", re.IGNORECASE)
LITERAL_TRUE = re.compile(
    r"(?:\busing\s*\(\s*true\s*\)|\bwith\s+check\s*\(\s*true\s*\))",
    re.IGNORECASE,
)
TO_ROLES = re.compile(
    r"\bto\s+(.+?)(?=\busing\b|\bwith\s+check\b|;)",
    re.IGNORECASE | re.DOTALL,
)


def _applies_to_authenticated(statement: str) -> bool:
    """No TO means PUBLIC; explicit PUBLIC/authenticated also reaches clients."""
    match = TO_ROLES.search(statement)
    if match is None:
        return True
    roles = {
        role.strip().strip('"').lower()
        for role in match.group(1).split(",")
        if role.strip()
    }
    return "authenticated" in roles or "public" in roles


def _contains_permissive_mt_client_policy(sql: str) -> bool:
    for statement in CREATE_POLICY.findall(sql):
        if (
            MT_TABLE.search(statement)
            and LITERAL_TRUE.search(statement)
            and _applies_to_authenticated(statement)
        ):
            return True
    return False


def test_no_new_authenticated_or_public_literal_true_mt_policy() -> None:
    observed = {
        path.name
        for path in MIGRATIONS.glob("*.sql")
        if _contains_permissive_mt_client_policy(path.read_text(encoding="utf-8"))
    }
    unexpected = sorted(observed - LEGACY_PERMISSIVE_MT_POLICY_FILES)

    assert not unexpected, (
        "New MT literal-true RLS policies expand an unresolved tenant-authorization "
        "GAP for authenticated/PUBLIC. Route authorization through the canonical "
        "elo-authz identity/scope/capability contract first. New files: "
        + ", ".join(unexpected)
    )


def test_legacy_baseline_is_still_present_and_explicit() -> None:
    missing = sorted(
        name for name in LEGACY_PERMISSIVE_MT_POLICY_FILES if not (MIGRATIONS / name).exists()
    )
    assert not missing, "Guard baseline refers to missing historical migrations: " + ", ".join(missing)


def test_guard_documents_current_authority_boundary() -> None:
    decision = Path(
        "docs/architecture/ELO_OKR_ENTERPRISE_TENANT_SCOPE_DECISION_20261009.md"
    ).read_text(encoding="utf-8")
    health = Path("docs/governance/ELO_SYSTEM_HEALTH_GATE.md").read_text(
        encoding="utf-8"
    )
    health_sql = Path("supabase/health/elo_system_health_gate.sql").read_text(
        encoding="utf-8"
    )

    assert "Status: PREPARED / NOT LIVE" in decision
    assert "scope_type = ENTERPRISE" in decision
    assert "scope_key  = MULTITEINER" in decision
    assert "elo_identity_scopes" in decision
    assert "GAP_HIGH" in health
    assert "AUTHZ_MT_PERMISSIVE_TRUE" in health_sql
