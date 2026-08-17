from decimal import Decimal

import pytest

from elo.core.budgeting import (
    Assumption,
    BudgetAuthorization,
    BudgetAuthorizationError,
    BudgetInput,
    BudgetInputClass,
    BudgetLine,
    BudgetLineType,
    BudgetRequest,
    BudgetScenarioKind,
    BudgetSensitivity,
    BudgetScenario,
    BudgetStatus,
    CapacityConstraint,
    GovernedBudgetingService,
)
from elo.core.learning_governance import GovernedLearningService
from elo.memory.persistent import PersistentMemoryStore


TENANT = "multiteiner"
PRINCIPAL = "elo"
PROVENANCE = {"source_excerpt": "provided by exercise", "authority": "exercise"}


def request() -> BudgetRequest:
    return BudgetRequest(
        request_id="REQ-024",
        tenant_id=TENANT,
        principal_id=PRINCIPAL,
        domain="ORCAMENTO",
        period="2026-Q4",
        objective="prepare governed budget",
        scope="MT-001",
    )


def inp(name, value, classification=BudgetInputClass.FACT, *, unit="unit", source_id="SRC-1", tenant=TENANT, provenance=PROVENANCE):
    return BudgetInput.create(
        tenant_id=tenant,
        domain="ORCAMENTO",
        name=name,
        classification=classification,
        value=value,
        unit=unit,
        source_id=source_id,
        provenance=provenance,
    )


def line(quantity, cost, *, line_type=BudgetLineType.COST, formula_version="1.0"):
    return BudgetLine(
        line_id=f"L-{quantity.input_id[:6]}-{cost.input_id[:6]}",
        description="budget line",
        line_type=line_type,
        quantity_input_id=quantity.input_id,
        unit_cost_input_id=cost.input_id,
        formula_version=formula_version,
    )


def complete_budget():
    service = GovernedBudgetingService()
    quantity = inp("quantity", 10)
    cost = inp("unit cost", "25.50", unit="BRL/unit")
    revenue = inp("revenue unit", "40.00", unit="BRL/unit")
    revenue_quantity = inp("revenue quantity", 10)
    version = service.calculate(
        request(),
        inputs=(quantity, cost, revenue, revenue_quantity),
        lines=(line(quantity, cost), line(revenue_quantity, revenue, line_type=BudgetLineType.REVENUE)),
    )
    return service, version, quantity, cost


# B01 — complete inputs calculate reproducibly and version the result.
def test_complete_budget_is_reproducible_and_versioned():
    service, version, _, _ = complete_budget()
    assert version.status == BudgetStatus.COMPLETE
    assert version.total_cost == Decimal("255.00")
    assert version.total_revenue == Decimal("400.00")
    assert version.gross_margin == Decimal("145.00")
    assert version.is_reproducible
    assert version.version_number == 1
    assert service.versions("REQ-024") == (version,)


# B02 — missing critical input remains a gap and creates follow-up.
def test_missing_input_creates_gap_and_follow_up():
    service = GovernedBudgetingService()
    quantity = inp("quantity", None, BudgetInputClass.GAP)
    cost = inp("unit cost", 25, unit="BRL/unit")
    version = service.calculate(request(), inputs=(quantity, cost), lines=(line(quantity, cost),))
    assert version.status == BudgetStatus.CONDITIONAL
    assert version.total_cost is None
    assert version.follow_ups[0].state == "WAITING_FEEDBACK"
    assert "cannot be invented" in version.follow_ups[0].gap


# B03 — conflicting evidence is preserved, not silently selected.
def test_conflicting_source_is_not_silently_resolved():
    service = GovernedBudgetingService()
    quantity = inp("quantity", 10)
    cost = inp("unit cost", 25, BudgetInputClass.CONFLICT, unit="BRL/unit", source_id="SRC-A")
    version = service.calculate(request(), inputs=(quantity, cost), lines=(line(quantity, cost),))
    assert version.status == BudgetStatus.CONDITIONAL
    assert "conflicting evidence" in version.follow_ups[0].gap


