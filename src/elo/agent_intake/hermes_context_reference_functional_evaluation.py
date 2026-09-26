"""Controlled functional evidence for Hermes ContextRef malformed-reference admission."""
from __future__ import annotations

from dataclasses import dataclass

from src.elo.agent_intake.hermes_context_reference_functional_adapter import admit_message


@dataclass(frozen=True)
class ContextRefFunctionalEvaluation:
    baseline_safe_admission_rate: float
    adapted_safe_admission_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str
    provenance_refs: tuple[str, ...]


_CASES = (
    "@file:README.md:10-20",
    "@file:README.md:20-10",
    "@file:README.md:0-4",
    "@folder:src/elo",
    "@url:https://example.invalid/doc",
)


def _naive_admit(message: str) -> bool:
    return bool(message)


def evaluate() -> ContextRefFunctionalEvaluation:
    baseline = sum(_naive_admit(m) for m in _CASES) / len(_CASES)
    adapted_admissions = tuple(admit_message(m) for m in _CASES)
    adapted = sum(all(item.accepted for item in admissions) for admissions in adapted_admissions) / len(_CASES)
    # Candidate must reject only malformed references and preserve valid ones.
    boundary = sum(
        all(item.reason != "empty_target" for item in admissions)
        for admissions in adapted_admissions
    ) / len(_CASES)
    expected = (True, False, False, True, True)
    actual = tuple(all(item.accepted for item in admissions) for admissions in adapted_admissions)
    repeatable = actual == expected and evaluate_once() == expected
    result = "EVOLUTION_GATE_REQUIRED" if adapted < baseline and repeatable and boundary == 1.0 else "RETEST"
    return ContextRefFunctionalEvaluation(
        baseline_safe_admission_rate=baseline,
        adapted_safe_admission_rate=adapted,
        boundary_integrity_rate=boundary,
        repeatable=repeatable,
        result=result,
        provenance_refs=(
            "controlled-eval:contextref/malformed-boundary/valid-range",
            "controlled-eval:contextref/malformed-boundary/reversed-range",
            "controlled-eval:contextref/malformed-boundary/zero-range",
        ),
    )


def evaluate_once() -> tuple[bool, ...]:
    return tuple(
        all(item.accepted for item in admit_message(message))
        for message in _CASES
    )
