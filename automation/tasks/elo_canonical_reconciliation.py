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


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[A-Za-z0-9_./-]{3,}", text)}


def reconcile_repository(root: str | Path, changed_paths: Iterable[str]) -> ReconciliationEvidence:
    """Inspect changed paths and repository references without mutating files.

    The reconciler is intentionally conservative. It does not infer CREATE from
    absence alone; canonical owner and source-of-truth evidence must be explicit.
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

    changed_names = {Path(p).name.lower() for p in changed}
    changed_stems = {Path(p).stem.lower().replace("-", "_") for p in changed}
    all_files = list(_text_files(root))

    candidates: list[str] = []
    references: list[str] = []
    owners: list[str] = []
    reasons: list[str] = []

    for path in all_files:
        if str(path).replace("\\", "/") in {p.replace("\\", "/") for p in changed}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lower = text.lower()
        path_lower = str(path).lower()
        if any(stem in lower or stem in path_lower for stem in changed_stems):
            references.append(str(path.relative_to(root)))
        if any(word in lower for word in ("canonical owner", "source of truth", "canonical authority")):
            if any(stem in lower for stem in changed_stems):
                owners.append(str(path.relative_to(root)))

    # Explicitly surface same-name/same-stem implementations.
    for path in all_files:
        if path.name.lower() in changed_names or path.stem.lower().replace("-", "_") in changed_stems:
            candidates.append(str(path.relative_to(root)))

    candidates = sorted(set(candidates))
    references = sorted(set(references))
    owners = sorted(set(owners))

    canonical_identity = None
    source_of_truth = None
    duplicate: bool | None = None

    if candidates:
        duplicate = True
        reasons.append("Equivalent or same-stem implementation detected")
    elif references:
        duplicate = True
        reasons.append("Existing repository references indicate related capability")
    else:
        duplicate = None
        reasons.append("No equivalent proven; absence is not sufficient to authorize CREATE")

    # Explicit owner/source evidence is required; do not infer it from naming.
    if owners:
        source_of_truth = owners[0]
        canonical_identity = changed_stems.pop() if len(changed_stems) == 1 else None
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
