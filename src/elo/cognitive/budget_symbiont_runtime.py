"""Governed runtime bridge for the Budget Intelligence POC.

The runtime is deliberately evolution-oriented: a successful execution is not
considered an architectural improvement by itself. Each implementation must
carry measurable comparative evidence before entering governed learning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from elo.core.budgeting import BudgetInput, BudgetLine, BudgetRequest, BudgetVersion, GovernedBudgetingService
from elo.cognitive.routing.execution_routing import ExecutionRouter, RoutingDecision
from elo.cognitive.routing.model_selection import ModelCandidate
from elo.cognitive.routing.tool_selection import ToolCandidate
from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabEvaluation, SymbiontLabObservation


@dataclass(frozen=True, slots=True)
class ProviderResult:
    provider_id: str
    model_id: str | None
    result: str
    evidence_ids: tuple[str, ...]
    provenance: dict[str, str]


class GovernedProvider(Protocol):
    def execute(self, *, request: BudgetRequest, route: RoutingDecision, context: str) -> ProviderResult: ...


@dataclass(frozen=True, slots=True)
class IntelligenceExecution:
    route: RoutingDecision
    provider_result: ProviderResult


@dataclass(frozen=True, slots=True)
class EvolutionImpact:
    """Comparative evidence for a material improvement claim.

    Numeric scores are measurements supplied by the caller; they are never
    treated as self-authenticating evidence. The measurement must be tied to
    explicit evidence references, a reproducible comparison, and regression
    status. Generalization is a separate claim and is never inferred from the
    score delta alone.
    """

    baseline_score: float
    observed_score: float
    minimum_delta: float = 0.10
    evidence_confidence: float = 0.0
    comparative_runs: int = 0
    regression_free: bool = False
    generalization_supported: bool = False
    measurement_evidence_ids: tuple[str, ...] = ()
    baseline_ref: str = ""
    comparison_ref: str = ""

    @property
    def delta(self) -> float:
        return self.observed_score - self.baseline_score

    @property
    def material(self) -> bool:
        return (
            self.delta >= self.minimum_delta
            and self.evidence_confidence >= 0.70
            and self.comparative_runs >= 2
            and self.regression_free
            and bool(self.measurement_evidence_ids)
            and bool(self.baseline_ref)
            and bool(self.comparison_ref)
        )

    def validate(self) -> None:
        if not 0.0 <= self.baseline_score <= 1.0:
            raise ValueError("baseline score must be between 0 and 1")
        if not 0.0 <= self.observed_score <= 1.0:
            raise ValueError("observed score must be between 0 and 1")
        if self.minimum_delta <= 0:
            raise ValueError("minimum evolution delta must be positive")
        if not 0.0 <= self.evidence_confidence <= 1.0:
            raise ValueError("evidence confidence must be between 0 and 1")
        if self.comparative_runs < 2:
            raise ValueError("material evolution requires comparative runs")
        if not self.measurement_evidence_ids:
            raise ValueError("material evolution requires measurement evidence")
        if not self.baseline_ref or not self.comparison_ref:
            raise ValueError("material evolution requires reconstructible comparison references")
        if not self.regression_free:
            raise ValueError("regression blocks material evolution")
        if not self.material:
            raise ValueError("implementation does not demonstrate material evolution")


class IntelligenceRouter:
    """Subordinate execution coordinator; it never selects the route."""

    def execute(self, *, route: RoutingDecision, provider: GovernedProvider, request: BudgetRequest, context: str) -> IntelligenceExecution:
        if not route.model_id and not route.tool_id:
            raise ValueError("intelligence execution requires a route selected by ExecutionRouter")
        result = provider.execute(request=request, route=route, context=context)
        if not result.provider_id or not result.provenance:
            raise ValueError("provider result requires identity and provenance")
        if not result.evidence_ids:
            raise ValueError("provider result requires evidence")
        return IntelligenceExecution(route=route, provider_result=result)


@dataclass(frozen=True, slots=True)
class BudgetSymbiontRun:
    request: BudgetRequest
    budget: BudgetVersion
    intelligence: IntelligenceExecution
    evolution_impact: EvolutionImpact
    laboratory: SymbiontLabEvaluation


class BudgetSymbiontRuntime:
    """First executable Budget → Symbiont → governed-learning bridge."""

    def __init__(self, *, budgeting: GovernedBudgetingService, execution_router: ExecutionRouter, intelligence_router: IntelligenceRouter, laboratory: SymbiontLabAdapter) -> None:
        self.budgeting = budgeting
        self.execution_router = execution_router
        self.intelligence_router = intelligence_router
        self.laboratory = laboratory

    def run(
        self,
        *,
        request: BudgetRequest,
        inputs: Sequence[BudgetInput],
        lines: Sequence[BudgetLine],
        capability: str,
        models: Sequence[ModelCandidate],
        tools: Sequence[ToolCandidate],
        provider: GovernedProvider,
        context: str,
        principal_id: str,
        dataset_version: str,
        hypothesis: str,
        expected_outcome: str,
        evolution_impact: EvolutionImpact,
    ) -> BudgetSymbiontRun:
        # The runtime accepts only a materially evidenced improvement claim.
        evolution_impact.validate()

        budget = self.budgeting.calculate(request, inputs=inputs, lines=lines)
        if not budget.evidence_ids or not budget.provenance:
            raise ValueError("budget result must preserve evidence and provenance")

        # The only component allowed to choose model/tool is ExecutionRouter.
        route = self.execution_router.route(capability, models=list(models), tools=list(tools))
        intelligence = self.intelligence_router.execute(route=route, provider=provider, request=request, context=context)

        evidence_ids = tuple(dict.fromkeys((*budget.evidence_ids, *intelligence.provider_result.evidence_ids, *evolution_impact.measurement_evidence_ids)))
        provenance = dict(intelligence.provider_result.provenance)
        provenance.update({
            "budget_version": budget.version_id,
            "formula_version": budget.formula_version,
            "evolution_baseline_score": str(evolution_impact.baseline_score),
            "evolution_observed_score": str(evolution_impact.observed_score),
            "evolution_delta": str(evolution_impact.delta),
            "evolution_evidence_confidence": str(evolution_impact.evidence_confidence),
            "evolution_comparative_runs": str(evolution_impact.comparative_runs),
            "evolution_regression_free": str(evolution_impact.regression_free),
            "evolution_generalization_supported": str(evolution_impact.generalization_supported),
            "evolution_baseline_ref": evolution_impact.baseline_ref,
            "evolution_comparison_ref": evolution_impact.comparison_ref,
        })
        observed = intelligence.provider_result.result
        observation = SymbiontLabObservation(
            observation_id=f"budget-run:{request.request_id}:{budget.version_id}",
            tenant_id=request.tenant_id,
            domain=request.domain,
            decision_id=f"budget-decision:{budget.version_id}",
            expected_outcome=expected_outcome,
            observed_outcome=observed,
            evidence_ids=evidence_ids,
            source_ref=intelligence.provider_result.provider_id,
            source_commit=provenance.get("source_commit", "runtime"),
            hypothesis=(
                f"{hypothesis}; material_delta={evolution_impact.delta:.3f}; "
                f"confidence={evolution_impact.evidence_confidence:.2f}; "
                f"comparative_runs={evolution_impact.comparative_runs}"
            ),
            baseline=(
                f"budget_status={budget.status.value};version={budget.version_id};"
                f"score={evolution_impact.baseline_score};ref={evolution_impact.baseline_ref}"
            ),
            experiment=(
                f"capability={capability};model={route.model_id};tool={route.tool_id};"
                f"observed_score={evolution_impact.observed_score};ref={evolution_impact.comparison_ref}"
            ),
            result=observed,
            regression_status="PASS" if evolution_impact.regression_free else "FAIL",
            generalization_status="CONFIRMED" if evolution_impact.generalization_supported else "UNCONFIRMED",
            risk="LOW",
            existing_owner=None,
            scope=request.domain,
            tenant_scope=request.tenant_id,
            source_kind="runtime",
        )
        laboratory = self.laboratory.evaluate(observation, principal_id=principal_id, dataset_version=dataset_version)
        return BudgetSymbiontRun(request=request, budget=budget, intelligence=intelligence, evolution_impact=evolution_impact, laboratory=laboratory)
