"""Bounded ELO cognitive loop over canonical context and scenario diagnostics.

This module coordinates the existing canonical contracts. It does not execute
enterprise actions, create a parallel reasoning engine, or mutate evidence.
"""

from dataclasses import dataclass, field
from typing import Mapping

from elo.agent_intake.elo_flow_cadence import CadenceOutcome
from elo.agent_intake.flow_complementarity import RelationKind
from elo.agent_intake.governed_flow_router import GovernedFlowRouter, NextFlowResolution

from .context_resolution import ContextPack
from .diagnostic_scenarios import (
    DiagnosticObservation,
    DiagnosticScenario,
    DiagnosticScenarioEngine,
    DiagnosticStatus,
)


@dataclass(frozen=True)
class CoreLoopRequest:
    context: ContextPack
    scenario: DiagnosticScenario
    observations: tuple[DiagnosticObservation, ...] = ()
    minimum_confidence: float = 0.7
    flow_origin: str | None = None
    flow_outcome: CadenceOutcome | None = None
    flow_relation_kind: RelationKind | None = None
    flow_evidence: Mapping[str, object] = field(default_factory=dict)
    flow_provenance_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class CoreLoopResult:
    scenario_id: str
    status: str
    evidence_ids: tuple[str, ...]
    diagnostic_modes: tuple[str, ...]
    covered_lenses: tuple[str, ...]
    confidence: float
    recommendation: str | None = None
    handoff_required: bool = False
    gaps: tuple[str, ...] = ()
    metadata: Mapping[str, str] = ()
    next_flow: str | None = None
    flow_routing_status: str | None = None

    @property
    def can_execute(self) -> bool:
        return False


class CoreLoopEngine:
    """Canonical coordinator for Context → Evidence → Diagnosis → Handoff."""

    def __init__(
        self,
        scenario_engine: DiagnosticScenarioEngine | None = None,
        flow_router: GovernedFlowRouter | None = None,
    ) -> None:
        self._scenario = scenario_engine or DiagnosticScenarioEngine()
        self._flow_router = flow_router

    def run(self, request: CoreLoopRequest) -> CoreLoopResult:
        if not 0.0 <= request.minimum_confidence <= 1.0:
            raise ValueError("minimum_confidence must be between 0 and 1")

        context_gaps = request.context.integrity_gaps()
        scoped_evidence = request.context.scoped_evidence()
        evidence_ids = tuple(dict.fromkeys(item.source_id for item in scoped_evidence))
        observations = tuple(request.observations)

        if not observations:
            return CoreLoopResult(
                scenario_id=request.scenario.scenario_id,
                status="BLOCKED",
                evidence_ids=evidence_ids,
                diagnostic_modes=(),
                covered_lenses=(),
                confidence=0.0,
                handoff_required=True,
                gaps=tuple(dict.fromkeys(context_gaps + ("no diagnostic evidence supplied",))),
            )

        report = self._scenario.diagnose(
            request.scenario.scenario_id,
            observations,
        )
        scenario = DiagnosticScenario(
            scenario_id=request.scenario.scenario_id,
            question=request.scenario.question,
            observations=observations,
        )
        conflicts = scenario.has_conflict()
        blocked = scenario.is_blocked()
        confidence = scenario.evidence_quality()
        lenses = tuple(dict.fromkeys(item.lens.value for item in observations if item.lens is not None))
        report_evidence = tuple(dict.fromkeys(
            evidence_id
            for finding in report.findings
            for evidence_id in finding.evidence_ids
        ))
        all_evidence = tuple(dict.fromkeys(evidence_ids + report_evidence))
        gaps = tuple(dict.fromkeys(
            context_gaps
            + report.uncertainties
            + (("conflicting specialist evidence",) if conflicts else ())
            + (("blocked evidence or governance condition",) if blocked else ())
        ))
        handoff = bool(gaps) or confidence < request.minimum_confidence
        if confidence < request.minimum_confidence:
            gaps = tuple(dict.fromkeys(gaps + ("diagnostic confidence below decision threshold",)))

        routing: NextFlowResolution | None = None
        if request.flow_origin is not None or request.flow_outcome is not None:
            if handoff:
                # A blocked/conflicted/low-confidence Core Loop must not emit a
                # next-flow recommendation, even when an independent relation
                # appears eligible. The diagnostic gate remains authoritative.
                gaps = tuple(dict.fromkeys(
                    gaps + ("next flow withheld by core-loop diagnostic gate",)
                ))
            elif self._flow_router is None or request.flow_origin is None or request.flow_outcome is None:
                gaps = tuple(dict.fromkeys(gaps + ("flow routing contract is incomplete",)))
                handoff = True
            else:
                routing = self._flow_router.resolve_next(
                    origin_flow=request.flow_origin,
                    outcome=request.flow_outcome,
                    evidence=request.flow_evidence,
                    provenance_refs=request.flow_provenance_refs,
                    relation_kind=request.flow_relation_kind,
                )
                if routing.status != "ELIGIBLE":
                    gaps = tuple(dict.fromkeys(gaps + (
                        f"next flow routing status: {routing.status}",
                    )))
                    handoff = True

        status = "HANDOFF" if handoff else "RECOMMENDATION"
        return CoreLoopResult(
            scenario_id=request.scenario.scenario_id,
            status=status,
            evidence_ids=all_evidence,
            diagnostic_modes=tuple(mode.value for mode in report.modes_with_findings()),
            covered_lenses=lenses,
            confidence=confidence,
            recommendation=None if handoff else "reconcile diagnostic findings before any authorized action",
            handoff_required=handoff,
            gaps=gaps,
            next_flow=routing.selected_next if routing else None,
            flow_routing_status=routing.status if routing else None,
        )