# B04 — committed and available are distinct resource states.
def test_committed_is_not_available():
    service = GovernedBudgetingService()
    quantity = inp("committed quantity", 100, BudgetInputClass.COMMITTED)
    cost = inp("unit cost", 10, unit="BRL/unit")
    available = inp("available quantity", 20, BudgetInputClass.AVAILABLE)
    version = service.calculate(request(), inputs=(quantity, cost, available), lines=(line(quantity, cost),))
    assert version.inputs[0].classification == BudgetInputClass.COMMITTED
    assert version.inputs[2].classification == BudgetInputClass.AVAILABLE
    assert version.total_cost == Decimal("1000")
    assert version.inputs[0].value != version.inputs[2].value


# B05 — insufficient capacity produces a constrained result.
def test_insufficient_capacity_is_constrained():
    service = GovernedBudgetingService()
    quantity = inp("quantity", 100)
    cost = inp("unit cost", 10, unit="BRL/unit")
    constraint = CapacityConstraint(
        constraint_id="CAP-1",
        resource="assembly",
        required=Decimal("100"),
        available=Decimal("60"),
        unit="unit",
        source_id="PCP-1",
        provenance=PROVENANCE,
    )
    version = service.calculate(request(), inputs=(quantity, cost), lines=(line(quantity, cost),), capacity_constraints=(constraint,))
    assert version.status == BudgetStatus.CONSTRAINED
    assert version.total_cost is None
    assert any("capacity constraint" in follow_up.gap for follow_up in version.follow_ups)


# B06 — seasonal and recurring demand remain distinct inputs/domains.
def test_seasonal_and_recurring_demand_remain_distinct():
    service = GovernedBudgetingService()
    seasonal = inp("seasonal demand", 300, source_id="COMMERCIAL-SEASONAL")
    recurring = inp("recurring demand", 70, source_id="COMMERCIAL-RECURRING")
    version = service.calculate(request(), inputs=(seasonal, recurring), lines=())
    assert {item.name for item in version.inputs} == {"seasonal demand", "recurring demand"}
    assert {item.source_id for item in version.inputs} == {"COMMERCIAL-SEASONAL", "COMMERCIAL-RECURRING"}


# B07 — unavailable specialist information remains conditional.
def test_specialist_unavailable_remains_conditional():
    service = GovernedBudgetingService()
    m14_time = inp("M14 assembly time", None, BudgetInputClass.GAP, unit="h", source_id="ASSEMBLY")
    cost = inp("M14 cost", 100, unit="BRL/unit")
    version = service.calculate(request(), inputs=(m14_time, cost), lines=(line(m14_time, cost),))
    assert version.status == BudgetStatus.CONDITIONAL
    assert version.follow_ups


# B08 — source unavailable is represented as a gap, not fabricated retrieval.
def test_unavailable_source_is_explicit_gap():
    service = GovernedBudgetingService()
    missing = inp("supplier quote", None, BudgetInputClass.GAP, unit="BRL/unit", source_id="SUPPLIER-NOT-AVAILABLE")
    quantity = inp("quantity", 5)
    version = service.calculate(request(), inputs=(missing, quantity), lines=(line(quantity, missing),))
    assert version.total_cost is None
    assert "cannot be invented" in version.follow_ups[0].gap


# B09 — recommendation does not grant approval.
def test_recommendation_does_not_grant_approval():
    _, version, _, _ = complete_budget()
    decision = GovernedBudgetingService.recommend(version, recommendation="approve proposal", rationale="complete evidence")
    assert decision.status == "RECOMMENDATION"
    authorization = BudgetAuthorization(TENANT, PRINCIPAL, frozenset({"CALCULATE"}))
    with pytest.raises(BudgetAuthorizationError):
        GovernedBudgetingService.authorize(authorization, tenant_id=TENANT, principal_id=PRINCIPAL, action="APPROVE")


