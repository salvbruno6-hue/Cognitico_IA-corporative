"""Canonical Core-owned capability resolution.

The application does not choose an operational capability. Core resolves a
capability only from a condition already produced by cognitive analysis,
reusing the existing governed conditional-pointer matrix. Unresolved or
ambiguous conditions remain unresolved and cannot reach operational runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.agent_intake.conditional_pointer import ConditionalPointerEvidence, resolve_pointer


@dataclass(frozen=True, slots=True)
class CoreCapabilityDecision:
    """Capability decision emitted by Core after cognitive analysis."""

    request_id: str
    tenant_scope: str
    condition: str
    capability_id: str | None
    destination: str | None
    status: str
    evidence: tuple[dict[str, Any], ...]
    rationale: str

    @property
    def executable(self) -> bool:
        return self.status == "resolved" and bool(self.capability_id)


def resolve_capability(
    *,
    request_id: str,
    tenant_scope: str,
    condition: str,
    analysis_evidence: tuple[str, ...] = (),
) -> CoreCapabilityDecision:
    """Resolve the operational capability from a Core-owned analysis condition."""
    pointer: ConditionalPointerEvidence = resolve_pointer(
        request_id=request_id,
        tenant_scope=tenant_scope,
        information={
            "condition": condition,
            "source": "elo-core-analysis",
            "analysis_evidence": tuple(analysis_evidence),
        },
    )
    return CoreCapabilityDecision(
        request_id=request_id,
        tenant_scope=tenant_scope,
        condition=pointer.condition,
        capability_id=pointer.matched_capability,
        destination=pointer.destination,
        status=pointer.status,
        evidence=pointer.evidence,
        rationale=(
            "Core resolved capability from the governed conditional-pointer matrix"
            if pointer.status == "resolved"
            else "Core could not resolve a capability from the analyzed condition"
        ),
    )


__all__ = ["CoreCapabilityDecision", "resolve_capability"]
