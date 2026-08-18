from elo.core.context_resolution import ContextEvidence, ContextQuery, ContextResolutionEngine, ContextSource
from elo.core.core_loop import CoreLoopEngine, CoreLoopRequest
from elo.core.cross_domain import CorporateDomain, CrossDomainRelation
from elo.core.corporate_systemic import CorporateSystemicView
from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenario
from elo.core.scenario_gates import MultiScenarioGate
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback, SystemicModel


def context_pack():
    engine = ContextResolutionEngine()
    pack = engine.resolve(
        ContextQuery(
            "avaliar prazo de entrega",
            tenant_id="tenant-a",
            domain="PCP",
            principal_id="principal-a",
            request_id="request-a",
            correlation_id="corr-a",
        )
    )
    return engine.enrich(
        pack,
        sources=(ContextSource("e1", "document", "external", tenant_id="tenant-a", domain="PCP"),),
        evidence=(ContextEvidence("e1", "delivery evidence", 0.9, tenant_id="tenant-a", domain="PCP"),),
    )


def scenario(kind):
    return DiagnosticScenario(
        scenario_id=kind.lower(),
        question="avaliar prazo",
        observations=(
            DiagnosticObservation(
                evidence_id="e1",
                dimension="delivery",
                value=0.9,
                statement=f"{kind} delivery condition",
                confidence=0.9,
                lens=DiagnosticLens.OPERATIONAL,
            ),
        ),
        metadata={
            "scenario_type": kind,
            "metrics": "lead_time",
            "metric:lead_time": "3d",
        },
    )


def test_baseline_composes_context_cross_domain_scenario_and_core_loop():
    context = context_pack()
    relation = CrossDomainRelation(
        relation_id="r1",
        origin_domain=CorporateDomain.COMMERCIAL,
        destination_domain=CorporateDomain.BUDGET,
        relation_type="INFORMS",
        statement="commercial demand informs budget",
        tenant_id="tenant-a",
        principal_id="principal-a",
        source_id="e1",
        evidence_ids=("e1",),
        valid_from="2026-08-18",
        confidence=0.9,
        provenance={
            "origin_domain": CorporateDomain.COMMERCIAL.value,
            "destination_domain": CorporateDomain.BUDGET.value,
        },
    )
    systemic = CorporateSystemicView.build(SystemicModel(), (relation,), tenant_id="tenant-a")
    observations = context.scoped_evidence()
    diagnostic_observations = (
        DiagnosticObservation("e1", "delivery", 0.9, "delivery constrained", 0.9, lens=DiagnosticLens.OPERATIONAL),
        DiagnosticObservation("e1", "delivery", 0.9, "capacity constrained", 0.9, lens=DiagnosticLens.CAPACITY),
    )
    result = CoreLoopEngine().run(
        CoreLoopRequest(
            context=context,
            scenario=DiagnosticScenario("baseline", "avaliar prazo", observations=diagnostic_observations),
            observations=diagnostic_observations,
        )
    )
    assert observations[0].source_id == "e1"
    assert systemic.source_of_truth == "derived_projection"
    assert result.evidence_ids == ("e1",)
    assert result.can_execute is False


def test_baseline_multi_scenario_gate_requires_complete_and_shared_evidence():
    result = MultiScenarioGate().evaluate(tuple(scenario(kind) for kind in (
        "BASELINE", "STRESS", "FAILURE", "COUNTERFACTUAL", "SENSITIVITY"
    )))
    assert result.ready_for_reasoning is True
    assert result.shared_evidence == ("e1",)


def test_baseline_decision_and_outcome_feedback_remain_traceable():
    decision = DecisionRecord(
        decision_id="d1",
        decision="request review",
        rationale="delivery evidence indicates risk",
        evidence_ids=("e1",),
        authority="principal-a",
        expected_outcome="review completed",
    )
    feedback = OutcomeFeedback("d1", "review completed", "review completed", evidence_ids=("e2",))
    assert decision.evidence_ids == ("e1",)
    assert feedback.decision_id == decision.decision_id
    assert feedback.evidence_ids == ("e2",)


def test_baseline_context_does_not_cross_tenant():
    context = context_pack()
    foreign = ContextSource("foreign", "document", "external", tenant_id="tenant-b", domain="PCP")
    enriched = ContextResolutionEngine().enrich(context, sources=(foreign,))
    assert enriched.evidence_ids() == ("e1",)
