"""Deterministic repository reconciliation for ELO canonicality gates."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Iterable

DECISIONS = ("REUSE", "STRENGTHEN", "REFACTOR", "DEPRECATE", "CREATE")
CANONICAL_STRUCTURE_MAP = "02-architecture-library/ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md"

# Bounded ownership of the EXISTING read-only live reconciliation facility.
# This is a verified owner resolution, not permission to merge or introduce a
# new authority. Anything outside these exact paths remains unclassified.
LIVE_RECONCILIATION_CONTRACT = "docs/governance/ELO_LIVE_STATE_RECONCILIATION_CONTRACT.md"
LIVE_RECONCILIATION_RUNTIME = "src/elo/infrastructure/live_state_reconciliation.py"
LIVE_RECONCILIATION_CLI = "scripts/run_live_reconciliation.py"
LIVE_RECONCILIATION_WORKFLOW = ".github/workflows/elo-live-reconciliation.yml"
LIVE_RECONCILIATION_SCOPE = frozenset({
    LIVE_RECONCILIATION_CLI,
    LIVE_RECONCILIATION_WORKFLOW,
    "tests/infrastructure/test_live_reconciliation_workflow.py",
    # Self-audit changes require the same proof and normal CI/review gates.
    "automation/tasks/elo_canonical_reconciliation.py",
    "tests/governance/test_elo_canonical_reconciliation.py",
})
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


def _verified_live_reconciliation_owner(root: Path, changed: set[str]) -> bool:
    """Require the existing contract and implementation chain, not a label.

    Restrict this to known files. A new module, unrelated workflow or parallel
    reconciler may not gain canonical status from filename similarities.
    """
    if LIVE_RECONCILIATION_CLI not in changed:
        return False
    if not changed.issubset(LIVE_RECONCILIATION_SCOPE):
        return False

    contract = root / LIVE_RECONCILIATION_CONTRACT
    runtime = root / LIVE_RECONCILIATION_RUNTIME
    cli = root / LIVE_RECONCILIATION_CLI
    workflow = root / LIVE_RECONCILIATION_WORKFLOW
    structure_map = root / CANONICAL_STRUCTURE_MAP
    if not all(p.is_file() for p in (contract, runtime, cli, workflow, structure_map)):
        return False

    contract_text = contract.read_text(encoding="utf-8", errors="ignore")
    runtime_text = runtime.read_text(encoding="utf-8", errors="ignore")
    cli_text = cli.read_text(encoding="utf-8", errors="ignore")
    workflow_text = workflow.read_text(encoding="utf-8", errors="ignore")
    map_text = structure_map.read_text(encoding="utf-8", errors="ignore")
    return all((
        "owner: ELO Governance" in contract_text,
        "ELO_LIVE_STATE_RECONCILIATION_CONTRACT" in runtime_text,
        "from elo.infrastructure.live_state_reconciliation import" in cli_text,
        "LiveStateReconciliation" in cli_text,
        "scripts/run_live_reconciliation.py" in workflow_text,
        "src/elo/" in map_text,
        "canonical executable root" in map_text,
    ))


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

    scoped_live_reconciliation = (
        not candidates
        and not owner_evidence
        and _verified_live_reconciliation_owner(root, changed_normalised)
    )
    if scoped_live_reconciliation:
        source_of_truth = LIVE_RECONCILIATION_RUNTIME
        canonical_identity = "elo-live-state-reconciliation"
        duplicate = False
        owners.append(LIVE_RECONCILIATION_CONTRACT)
        reasons = ["Existing read-only reconciler, governance owner and workflow chain verified"]

    frontend_changed = any(p.startswith("frontend/") for p in changed_normalised)
    if frontend_changed and owners and not candidates and not maintenance_changed:
        source_of_truth = owners[0]
        canonical_identity = "frontend"
        duplicate = False
        reasons = ["Existing canonical frontend surface is being reused; no parallel executable candidate found"]

    complete = bool(canonical_identity and source_of_truth and duplicate is not None)
    decision = (
        "STRENGTHEN" if scoped_live_reconciliation and complete
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
