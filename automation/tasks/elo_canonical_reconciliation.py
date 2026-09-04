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
import re
from typing import Iterable


DECISIONS = ("REUSE", "STRENGTHEN", "REFACTOR", "DEPRECATE", "CREATE")


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
    return tuple(sorted({term.strip().lower() for term in terms if term and term.strip()}))


def reconcile_repository(
    root: str | Path,
    changed_paths: Iterable[str],
    concept_terms: Iterable[str] | None = None,
) -> ReconciliationEvidence:
    """Inspect changed paths and repository references without mutating files.

    A same-stem candidate or independent concept-linked implementation is
    evidence requiring reconciliation. Owner/source documentation alone is not
    proof of a duplicate implementation. CREATE is admissible only when
    identity, owner/source-of-truth and duplicate state are all explicit.
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
    independent_references: list[str] = []
    reasons: list[str] = []

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

        stem_hit = any(stem in lower or stem in path_lower for stem in changed_stems)
        concept_hit = bool(terms) and any(term in lower or term in path_lower for term in terms)
        if stem_hit or concept_hit:
            references.append(relative)

        explicit_owner = any(
            marker in lower
            for marker in ("canonical owner", "canonical authority", "source of truth")
        )
        if explicit_owner and (stem_hit or concept_hit):
            owners.append(relative)
        if (stem_hit or concept_hit) and not explicit_owner:
            independent_references.append(relative)

        # Same-stem or concept-linked source files are candidates for explicit
        # reconciliation. This is intentionally a candidate signal, not a
        # final ownership decision.
        source_suffixes = {".py", ".ts", ".tsx", ".js", ".jsx", ".sql", ".yml", ".yaml"}
        if path.stem.lower().replace("-", "_") in changed_stems or (
            concept_hit and path.suffix.lower() in source_suffixes
        ):
            candidates.append(relative)

    candidates = sorted(set(candidates))
    references = sorted(set(references))
    owners = sorted(set(owners))
    independent_references = sorted(set(independent_references))

    canonical_identity = None
    source_of_truth = None
    duplicate: bool | None = None

    if candidates:
        duplicate = True
        reasons.append("Existing source candidate requires canonical reconciliation")
    elif independent_references:
        duplicate = True
        reasons.append("Independent repository references indicate a related capability")
    else:
        duplicate = None
        reasons.append("Duplicate state is not proven; absence is not sufficient to authorize CREATE")

    if owners:
        source_of_truth = owners[0]
        if len(changed_stems) == 1:
            canonical_identity = next(iter(changed_stems))
    else:
        reasons.append("Canonical owner/source of truth not explicitly proven")

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
