"""Controlled evaluation of Hermes context-reference parsing boundary."""
from __future__ import annotations
from dataclasses import dataclass
from src.elo.core.context_references import parse_context_references

@dataclass(frozen=True)
class ContextReferenceEvaluation:
    baseline_rate: float
    adapted_rate: float
    boundary_integrity_rate: float
    repeatable: bool
    result: str

_CASES = (
    "@file:README.md",
    "@folder:src/elo",
    "@diff",
    "@staged",
    "@git:HEAD",
    "@url:https://example.invalid/doc",
)

def _rate(messages):
    return sum(bool(parse_context_references(m)) for m in messages) / len(messages)

def _integrity(messages):
    refs = tuple(r for m in messages for r in parse_context_references(m))
    return sum(
        r.owner in {"artifact_resolver", "source_discovery"}
        and (r.required_capability in {None, "source.github.read", "source.web.read"})
        for r in refs
    ) / len(refs)

def evaluate():
    baseline = _CASES
    adapted = _CASES
    b = _rate(baseline)
    a = _rate(adapted)
    i = _integrity(adapted)
    repeatable = _rate(_CASES) == a and i == 1.0
    result = "EVOLUTION_GATE_REQUIRED" if a > b and repeatable else "RETEST"
    return ContextReferenceEvaluation(b, a, i, repeatable, result)
