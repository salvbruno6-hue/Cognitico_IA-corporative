"""Governance read views for Symbiont implementation-loop boundaries.

The view is a read model, not an authority. A start view is emitted when a
Symbiont implementation loop begins and a completion view is emitted when the
loop returns a decision. Neither view mutates canonical state, approves
promotion, performs deployment, or replaces Evolution Gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ImplementationViewPhase(str, Enum):
    START = "START"
    END = "END"


class ImplementationOwnership(str, Enum):
    CANONICAL = "CANONICAL"
    EXTENSION = "EXTENSION"
    INTEGRATION = "INTEGRATION"
    EXISTING_BUT_UNWIRED = "EXISTING_BUT_UNWIRED"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"
    DUPLICATE = "DUPLICATE"
    CONFLICT = "CONFLICT"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True, slots=True)
class SymbiontImplementationView:
    implementation_id: str
    phase: ImplementationViewPhase
    candidate_id: str
    owner: str
    functional_branch: str
    capability: str
    specialization: str | None
    ownership: ImplementationOwnership
    source_ref: str
    source_commit: str
    related_contracts: tuple[str, ...]
    dependencies: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    environment: str
    loop_stage: str
    loop_result: str | None
    canonical_mutation: bool
    evolution_gate_status: str
    governance_status: str
    runtime_status: str
    view_version: str = "1"

    def as_dict(self) -> dict[str, object]:
        return {
            "implementation_id": self.implementation_id,
            "phase": self.phase.value,
            "candidate_id": self.candidate_id,
            "owner": self.owner,
            "functional_branch": self.functional_branch,
            "capability": self.capability,
            "specialization": self.specialization,
            "ownership": self.ownership.value,
            "source_ref": self.source_ref,
            "source_commit": self.source_commit,
            "related_contracts": list(self.related_contracts),
            "dependencies": list(self.dependencies),
            "evidence_refs": list(self.evidence_refs),
            "environment": self.environment,
            "loop_stage": self.loop_stage,
            "loop_result": self.loop_result,
            "canonical_mutation": self.canonical_mutation,
            "evolution_gate_status": self.evolution_gate_status,
            "governance_status": self.governance_status,
            "runtime_status": self.runtime_status,
            "view_version": self.view_version,
        }


def _require_text(value: str, field: str) -> str:
    if not value.strip():
        raise ValueError(f"{field} must not be blank")
    return value


def create_implementation_view(
    *,
    implementation_id: str,
    phase: ImplementationViewPhase,
    candidate_id: str,
    owner: str,
    functional_branch: str,
    capability: str,
    source_ref: str,
    source_commit: str,
    loop_stage: str,
    specialization: str | None = None,
    ownership: ImplementationOwnership = ImplementationOwnership.UNRESOLVED,
    related_contracts: tuple[str, ...] = (),
    dependencies: tuple[str, ...] = (),
    evidence_refs: tuple[str, ...] = (),
    environment: str = "CONTROLLED_TEST",
    loop_result: str | None = None,
    canonical_mutation: bool = False,
    evolution_gate_status: str = "NOT_EVALUATED",
    governance_status: str = "NOT_EVALUATED",
    runtime_status: str = "NOT_DEPLOYED",
) -> SymbiontImplementationView:
    """Create a deterministic governance read view for one loop boundary."""
    for value, field in (
        (implementation_id, "implementation_id"),
        (candidate_id, "candidate_id"),
        (owner, "owner"),
        (functional_branch, "functional_branch"),
        (capability, "capability"),
        (source_ref, "source_ref"),
        (source_commit, "source_commit"),
        (loop_stage, "loop_stage"),
        (environment, "environment"),
    ):
        _require_text(value, field)

    if canonical_mutation:
        raise ValueError("implementation view cannot authorize canonical mutation")

    return SymbiontImplementationView(
        implementation_id=implementation_id,
        phase=phase,
        candidate_id=candidate_id,
        owner=owner,
        functional_branch=functional_branch,
        capability=capability,
        specialization=specialization,
        ownership=ownership,
        source_ref=source_ref,
        source_commit=source_commit,
        related_contracts=tuple(related_contracts),
        dependencies=tuple(dependencies),
        evidence_refs=tuple(evidence_refs),
        environment=environment,
        loop_stage=loop_stage,
        loop_result=loop_result,
        canonical_mutation=False,
        evolution_gate_status=evolution_gate_status,
        governance_status=governance_status,
        runtime_status=runtime_status,
    )


def create_loop_views(
    *,
    implementation_id: str,
    candidate_id: str,
    owner: str,
    functional_branch: str,
    capability: str,
    source_ref: str,
    source_commit: str,
    end_stage: str,
    end_result: str | None,
    specialization: str | None = None,
    ownership: ImplementationOwnership = ImplementationOwnership.UNRESOLVED,
    related_contracts: tuple[str, ...] = (),
    dependencies: tuple[str, ...] = (),
    evidence_refs: tuple[str, ...] = (),
    environment: str = "CONTROLLED_TEST",
    evolution_gate_status: str = "NOT_EVALUATED",
    governance_status: str = "NOT_EVALUATED",
    runtime_status: str = "NOT_DEPLOYED",
) -> tuple[SymbiontImplementationView, SymbiontImplementationView]:
    """Create the mandatory START and END views for one implementation loop."""
    start = create_implementation_view(
        implementation_id=implementation_id,
        phase=ImplementationViewPhase.START,
        candidate_id=candidate_id,
        owner=owner,
        functional_branch=functional_branch,
        capability=capability,
        source_ref=source_ref,
        source_commit=source_commit,
        loop_stage="OBSERVED",
        specialization=specialization,
        ownership=ownership,
        related_contracts=related_contracts,
        dependencies=dependencies,
        evidence_refs=evidence_refs,
        environment=environment,
        evolution_gate_status=evolution_gate_status,
        governance_status=governance_status,
        runtime_status=runtime_status,
    )
    end = create_implementation_view(
        implementation_id=implementation_id,
        phase=ImplementationViewPhase.END,
        candidate_id=candidate_id,
        owner=owner,
        functional_branch=functional_branch,
        capability=capability,
        source_ref=source_ref,
        source_commit=source_commit,
        loop_stage=end_stage,
        specialization=specialization,
        ownership=ownership,
        related_contracts=related_contracts,
        dependencies=dependencies,
        evidence_refs=evidence_refs,
        environment=environment,
        loop_result=end_result,
        evolution_gate_status=evolution_gate_status,
        governance_status=governance_status,
        runtime_status=runtime_status,
    )
    return start, end


__all__ = [
    "ImplementationOwnership",
    "ImplementationViewPhase",
    "SymbiontImplementationView",
    "create_implementation_view",
    "create_loop_views",
]
