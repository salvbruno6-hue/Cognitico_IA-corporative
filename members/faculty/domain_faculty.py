"""Provider-neutral domain faculty primitives.

A DomainFaculty captures reusable domain logic. DomainOverlay captures a
contextual variation without mutating the faculty. No persistence or provider
is owned here; lifecycle and admission remain governed by the ELO Core.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Tuple


class ComparisonKind(str, Enum):
    COMPATIBLE = "COMPATIBLE"
    VARIATION = "VARIATION"
    COMPLEMENT = "COMPLEMENT"
    CONFLICT = "CONFLICT"
    NEW = "NEW"


@dataclass(frozen=True)
class LogicStep:
    name: str
    kind: str
    required: bool = True


@dataclass(frozen=True)
class DomainFaculty:
    domain: str
    version: str
    objective: str
    steps: Tuple[LogicStep, ...]
    invariants: FrozenSet[str] = frozenset()

    @property
    def step_names(self) -> FrozenSet[str]:
        return frozenset(step.name for step in self.steps)


@dataclass(frozen=True)
class DomainOverlay:
    overlay_id: str
    domain: str
    source_member: str
    version: str
    differences: Tuple[str, ...]
    removable: bool = True


@dataclass(frozen=True)
class FacultyComparisonResult:
    classification: ComparisonKind
    shared_steps: FrozenSet[str]
    missing_steps: FrozenSet[str]
    added_steps: FrozenSet[str]
    differences: Tuple[str, ...] = ()


def compare_faculty(
    faculty: DomainFaculty,
    candidate: DomainFaculty,
) -> FacultyComparisonResult:
    """Compare a candidate flow without mutating the canonical faculty."""
    if faculty.domain != candidate.domain:
        return FacultyComparisonResult(
            classification=ComparisonKind.CONFLICT,
            shared_steps=frozenset(),
            missing_steps=frozenset(faculty.step_names),
            added_steps=frozenset(candidate.step_names),
            differences=("domain mismatch",),
        )

    shared = faculty.step_names & candidate.step_names
    missing = faculty.step_names - candidate.step_names
    added = candidate.step_names - faculty.step_names

    if not missing and not added:
        kind = ComparisonKind.COMPATIBLE
    elif added and not missing:
        kind = ComparisonKind.COMPLEMENT
    elif missing and added:
        kind = ComparisonKind.VARIATION
    else:
        kind = ComparisonKind.VARIATION

    return FacultyComparisonResult(
        classification=kind,
        shared_steps=frozenset(shared),
        missing_steps=frozenset(missing),
        added_steps=frozenset(added),
        differences=tuple(sorted((*missing, *added))),
    )


def build_overlay(
    candidate: DomainFaculty,
    source_member: str,
    comparison: FacultyComparisonResult,
    overlay_id: str,
) -> DomainOverlay:
    """Create a removable contextual overlay from a governed comparison."""
    if comparison.classification not in {
        ComparisonKind.VARIATION,
        ComparisonKind.COMPLEMENT,
    }:
        raise ValueError("an overlay requires a variation or complement")
    return DomainOverlay(
        overlay_id=overlay_id,
        domain=candidate.domain,
        source_member=source_member,
        version=candidate.version,
        differences=comparison.differences,
    )
