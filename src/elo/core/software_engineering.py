"""Native, provider-neutral self-correcting software engineering boundary."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class SoftwareEngineeringError(ValueError):
    """Raised when an engineering cycle is incomplete or unsafe."""


@dataclass(frozen=True)
class EngineeringCycle:
    cycle_id: str
    tenant_id: str
    target: str
    diagnosis: str
    root_cause: str
    hypothesis: str
    proposed_change: str
    evidence_ids: tuple[str, ...]
    provenance: Mapping[str, str]
    reproduction_evidence_ids: tuple[str, ...] = ()
    regression_test_ids: tuple[str, ...] = ()
    validation_evidence_ids: tuple[str, ...] = ()
    state: str = "LAB_CANDIDATE"


class NativeSoftwareEngineering:
    """Prepare a reproducible diagnose→patch→test cycle without mutating main."""

    _SECRET_KEYS = {"password", "token", "access_token", "refresh_token", "api_key", "service_role"}

    def prepare_cycle(
        self, *, cycle_id: str, tenant_id: str, target: str, diagnosis: str,
        root_cause: str, hypothesis: str, proposed_change: str,
        evidence_ids: tuple[str, ...] | list[str], provenance: Mapping[str, str],
        reproduction_evidence_ids: tuple[str, ...] | list[str],
        regression_test_ids: tuple[str, ...] | list[str],
    ) -> EngineeringCycle:
        values = (cycle_id, tenant_id, target, diagnosis, root_cause, hypothesis, proposed_change)
        if any(not str(v).strip() for v in values):
            raise SoftwareEngineeringError("cycle identity and diagnostic fields are required")
        if not evidence_ids:
            raise SoftwareEngineeringError("reproducible evidence is required")
        if not reproduction_evidence_ids:
            raise SoftwareEngineeringError("bug reproduction evidence is required")
        if not regression_test_ids:
            raise SoftwareEngineeringError("regression test evidence is required")
        if not provenance.get("source_ref") or not provenance.get("source_commit"):
            raise SoftwareEngineeringError("provenance requires source_ref and source_commit")
        if any(key.lower() in self._SECRET_KEYS for key in provenance):
            raise SoftwareEngineeringError("secret-bearing provenance is forbidden")
        return EngineeringCycle(
            cycle_id=cycle_id.strip(), tenant_id=tenant_id.strip(), target=target.strip(),
            diagnosis=diagnosis.strip(), root_cause=root_cause.strip(), hypothesis=hypothesis.strip(),
            proposed_change=proposed_change.strip(), evidence_ids=tuple(evidence_ids),
            provenance=dict(provenance),
            reproduction_evidence_ids=tuple(reproduction_evidence_ids),
            regression_test_ids=tuple(regression_test_ids),
        )

    @staticmethod
    def advance(
        *,
        cycle: EngineeringCycle,
        tests_passed: bool,
        regression_passed: bool,
        validation_evidence_ids: tuple[str, ...] | list[str] = (),
    ) -> EngineeringCycle:
        if not cycle.reproduction_evidence_ids:
            raise SoftwareEngineeringError("governance requires bug reproduction evidence")
        if not cycle.regression_test_ids:
            raise SoftwareEngineeringError("governance requires a regression test")
        if not tests_passed:
            return EngineeringCycle(**{**cycle.__dict__, "state": "ADJUST_REQUIRED"})
        if not regression_passed:
            return EngineeringCycle(**{**cycle.__dict__, "state": "REGRESSION_FAILED"})
        if not validation_evidence_ids:
            raise SoftwareEngineeringError("governance requires validation evidence after retest")
        return EngineeringCycle(**{
            **cycle.__dict__,
            "validation_evidence_ids": tuple(validation_evidence_ids),
            "state": "READY_FOR_GOVERNANCE",
        })
