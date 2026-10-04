"""Read-only global capability visibility over existing ELO authorities.

This extends the Symbiont governance read model. It does not create a second
registry, graph, selector, router, execution authority or Evolution Gate.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping, Sequence

from elo.agent_intake.implementation_loop_readiness import LoopReadiness
from elo.agent_intake.symbiont_implementation_view import SymbiontImplementationView
from elo.cognitive.symbiont_capability_evolution import (
    CapabilityEvolutionReview,
    CapabilityStatusReport,
)
from elo.core.capability_registry import CapabilitySnapshot


class CapabilityVisibilityState(StrEnum):
    REGISTERED_VISIBLE = "REGISTERED_VISIBLE"
    EXISTING_BUT_UNWIRED = "EXISTING_BUT_UNWIRED"
    IMPLEMENTED_NOT_REGISTERED = "IMPLEMENTED_NOT_REGISTERED"
    REGISTERED_WITHOUT_IMPLEMENTATION_VIEW = "REGISTERED_WITHOUT_IMPLEMENTATION_VIEW"
    UNRESOLVED_OWNER = "UNRESOLVED_OWNER"


@dataclass(frozen=True, slots=True)
class GovernanceRelation:
    source: str
    relation: str
    target: str
    authority: str
    evidence_refs: tuple[str, ...] = ()
    condition: str = ""


@dataclass(frozen=True, slots=True)
class CapabilityVisibilityRecord:
    capability_id: str
    registry_visible: bool
    available: bool
    implementation_visible: bool
    owner: str | None
    consumer: str | None = None
    canonical_route: str | None = None
    execution_boundary: str | None = None
    runtime_status: str | None
    evolution_status: str | None
    evidence_refs: tuple[str, ...]
    state: CapabilityVisibilityState


@dataclass(frozen=True, slots=True)
class GlobalCapabilityVisibility:
    records: tuple[CapabilityVisibilityRecord, ...]
    blockers: tuple[str, ...] = ()
    canonical_mutation: bool = False

    @property
    def capability_count(self) -> int:
        return len(self.records)

    @property
    def isolated(self) -> tuple[CapabilityVisibilityRecord, ...]:
        return tuple(
            record
            for record in self.records
            if record.state
            in {
                CapabilityVisibilityState.EXISTING_BUT_UNWIRED,
                CapabilityVisibilityState.IMPLEMENTED_NOT_REGISTERED,
                CapabilityVisibilityState.REGISTERED_WITHOUT_IMPLEMENTATION_VIEW,
                CapabilityVisibilityState.UNRESOLVED_OWNER,
            }
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "capability_count": self.capability_count,
            "records": [
                {
                    "capability_id": item.capability_id,
                    "registry_visible": item.registry_visible,
                    "available": item.available,
                    "implementation_visible": item.implementation_visible,
                    "owner": item.owner,
                    "consumer": item.consumer,
                    "canonical_route": item.canonical_route,
                    "execution_boundary": item.execution_boundary,
                    "runtime_status": item.runtime_status,
                    "evolution_status": item.evolution_status,
                    "evidence_refs": list(item.evidence_refs),
                    "state": item.state.value,
                }
                for item in self.records
            ],
            "blockers": list(self.blockers),
            "canonical_mutation": self.canonical_mutation,
        }


def build_global_capability_visibility(
    *,
    registry_snapshot: Sequence[CapabilitySnapshot],
    implementation_views: Sequence[SymbiontImplementationView] = (),
    declared_capabilities: Sequence[str] = (),
    consumers: Mapping[str, str] | None = None,
    canonical_routes: Mapping[str, str] | None = None,
    execution_boundaries: Mapping[str, str] | None = None,
) -> GlobalCapabilityVisibility:
    """Reconcile existing capability visibility without inferring runtime.

    Consumer, route and execution-boundary links are accepted only as explicit
    evidence supplied by the caller. File existence or registry visibility does
    not infer any of these relationships.
    """
    consumers = consumers or {}
    canonical_routes = canonical_routes or {}
    execution_boundaries = execution_boundaries or {}
    snapshots = {item.name: item for item in registry_snapshot}
    views_by_capability: dict[str, SymbiontImplementationView] = {}
    for view in implementation_views:
        views_by_capability.setdefault(view.capability, view)

    ids = set(declared_capabilities) | set(snapshots) | set(views_by_capability)
    records: list[CapabilityVisibilityRecord] = []
    for capability_id in sorted(item for item in ids if item):
        snapshot = snapshots.get(capability_id)
        view = views_by_capability.get(capability_id)
        registry_visible = snapshot is not None
        implementation_visible = view is not None
        evidence_refs = tuple(dict.fromkeys(view.evidence_refs if view else ()))
        owner = view.owner if view and view.owner.strip() else None

        if view is not None and view.ownership.value == "UNRESOLVED":
            state = CapabilityVisibilityState.UNRESOLVED_OWNER
        elif view is not None and snapshot is None:
            state = CapabilityVisibilityState.IMPLEMENTED_NOT_REGISTERED
        elif snapshot is not None and view is None:
            state = CapabilityVisibilityState.REGISTERED_WITHOUT_IMPLEMENTATION_VIEW
        elif snapshot is not None:
            state = CapabilityVisibilityState.REGISTERED_VISIBLE
        else:
            state = CapabilityVisibilityState.EXISTING_BUT_UNWIRED

        records.append(
            CapabilityVisibilityRecord(
                capability_id=capability_id,
                registry_visible=registry_visible,
                available=bool(snapshot and snapshot.status.value == "AVAILABLE"),
                implementation_visible=implementation_visible,
                owner=owner,
                consumer=consumers.get(capability_id),
                canonical_route=canonical_routes.get(capability_id),
                execution_boundary=execution_boundaries.get(capability_id),
                runtime_status=view.runtime_status if view else None,
                evolution_status=view.evolution_gate_status if view else None,
                evidence_refs=evidence_refs,
                state=state,
            )
        )

    blockers = tuple(
        f"{record.capability_id}:{record.state.value}"
        for record in records
        if record.state is not CapabilityVisibilityState.REGISTERED_VISIBLE
    )
    return GlobalCapabilityVisibility(records=tuple(records), blockers=blockers)


@dataclass(frozen=True, slots=True)
class SymbiontGovernanceOrchestration:
    capability_id: str
    status: str
    owner: str
    relations: tuple[GovernanceRelation, ...]
    blockers: tuple[str, ...]
    next_action: str
    canonical_mutation: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "capability_id": self.capability_id,
            "status": self.status,
            "owner": self.owner,
            "relations": [
                {
                    "source": relation.source,
                    "relation": relation.relation,
                    "target": relation.target,
                    "authority": relation.authority,
                    "evidence_refs": list(relation.evidence_refs),
                    "condition": relation.condition,
                }
                for relation in self.relations
            ],
            "blockers": list(self.blockers),
            "next_action": self.next_action,
            "canonical_mutation": self.canonical_mutation,
        }


def orchestrate_capability_governance(
    *,
    implementation_view: SymbiontImplementationView,
    readiness: LoopReadiness,
    evolution_review: CapabilityEvolutionReview,
    status_report: CapabilityStatusReport,
) -> SymbiontGovernanceOrchestration:
    """Expose the canonical resource-to-execution orchestration chain."""
    refs = tuple(dict.fromkeys(status_report.evidence_refs))
    capability = implementation_view.capability
    relations: list[GovernanceRelation] = [
        GovernanceRelation("SIMBIONTE", "DIAGNOSES", capability, "Symbiont read-model", refs, status_report.status.value),
        GovernanceRelation("Capability Registry", "EXPOSES", capability, "canonical capability discovery", refs, "resource visibility"),
        GovernanceRelation("Capability Selector", "SELECTS", capability, "canonical capability selection", refs, "available/evidenced capability required"),
        GovernanceRelation(capability, "OWNED_BY", implementation_view.owner, "canonical owner resolution", implementation_view.evidence_refs, implementation_view.ownership.value),
        GovernanceRelation(capability, "DESCRIBED_BY", "SymbiontImplementationView", "implementation governance contract", implementation_view.evidence_refs, implementation_view.loop_stage),
        GovernanceRelation("SymbiontImplementationView", "FEEDS", "LoopReadiness", "implementation readiness contract", implementation_view.evidence_refs, "ready_for_loop=" + str(readiness.ready_for_loop)),
        GovernanceRelation("LoopReadiness", "FEEDS", "CapabilityEvolutionReview", "existing implementation/evolution loop", readiness.missing, "ready_for_loop=" + str(readiness.ready_for_loop)),
        GovernanceRelation("CapabilityEvolutionReview", "OBSERVES", "EVOLUÇÃO_DE_CAPACIDADES", "existing capability evolution review", evolution_review.evidence_refs, evolution_review.status),
        GovernanceRelation("ExecutionRouter", "ROUTES", capability, "canonical model/tool routing", refs, "route only through existing routing authority"),
        GovernanceRelation("AgentOrchestrator", "DELEGATES", capability, "canonical specialist delegation", refs, "only for authorized agent task"),
        GovernanceRelation("ExecutionBoundary", "GOVERNS_EXECUTION", capability, "canonical execution boundary", refs, "authorization, correlation and evidence required"),
        GovernanceRelation("CapabilityEvolutionReview", "HANDOFF_TO", "Evolution Gate", "existing Evolution Gate", evolution_review.evidence_refs, "only when existing gate criteria are satisfied"),
        GovernanceRelation("Evolution Gate", "GOVERNS", "canonical promotion/merge decision", "existing Evolution Gate", (), "explicit authorization required"),
        GovernanceRelation("canonical runtime", "EMITS", "RuntimeOperationalEvidence", "existing runtime evidence boundary", (), status_report.status.value),
    ]
    blockers = (
        tuple(dict.fromkeys((*status_report.blockers, *(f"readiness:{item}" for item in readiness.missing))))
        if not readiness.ready_for_loop
        else status_report.blockers
    )
    return SymbiontGovernanceOrchestration(
        capability_id=status_report.capability_id,
        status=status_report.status.value,
        owner=implementation_view.owner,
        relations=tuple(relations),
        blockers=blockers,
        next_action=status_report.next_action,
        canonical_mutation=False,
    )


__all__ = [
    "CapabilityVisibilityState",
    "CapabilityVisibilityRecord",
    "GlobalCapabilityVisibility",
    "GovernanceRelation",
    "SymbiontGovernanceOrchestration",
    "build_global_capability_visibility",
    "orchestrate_capability_governance",
]
