"""Bounded ELO cognitive loop over canonical context and scenario diagnostics.

This module coordinates the existing canonical contracts. It does not execute
enterprise actions, create a parallel reasoning engine, or mutate evidence.
"""

from dataclasses import dataclass
from typing import Mapping

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

    @property
    def can_execute(self) -> bool:
        return False


class CoreLoopEngine:
    """Canonical coordinator for Context → Evidence → Diagnosis → Handoff."""

    def __init__(self, scenario_engine: DiagnosticScenarioEngine | None = None) -> None:
        self._scenario = scenario_engine or DiagnosticScenarioEngine()

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
        )