# B10 — cross-tenant inputs are rejected.
def test_cross_tenant_input_is_rejected():
    service = GovernedBudgetingService()
    quantity = inp("quantity", 10, tenant="other-tenant")
    cost = inp("unit cost", 10, unit="BRL/unit")
    with pytest.raises(ValueError, match="cross-tenant"):
        service.calculate(request(), inputs=(quantity, cost), lines=(line(quantity, cost),))


# B11 — cross-domain data requires provenance; no provenance means no fact.
def test_cross_domain_input_without_provenance_is_rejected():
    with pytest.raises(ValueError, match="source_id and provenance"):
        BudgetInput.create(
            tenant_id=TENANT,
            domain="COMERCIAL",
            name="quoted quantity",
            classification=BudgetInputClass.FACT,
            value=10,
            unit="unit",
            source_id="COMMERCIAL-1",
            provenance={},
        )


# B12 — formula/version mismatch blocks the line.
def test_formula_version_mismatch_blocks_calculation():
    service = GovernedBudgetingService()
    quantity = inp("quantity", 10)
    cost = inp("unit cost", 10, unit="BRL/unit")
    version = service.calculate(request(), inputs=(quantity, cost), lines=(line(quantity, cost, formula_version="9.9"),))
    assert version.status == BudgetStatus.CONDITIONAL
    assert version.lines[0].status == BudgetStatus.BLOCKED
    assert version.total_cost is None


# B13 — historical version is immutable and recalculation creates a new version.
def test_recalculation_preserves_previous_version():
    service, first, quantity, cost = complete_budget()
    new_cost = inp("unit cost revised", 30, unit="BRL/unit")
    second = service.recalculate(
        request(),
        first,
        inputs=(quantity, new_cost),
        lines=(BudgetLine(
            line_id="L-REVISED",
            description="revised line",
            line_type=BudgetLineType.COST,
            quantity_input_id=quantity.input_id,
            unit_cost_input_id=new_cost.input_id,
        ),),
    )
    assert first.version_number == 1
    assert first.total_cost == Decimal("255.00")
    assert second.version_number == 2
    assert second.total_cost == Decimal("300.00")
    assert second.supersedes_version_id == first.version_id


# B14 — an attempted fabricated value marked GAP cannot close the gap.
def test_fabricated_gap_value_is_not_accepted_as_fact():
    service = GovernedBudgetingService()
    fabricated = inp("M14 time", 8, BudgetInputClass.GAP, unit="h")
    cost = inp("M14 cost", 100, unit="BRL/unit")
    version = service.calculate(request(), inputs=(fabricated, cost), lines=(line(fabricated, cost),))
    assert version.total_cost is None
    assert version.status == BudgetStatus.CONDITIONAL


# B15 — scenarios compare without mutating baseline.
def test_scenario_comparison_does_not_mutate_baseline():
    service, baseline, quantity, cost = complete_budget()
    alternative_cost = inp("unit cost stress", 35, unit="BRL/unit", source_id="STRESS")
    scenario = BudgetScenario(
        scenario_id="SC-STRESS",
        name="stress",
        kind=BudgetScenarioKind.STRESS,
        overrides={cost.input_id: Decimal("35")},
        rationale="controlled unit-cost variation",
    )
    alternative = service.calculate(
        request(),
        inputs=(quantity, alternative_cost),
        lines=(line(quantity, alternative_cost),),
        scenarios=(scenario,),
    )
    comparison = service.compare_scenarios(baseline, (alternative,))
    assert comparison[0]["known_cost_delta"] == Decimal("95")
    assert baseline.total_cost == Decimal("255.00")
    assert baseline.scenarios == ()


