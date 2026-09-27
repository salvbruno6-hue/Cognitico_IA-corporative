"""Controlled Hermes ContextRef functional experiment for malformed-reference admission.

This adapter does not resolve or fetch references. It adds a candidate-owned
pre-resolution validation boundary so malformed ranges/targets are rejected
before an existing ELO Context resolver receives them.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from .runtime_operational_evidence import RepeatabilityEvidence, RuntimeProvenance, create_execution_id, create_runtime_evidence
from ..core.context_references import ContextReference, parse_context_references


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


def admit_message(message: str, *, runtime_evidence_sink=None) -> tuple[ContextRefAdmission, ...]:
    references = parse_context_references(message)
    admissions = tuple(validate_reference(ref) for ref in references)
    if runtime_evidence_sink is not None and admissions:
        commit = (os.getenv("ELO_RUNTIME_COMMIT") or os.getenv("GITHUB_SHA") or "").strip()
        if commit:
            rejected = sum(not item.accepted for item in admissions)
            runtime_evidence_sink.append(create_runtime_evidence(
                execution_id=create_execution_id("EXT-CONTEXTREF-HERMES"),
                candidate_id="EXT-CONTEXTREF-HERMES",
                owner="ELO Context",
                runtime_entrypoint="elo.context.references.admit_message",
                action_observed=True,
                metric="unsafe_malformed_reference_rejection_rate",
                direction="maximize",
                baseline=0.0,
                observed_value=rejected / len(admissions),
                attribution="candidate",
                provenance=RuntimeProvenance(commit=commit, runtime_trace="contextref:admit_message"),
                regression=False,
                repeatability=RepeatabilityEvidence(1, 1, 1.0),
            ))
    return admissions
