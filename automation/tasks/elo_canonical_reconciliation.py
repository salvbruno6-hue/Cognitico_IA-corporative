"""Deterministic repository reconciliation for ELO canonicality gates."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Iterable

DECISIONS = ("REUSE", "STRENGTHEN", "REFACTOR", "DEPRECATE", "CREATE")
CANONICAL_STRUCTURE_MAP = "02-architecture-library/ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md"
GOVERNANCE_LIFECYCLE_SOURCE = "10-adr/ADR-0020-end-to-end-cycle.md"
GOVERNANCE_LIFECYCLE_CONTRACT = "docs/governance/ELO_MERGE_COORDINATOR.md"
GOVERNANCE_LIFECYCLE_WORKFLOWS = {
    ".github/workflows/elo-agent-loop.yml",
    ".github/workflows/elo-maintenance-coordinator.yml",
    ".github/workflows/elo-merge-coordinator.yml",
}
GOVERNANCE_LIFECYCLE_ALLOWED_PATHS = GOVERNANCE_LIFECYCLE_WORKFLOWS | {
    GOVERNANCE_LIFECYCLE_SOURCE,
    GOVERNANCE_LIFECYCLE_CONTRACT,
    "tests/governance/test_merge_coordinator_contract.py",
    "automation/tasks/elo_canonical_reconciliation.py",
    CANONICAL_STRUCTURE_MAP,
    "tests/governance/test_elo_canonical_reconciliation.py",
}
SELF_AUDIT_PATHS = {
    "automation/tasks/elo_canonical_reconciliation.py",
    "automation/ELO_MAINTENANCE_COORDINATOR.md",
    "automation/tasks/elo_maintenance_coordinator.py",
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
    decision_override: str | None = None
    structure_map = root / CANONICAL_STRUCTURE_MAP

    if changed_in_runtime and structure_map.is_file() and not owner_evidence:
        source_of_truth = CANONICAL_STRUCTURE_MAP
        canonical_identity = "src/elo"
        duplicate = False
        reasons = ["Canonical structure map resolves src/elo as the executable ELO owner"]

    maintenance_changed = all(p.replace("\\", "/") in SELF_AUDIT_PATHS for p in changed)
    if maintenance_changed and structure_map.is_file():
        source_of_truth = CANONICAL_STRUCTURE_MAP
        canonical_identity = "elo-maintenance-governance"
        duplicate = False
        reasons = ["Maintenance/governance infrastructure is audited against the repository canonical map"]

    governance_workflow_changed = bool(changed_normalised.intersection(GOVERNANCE_LIFECYCLE_WORKFLOWS))
    governance_lifecycle_scoped = (
        governance_workflow_changed
        and changed_normalised.issubset(GOVERNANCE_LIFECYCLE_ALLOWED_PATHS)
    )
    if governance_lifecycle_scoped and structure_map.is_file():
        lifecycle_source = root / GOVERNANCE_LIFECYCLE_SOURCE
        lifecycle_contract = root / GOVERNANCE_LIFECYCLE_CONTRACT
        try:
            map_text = structure_map.read_text(encoding="utf-8", errors="ignore")
            source_text = lifecycle_source.read_text(encoding="utf-8", errors="ignore")
            contract_text = lifecycle_contract.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            map_text = source_text = contract_text = ""
        workflow_owner_declared = (
            "`.github/workflows/elo-*.yml` | ELO Governance" in map_text
            and "elo-agent-loop.yml" in source_text
            and "elo-merge-coordinator.yml" in source_text
            and "owner: ELO Governance" in contract_text
        )
        if workflow_owner_declared:
            source_of_truth = GOVERNANCE_LIFECYCLE_SOURCE
            canonical_identity = "elo-governed-pr-lifecycle"
            duplicate = False
            decision_override = "STRENGTHEN"
            reasons = [
                "Existing ELO governance lifecycle owner is declared by ADR-0020 and the repository canonical map"
            ]

    frontend_changed = any(p.startswith("frontend/") for p in changed_normalised)
    if frontend_changed and owners and not candidates and not maintenance_changed:
        source_of_truth = owners[0]
        canonical_identity = "frontend"
        duplicate = False
        reasons = ["Existing canonical frontend surface is being reused; no parallel executable candidate found"]

    complete = bool(canonical_identity and source_of_truth and duplicate is not None)
    decision = decision_override or ("REUSE" if complete and duplicate else "CREATE" if complete else None)
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
