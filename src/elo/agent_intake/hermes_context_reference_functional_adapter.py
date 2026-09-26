"""Controlled Hermes ContextRef functional experiment for malformed-reference admission.

This adapter does not resolve or fetch references. It adds a candidate-owned
pre-resolution validation boundary so malformed ranges/targets are rejected
before an existing ELO Context resolver receives them.
"""
from __future__ import annotations

from dataclasses import dataclass
from src.elo.core.context_references import ContextReference, parse_context_references


@dataclass(frozen=True)
class ContextRefAdmission:
    accepted: bool
    reason: str


def validate_reference(ref: ContextReference) -> ContextRefAdmission:
    if not ref.target and ref.kind in {"file", "folder", "git", "url"}:
        return ContextRefAdmission(False, "empty_target")
    if ref.line_start is not None and ref.line_start < 1:
        return ContextRefAdmission(False, "invalid_line_start")
    if ref.line_end is not None and ref.line_end < 1:
        return ContextRefAdmission(False, "invalid_line_end")
    if (
        ref.line_start is not None
        and ref.line_end is not None
        and ref.line_end < ref.line_start
    ):
        return ContextRefAdmission(False, "reversed_line_range")
    return ContextRefAdmission(True, "accepted")


def admit_message(message: str) -> tuple[ContextRefAdmission, ...]:
    return tuple(validate_reference(ref) for ref in parse_context_references(message))