# B16 — new evidence produces a new state/version.
def test_new_evidence_creates_new_budget_version():
    service = GovernedBudgetingService()
    quantity = inp("quantity", None, BudgetInputClass.GAP)
    cost = inp("unit cost", 10, unit="BRL/unit")
    first = service.calculate(request(), inputs=(quantity, cost), lines=(line(quantity, cost),))
    returned_quantity = inp("quantity after specialist feedback", 12, source_id="PCP-FEEDBACK")
    second = service.recalculate(request(), first, inputs=(returned_quantity, cost), lines=(line(returned_quantity, cost),))
    assert first.status == BudgetStatus.CONDITIONAL
    assert second.status == BudgetStatus.COMPLETE
    assert first.version_id != second.version_id
    assert first.inputs[0].classification == BudgetInputClass.GAP


# B17 — budget versus actual produces OutcomeFeedback.
def test_budget_vs_actual_produces_outcome_feedback():
    _, version, _, _ = complete_budget()
    outcome = GovernedBudgetingService.record_outcome(
        version,
        expected="BRL 255.00",
        observed="BRL 270.00",
        evidence_ids=("ACTUAL-1",),
    )
    assert outcome.feedback.assessment == "BUDGET_VS_ACTUAL"
    assert outcome.feedback.evidence_ids == ("ACTUAL-1",)


# B18 — contextual outcome remains an experience/feedback record, not a Core mutation.
def test_contextual_budget_outcome_is_feedback_only():
    _, version, _, _ = complete_budget()
    outcome = GovernedBudgetingService.record_outcome(
        version,
        expected="BRL 255.00",
        observed="BRL 260.00",
        evidence_ids=("ACTUAL-MT001",),
    )
    assert outcome.feedback.decision_id == version.version_id
    assert not hasattr(outcome, "promoted_to_core")


# B19 — generalizable learning still requires the existing learning governance path.
def test_generalizable_learning_requires_existing_governance():
    memory = PersistentMemoryStore()
    service = GovernedLearningService(memory)
    experience = service.capture_outcome(
        tenant_id=TENANT,
        domain="ORCAMENTO",
        principal_id=PRINCIPAL,
        decision_id="D-1",
        expected_outcome="planned",
        observed_outcome="actual",
        evidence_ids=("E-1",),
    )
    candidate = service.propose_candidate(experience, dataset_version="DS-1", hypothesis="generalizable cost pattern")
    evaluation = service.evaluate(candidate, metric="accuracy", score=0.95, threshold=0.90, evaluator="validator")
    with pytest.raises(ValueError, match="human approval"):
        service.approve_for_promotion(candidate, evaluation, human_approved=False)
    approved = service.approve_for_promotion(candidate, evaluation, human_approved=True)
    assert approved.state == "APPROVED"
    memory.close()


# B20 — MT-001 stays conditional while missing M14/mix/return evidence remain gaps.
def test_mt001_is_conditional_and_preserves_exact_gaps():
    service = GovernedBudgetingService()
    seasonal = inp("seasonal demand", 300, source_id="MT001")
    recurring = inp("recurring demand", 70, source_id="MT001")
    m01_time = inp("M01 assembly time", 4, unit="h", source_id="MT001")
    m05_time = inp("M05 assembly time", 6, unit="h", source_id="MT001")
    m14_time = inp("M14 assembly time", None, BudgetInputClass.GAP, unit="h", source_id="MT001")
    returns = inp("September returns composition", None, BudgetInputClass.GAP, source_id="MT001")
    version = service.calculate(
        request(),
        inputs=(seasonal, recurring, m01_time, m05_time, m14_time, returns),
        lines=(),
        assumptions=(Assumption(
            assumption_id="P001",
            statement="returned modules may become usable after repair/release",
            evidence_ids=(returns.input_id,),
            provenance=PROVENANCE,
        ),),
    )
    assert version.status == BudgetStatus.CONDITIONAL
    assert version.total_cost is None
    assert len(version.follow_ups) == 2
    assert any("M14 assembly time" in item.gap for item in version.follow_ups)
    assert any("September returns composition" in item.gap for item in version.follow_ups)
    assert seasonal.value == Decimal("300")
    assert recurring.value == Decimal("70")
    assert m14_time.value is None
    assert returns.value is None
