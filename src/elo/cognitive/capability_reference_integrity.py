"""Read-only capability-reference integrity reasoning for the ELO Symbiont."""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.system_health_assessment import HealthSeverity, SystemHealthFinding


@dataclass(frozen=True, slots=True)
class CapabilityReferenceSignal:
    capability_code: str
    reference_count: int
    object_count: int
    exists_in_catalog: bool
    active_in_catalog: bool
    evidence_ref: str = "supabase/health/elo_capability_reference_integrity.sql"

    def __post_init__(self) -> None:
        if not self.capability_code.strip():
            raise ValueError("capability_code is required")
        if self.reference_count < 0 or self.object_count < 0:
            raise ValueError("capability reference counts cannot be negative")
        if self.object_count > self.reference_count:
            raise ValueError("object_count cannot exceed reference_count")
        if self.active_in_catalog and not self.exists_in_catalog:
            raise ValueError("an active capability must exist in the catalog")
        if not self.evidence_ref.strip():
            raise ValueError("evidence_ref is required")


def assess_capability_reference_integrity(
    signal: CapabilityReferenceSignal,
) -> SystemHealthFinding:
    """Return PASS for active catalog references, REVIEW otherwise.

    REVIEW deliberately does not imply CREATE, assignment, role binding, or
    authorization. The canonical owner must decide whether the reference is
    legacy debt, a typo, or a missing governed capability.
    """
    healthy = signal.exists_in_catalog and signal.active_in_catalog
    return SystemHealthFinding(
        finding_id=f"AUTHZ_CAPABILITY_REFERENCE_{signal.capability_code}",
        dimension="authorization",
        severity=HealthSeverity.PASS if healthy else HealthSeverity.REVIEW,
        weight=2.0,
        evidence_refs=(signal.evidence_ref,),
        detail=(
            f"capability={signal.capability_code} references={signal.reference_count} "
            f"objects={signal.object_count} exists_in_catalog={signal.exists_in_catalog} "
            f"active_in_catalog={signal.active_in_catalog}"
        ),
        owner="elo-authz",
    )


__all__ = [
    "CapabilityReferenceSignal",
    "assess_capability_reference_integrity",
]
