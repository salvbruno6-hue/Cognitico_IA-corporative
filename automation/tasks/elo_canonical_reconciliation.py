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

    A same-stem or concept-linked source is only a *candidate*. It becomes a
    proven duplicate/parallel capability when explicit canonical owner/source
    evidence identifies that candidate as the existing source of truth.
    Otherwise the duplicate state remains UNKNOWN and CREATE is not admitted.
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
    owner_targets: list[str] = []
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
            # Explicit owner/source evidence is stronger than a generic
            # reference, but it only proves duplication when it identifies an
            # existing candidate path/name.
            for candidate in changed_stems:
                if candidate in lower:
                    owner_targets.append(candidate)

        if (stem_hit or concept_hit) and not explicit_owner:
            independent_references.append(relative)

        source_suffixes = {".py", ".ts", ".tsx", ".js", ".jsx", ".sql", ".yml", ".yaml"}
        if path.stem.lower().replace("-", "_") in changed_stems or (
            concept_hit and path.suffix.lower() in source_suffixes
        ):
            candidates.append(relative)

    candidates = sorted(set(candidates))
    references = sorted(set(references))
    owners = sorted(set(owners))
    independent_references = sorted(set(independent_references))
    owner_targets = sorted(set(owner_targets))

    # Candidate discovery is not itself proof of duplication. Explicit owner /
    # source-of-truth evidence must point at the candidate. Generic references
    # therefore leave the state UNKNOWN rather than creating a false block.
    candidate_stems = {
        Path(candidate).stem.lower().replace("-", "_")
        for candidate in candidates
    }
    duplicate: bool | None
    if candidate_stems.intersection(owner_targets):
        duplicate = True
        reasons.append("Existing candidate is explicitly identified as canonical source of truth")
    else:
        duplicate = None
        if candidates:
            reasons.append("Existing candidate found, but duplicate/parallel capability is not proven")
        elif independent_references:
            reasons.append("Related repository references found, but duplicate/parallel capability is not proven")
        else:
            reasons.append("Duplicate state is not proven; absence is not sufficient to authorize CREATE")

    canonical_identity = None
    source_of_truth = None
    if owners:
        source_of_truth = owners[0]
        if len(changed_stems) == 1:
            canonical_identity = next(iter(changed_stems))
    else:
        reasons.append("Canonical owner/source of truth not explicitly proven")

    # A proven duplicate is sufficient to classify REUSE. For a genuinely new
    # capability, explicit owner/source plus a proven non-duplicate state would
    # be required. UNKNOWN must remain incomplete.
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
