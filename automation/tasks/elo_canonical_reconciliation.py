"""Deterministic repository reconciliation for ELO canonicality gates.

This module does not decide architectural ownership by itself. It gathers
repository evidence and converts it into explicit, conservative facts for the
existing Maintenance Coordinator gate.

Rule: UNKNOWN is never treated as TRUE. Missing evidence produces
WAITING_FOR_EVIDENCE rather than permitting creation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


DECISIONS = ("REUSE", "STRENGTHEN", "REFACTOR", "DEPRECATE", "CREATE")
CANONICAL_STRUCTURE_MAP = "02-architecture-library/ELO_REPOSITORY_CANONICAL_STRUCTURE_MAP.md"
SELF_AUDIT_PATHS = {
    "automation/tasks/elo_canonical_reconciliation.py",
    "automation/ELO_MAINTENANCE_COORDINATOR.md",
    "automation/tasks/elo_maintenance_coordinator.py",
}
AUDIT_INFRA_PREFIXES = (
    ".github/",
    "automation/",
    "docs/",
    "tests/",
)
SOURCE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".jsx", ".sql", ".yml", ".yaml"}
GENERIC_CONCEPT_TERMS = {
    "package",
    "index",
    "config",
    "configuration",
    "readme",
    "test",
    "tests",
    "utils",
    "types",
}


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
    return tuple(
        sorted(
            {
                term.strip().lower()
                for term in terms
                if term and term.strip() and term.strip().lower() not in GENERIC_CONCEPT_TERMS
            }
        )
    )


def _is_audit_infrastructure(relative: str) -> bool:
    """Governance/audit artifacts are evidence about capabilities, not capabilities."""
    normalized = relative.replace("\\", "/")
    return normalized.startswith(AUDIT_INFRA_PREFIXES)


def reconcile_repository(
    root: str | Path,
    changed_paths: Iterable[str],
    concept_terms: Iterable[str] | None = None,
) -> ReconciliationEvidence:
    """Inspect changed paths and repository references without mutating files.

    A same-stem or concept-linked source is a *candidate*. It becomes a
    proven duplicate/parallel capability only when explicit canonical
    owner/source evidence identifies that existing candidate. Candidate
    discovery alone therefore remains UNKNOWN.

    Governance, test, documentation and automation artifacts are evidence
    about the canonical runtime; they are not themselves runtime capabilities
    and must not be promoted to duplicate/parallel candidates.
    """
    root = Path(root)
    changed = tuple(sorted(set(changed_paths)))
    if not changed:
        return ReconciliationEvidence(
            changed_paths=(), candidates=(), references=(), owners=(),
            source_of_truth=None, canonical_identity=None,
            duplicate_or_parallel=None, reuse_analysis_complete=False,
            decision=None, reasons=("No changed paths supplied",),
        )

    changed_stems = {Path(p).stem.lower().replace("-", "_") for p in changed}
    terms = _normalise_terms(concept_terms or ())
    all_files = list(_text_files(root))
    changed_normalised = {p.replace("\\", "/") for p in changed}

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

        self_audit_reference = relative in SELF_AUDIT_PATHS
        audit_infrastructure = _is_audit_infrastructure(relative)
        stem_hit = any(stem in lower or stem in path_lower for stem in changed_stems)
        concept_hit = bool(terms) and any(term in lower or term in path_lower for term in terms)
        if (stem_hit or concept_hit) and not self_audit_reference and not audit_infrastructure:
            references.append(relative)

        explicit_owner = any(
            marker in lower
            for marker in ("canonical owner", "canonical authority", "source of truth")
        )
        if explicit_owner and (stem_hit or concept_hit) and not self_audit_reference and not audit_infrastructure:
            owners.append(relative)
            owner_evidence.append((relative, lower))

        if (stem_hit or concept_hit) and not explicit_owner and not self_audit_reference and not audit_infrastructure:
            independent_references.append(relative)

        # Only executable/application source can be a competing capability.
        # Tests, docs, workflows and maintenance automation are supporting
        # evidence and are deliberately excluded from candidate discovery.
        source_candidate = (
            not self_audit_reference
            and not audit_infrastructure
            and path.suffix.lower() in SOURCE_SUFFIXES
            and (
                path.stem.lower().replace("-", "_") in changed_stems
                or concept_hit
            )
        )
        if source_candidate:
            candidates.append(relative)

    candidates = sorted(set(candidates))
    references = sorted(set(references))
    owners = sorted(set(owners))
    independent_references = sorted(set(independent_references))

    candidate_stems = {
        Path(candidate).stem.lower().replace("-", "_")
        for candidate in candidates
    }
    owner_targets = {
        stem
        for _, text in owner_evidence
        for stem in candidate_stems
        if stem in text
    }

    duplicate: bool | None
    if candidate_stems.intersection(owner_targets):
        duplicate = True
    else:
        duplicate = None
        if candidates:
            reasons = ["Existing executable candidate found, but duplicate/parallel capability is not proven"]
        elif independent_references:
            reasons = ["Related runtime references found, but duplicate/parallel capability is not proven"]
        else:
            reasons = ["Duplicate state is not proven; absence is not sufficient to authorize CREATE"]

    if candidate_stems.intersection(owner_targets):
        reasons = ["Existing candidate is explicitly identified as canonical source of truth"]

    canonical_identity = None
    source_of_truth = None
    if owners:
        source_of_truth = owners[0]
        if len(changed_stems) == 1:
            canonical_identity = next(iter(changed_stems))
    else:
        reasons.append("Canonical owner/source of truth not explicitly proven")

    structure_map = root / CANONICAL_STRUCTURE_MAP
    executable_changed = any(
        path.replace("\\", "/").startswith("src/elo/") for path in changed
    )
    if not owners and executable_changed and structure_map.is_file():
        source_of_truth = CANONICAL_STRUCTURE_MAP
        canonical_identity = "src/elo"
        if duplicate is None and not candidates:
            duplicate = False
            reasons.append("Canonical structure map resolves src/elo as the executable ELO owner")

    maintenance_changed = all(path.replace("\\", "/") in SELF_AUDIT_PATHS for path in changed)
    if maintenance_changed and structure_map.is_file():
        source_of_truth = CANONICAL_STRUCTURE_MAP
        canonical_identity = "elo-maintenance-governance"
        duplicate = False
        reasons = ["Maintenance/governance infrastructure is audited against the repository canonical map"]

    complete = bool(canonical_identity and source_of_truth and duplicate is not None)
    decision = None
    if complete:
        decision = "REUSE" if duplicate else "CREATE"
    else:
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
    """Map evidence to the existing canonicality Event contract conservatively."""
    return {
        "canonical_identity_valid": evidence.canonical_identity is not None,
        "canonical_target_resolved": evidence.source_of_truth is not None,
        "source_of_truth_resolved": evidence.source_of_truth is not None,
        "reuse_analysis_complete": evidence.reuse_analysis_complete,
        "duplicate_or_parallel_found": evidence.duplicate_or_parallel,
        "contract_conflict": False if evidence.reuse_analysis_complete else None,
    }
