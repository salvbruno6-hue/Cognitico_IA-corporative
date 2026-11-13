"""Deterministic repository reconciliation for ELO canonicality gates."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Iterable

DECISIONS = ("REUSE", "STRENGTHEN", "REFACTOR", "DEPRECATE", "CREATE")
CANONICAL_STRUCTURE_MAP = "02-architecture-library/ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md"
AUTHZ_CANONICAL_RUNTIME = "supabase/functions/elo-authz/index.ts"
AUTHZ_OWNER_CONTRACT = "docs/governance/ELO_OPERATOR_GITHUB_BINDING_RUNTIME.md"
# Only exact, already-reviewed implementation and test paths; no broad migration
# or workflow wildcard. The owner remains the existing elo-authz runtime.
# Existing specialized consumers of elo-authz. These two providers call the
# canonical issuer but are not grant issuers themselves. Anything else found
# during discovery is unresolved until disambiguated, never silently safe.
AUTHZ_KNOWN_DISTINCT_CONSUMERS = frozenset({
    "supabase/functions/elo-data-gateway/index.ts",
    "supabase/functions/elo-mcp/index.ts",
})


# Independently identify potential grant writers. The Maintenance workflow
# derives concept_terms from changed filenames (often just "index"), which
# cannot be trusted to discover an unreviewed parallel issuer with another name.
# This scan is additional evidence, not a second authorization authority.
AUTHZ_DIRECT_WRITE_SIGNATURES = (
    re.compile(r"/rest/v1/elo_authorization_grants", re.IGNORECASE),
    re.compile(r"\binsert\s+into\s+(?:public\.)?elo_authorization_grants\b", re.IGNORECASE),
    re.compile(r"\belo_atomic_issue_authorization_grant\s*\(", re.IGNORECASE),
    re.compile(
        r"\.from\(\s*['\\"](?:public\.)?elo_authorization_grants['\\"]\s*\)"
        r"[\s\S]{0,240}?\.(?:insert|upsert)\s*\(",
        re.IGNORECASE,
    ),
)


def _unreviewed_authz_writers(root: Path, source_files: Iterable[Path]) -> set[str]:
    """Find executable grant writers even when filename-derived terms miss them."""
    unreviewed: set[str] = set()
    for path in source_files:
        relative = str(path.relative_to(root)).replace("\\", "/")
        if relative in AUTHZ_GOVERNED_PATHS:
            continue
        # Never promote test mocks, docs or reconciler implementation as issuers.
        if relative.startswith(("tests/", "docs/", ".github/", "automation/")):
            continue
        if path.suffix.lower() not in {".py", ".ts", ".tsx", ".js", ".jsx", ".sql"}:
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if any(signature.search(content) for signature in AUTHZ_DIRECT_WRITE_SIGNATURES):
            unreviewed.add(relative)
    return unreviewed


def _is_distinct_authz_consumer(root: Path, candidate: str) -> bool:
    if candidate not in AUTHZ_KNOWN_DISTINCT_CONSUMERS:
        return False
    path = root / candidate
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8", errors="ignore")
    return (
        "elo-authz" in content
        and "issue_authorization_grant" not in content
        and "elo_authorization_grants" not in content
    )


AUTHZ_GOVERNED_PATHS = frozenset({
    AUTHZ_CANONICAL_RUNTIME,
    "tests/security/test_operator_github_binding_runtime.py",
    "tests/security/test_elo_atomic_grant_issuance_contract.py",
    "tests/security/sql/elo_atomic_grant_integration.sql",
    "supabase/migrations/20261110185000_elo_atomic_grant_audit_rpc.sql",
    ".github/workflows/elo-authz-atomic-db-test.yml",
})
SELF_AUDIT_PATHS = {
    "automation/tasks/elo_canonical_reconciliation.py",
    "automation/ELO_MAINTENANCE_COORDINATOR.md",
    "automation/tasks/elo_maintenance_coordinator.py",
}
SELF_AUDIT_SUPPORT_PATHS = {
    CANONICAL_STRUCTURE_MAP,
    "tests/governance/test_elo_canonical_reconciliation.py",
}
AUDIT_INFRA_PREFIXES = (".github/", "automation/", "docs/", "tests/")
SOURCE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".sql", ".yml", ".yaml"}
GENERIC_CONCEPT_TERMS = {"package", "index", "config", "configuration", "readme", "test", "tests", "utils", "types", "app", "css"}
EXPLICIT_OWNER_PATTERN = re.compile(
    r"(?:canonical owner|canonical authority|source of truth)\s*:\s*([^\n#`]+)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ReconciliationEvidence:
    changed_paths: tuple[str, ...]
    candidates: tuple[str, ...]
    references: tuple[str, ...]
    owners: tuple[str, ...]
    source_of_truth: str | None
    canonical_identity: str | None
    duplicate_or_parallel: bool | None
    reuse_analysis_complete: bool
    decision: str | None
    reasons: tuple[str, ...] = field(default_factory=tuple)

    @property
    def waiting_for_evidence(self) -> bool:
        return not self.reuse_analysis_complete or self.duplicate_or_parallel is None


def _text_files(root: Path) -> Iterable[Path]:
    ignored = {".git", ".venv", "venv", "node_modules", "__pycache__"}
    for path in root.rglob("*"):
        if path.is_file() and not any(part in ignored for part in path.parts):
            try:
                if path.stat().st_size <= 1_000_000:
                    yield path
            except OSError:
                continue


def _normalise_terms(terms: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({term.strip().lower() for term in terms if term and term.strip() and term.strip().lower() not in GENERIC_CONCEPT_TERMS}))


def _is_audit_infrastructure(relative: str) -> bool:
    return relative.replace("\\", "/").startswith(AUDIT_INFRA_PREFIXES)


def _explicit_owner_targets(text: str, candidate_stems: set[str]) -> set[str]:
    """Return candidates explicitly named by an owner/source-of-truth declaration."""
    targets: set[str] = set()
    for match in EXPLICIT_OWNER_PATTERN.finditer(text):
        declared = match.group(1).strip().strip("'\"")
        declared_stem = Path(declared.replace("\\", "/")).stem.lower().replace("-", "_")
        if declared_stem in candidate_stems:
            targets.add(declared_stem)
    return targets


def _is_governed_authz_change(root: Path, changed: set[str]) -> bool:
    """Resolve the existing authz issuer only from its real contract and map."""
    if AUTHZ_CANONICAL_RUNTIME not in changed:
        return False
    if not changed.issubset(AUTHZ_GOVERNED_PATHS):
        return False

    runtime = root / AUTHZ_CANONICAL_RUNTIME
    owner_contract = root / AUTHZ_OWNER_CONTRACT
    structure_map = root / CANONICAL_STRUCTURE_MAP
    if not (runtime.is_file() and owner_contract.is_file() and structure_map.is_file()):
        return False

    contract = owner_contract.read_text(encoding="utf-8", errors="ignore")
    structure = structure_map.read_text(encoding="utf-8", errors="ignore")
    runtime_text = runtime.read_text(encoding="utf-8", errors="ignore")
    return (
        "elo-authz" in contract
        and "issue_authorization_grant" in contract
        and "ELO_OPERATOR_GITHUB_BINDING_RUNTIME.md" in structure
        and "| supabase/functions/elo-authz/ |" in structure
        and "resolveAuthorizationGrant" in runtime_text
    )


def reconcile_repository(root: str | Path, changed_paths: Iterable[str], concept_terms: Iterable[str] | None = None) -> ReconciliationEvidence:
    root = Path(root)
    changed = tuple(sorted(set(changed_paths)))
    if not changed:
        return ReconciliationEvidence((), (), (), (), None, None, None, False, None, ("No changed paths supplied",))

    changed_normalised = {p.replace("\\", "/") for p in changed}
    changed_stems = {Path(p).stem.lower().replace("-", "_") for p in changed}
    terms = _normalise_terms(concept_terms or ())
    changed_in_runtime = any(p.startswith("src/elo/") for p in changed_normalised)
    all_files = list(_text_files(root))

    candidates: list[str] = []
    references: list[str] = []
    owners: list[str] = []
    owner_evidence: list[tuple[str, str]] = []
    independent_references: list[str] = []

    for path in all_files:
        relative = str(path.relative_to(root)).replace("\\", "/")
        if relative in changed_normalised:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lower = text.lower()
        path_lower = relative.lower()
        self_audit = relative in SELF_AUDIT_PATHS
        audit_infrastructure = _is_audit_infrastructure(relative)
        stem_hit = any(stem in lower or stem in path_lower for stem in changed_stems)
        concept_hit = bool(terms) and any(term in lower or term in path_lower for term in terms)
        related = stem_hit or concept_hit

        if related and not self_audit and not audit_infrastructure:
            references.append(relative)

        explicit_owner = bool(EXPLICIT_OWNER_PATTERN.search(text))
        if explicit_owner and related and not self_audit and not audit_infrastructure:
            owners.append(relative)
            owner_evidence.append((relative, lower))
        elif related and not self_audit and not audit_infrastructure:
            independent_references.append(relative)

        same_canonical_runtime = changed_in_runtime and path_lower.startswith("src/elo/")
        source_candidate = (
            not self_audit
            and not audit_infrastructure
            and not same_canonical_runtime
            and path.suffix.lower() in SOURCE_SUFFIXES
            and (path.stem.lower().replace("-", "_") in changed_stems or concept_hit)
        )
        if source_candidate:
            candidates.append(relative)

    # Search for potential grant writers separately from generic concept/stem
    # discovery. A parallel issuer must remain an unresolved GAP even if it
    # does not mention "index" or the filenames changed by this PR.
    if AUTHZ_CANONICAL_RUNTIME in changed_normalised:
        candidates.extend(sorted(_unreviewed_authz_writers(root, all_files)))
    candidates = sorted(set(candidates))
    references = sorted(set(references))
    owners = sorted(set(owners))
    independent_references = sorted(set(independent_references))
    candidate_stems = {Path(candidate).stem.lower().replace("-", "_") for candidate in candidates}
    owner_targets = {
        stem
        for _, text in owner_evidence
        for stem in _explicit_owner_targets(text, candidate_stems)
    }

    if candidate_stems.intersection(owner_targets):
        duplicate: bool | None = True
        reasons = ["Existing candidate is explicitly identified as canonical source of truth"]
    else:
        duplicate = None
        if candidates:
            reasons = ["Existing executable candidate found, but duplicate/parallel capability is not proven"]
        elif independent_references:
            reasons = ["Related runtime references found, but duplicate/parallel capability is not proven"]
        else:
            reasons = ["Duplicate state is not proven; absence is not sufficient to authorize CREATE"]

    source_of_truth = owners[0] if owners else None
    canonical_identity = next(iter(changed_stems)) if owners and len(changed_stems) == 1 else None
    structure_map = root / CANONICAL_STRUCTURE_MAP

    if changed_in_runtime and structure_map.is_file() and not owner_evidence:
        source_of_truth = CANONICAL_STRUCTURE_MAP
        canonical_identity = "src/elo"
        duplicate = False
        reasons = ["Canonical structure map resolves src/elo as the executable ELO owner"]

    maintenance_changed = (
        any(p.replace("\\", "/") in SELF_AUDIT_PATHS for p in changed)
        and all(
            p.replace("\\", "/") in SELF_AUDIT_PATHS | SELF_AUDIT_SUPPORT_PATHS
            for p in changed
        )
    )
    if maintenance_changed and structure_map.is_file():
        source_of_truth = CANONICAL_STRUCTURE_MAP
        canonical_identity = "elo-maintenance-governance"
        duplicate = False
        reasons = ["Maintenance/governance infrastructure is audited against the repository canonical map"]

    frontend_changed = any(p.startswith("frontend/") for p in changed_normalised)
    if frontend_changed and owners and not candidates and not maintenance_changed:
        source_of_truth = owners[0]
        canonical_identity = "frontend"
        duplicate = False
        reasons = ["Existing canonical frontend surface is being reused; no parallel executable candidate found"]

    # A source-only authz change is not a new capability. Require the existing
    # canonical owner contract and map. Unlisted paths and competing owners
    # remain unresolved, never treated as safe reuse.
    # A scoped owner contract does not prove that newly discovered executable
    # candidates are harmless. Only the two explicitly known, verified
    # consumers may be disregarded; unknown potential issuers remain a GAP.
    authz_candidates_disambiguated = all(
        _is_distinct_authz_consumer(root, candidate) for candidate in candidates
    )
    scoped_authz = (
        not owner_evidence
        and duplicate is None
        and _is_governed_authz_change(root, changed_normalised)
        and authz_candidates_disambiguated
    )
    if scoped_authz:
        source_of_truth = AUTHZ_OWNER_CONTRACT
        canonical_identity = "elo-authz"
        duplicate = False
        owners.append(AUTHZ_OWNER_CONTRACT)
        reasons = ["Existing elo-authz issuer and canonical owner contract verified"]

    complete = bool(canonical_identity and source_of_truth and duplicate is not None)
    decision = (
        "STRENGTHEN" if scoped_authz and complete
        else "REUSE" if complete and duplicate
        else "CREATE" if complete
        else None
    )
    if not complete:
        reasons.append("Canonical owner/source of truth not explicitly proven" if source_of_truth is None else "Reconciliation remains WAITING_FOR_EVIDENCE")
        if source_of_truth is not None:
            reasons.append("Reconciliation remains WAITING_FOR_EVIDENCE")

    return ReconciliationEvidence(
        changed_paths=changed,
        candidates=tuple(candidates),
        references=tuple(references),
        owners=tuple(owners),
        source_of_truth=source_of_truth,
        canonical_identity=canonical_identity,
        duplicate_or_parallel=duplicate,
        reuse_analysis_complete=complete,
        decision=decision,
        reasons=tuple(dict.fromkeys(reasons)),
    )


def event_facts(evidence: ReconciliationEvidence) -> dict[str, object]:
    return {
        "canonical_identity_valid": evidence.canonical_identity is not None,
        "canonical_target_resolved": evidence.source_of_truth is not None,
        "source_of_truth_resolved": evidence.source_of_truth is not None,
        "reuse_analysis_complete": evidence.reuse_analysis_complete,
        "duplicate_or_parallel_found": evidence.duplicate_or_parallel,
        "contract_conflict": False if evidence.reuse_analysis_complete else None,
    }
