"""Executable consolidation evidence for ELO-011 / issue #92.

This suite verifies composition of existing canonical contracts. It deliberately
avoids introducing a second Core, memory, scheduler, executor, or scenario owner.
"""

from elo.core.context_resolution import ContextEvidence, ContextPack, ContextQuery, ContextSource
from elo.core.core_loop import CoreLoopEngine, CoreLoopRequest
from elo.core.cross_domain import CorporateDomain, CrossDomainGovernance, CrossDomainRelation
from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenario, DiagnosticStatus
from elo.core.scenario_gates import MultiScenarioGate
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback


def build_context(*, tenant: str = "tenant-a", domain: str = "ORCAMENTO", principal: str = "principal-a") -> ContextPack:
    source = ContextSource(
        source_id="budget-source-1",
        source_type="fixture",
        authority="test-fixture",
        tenant_id=tenant,
        domain=domain,
        principal_id=principal,
        provenance={"fixture": "ELO-011"},
    )
    evidence = ContextEvidence(
        source_id="budget-source-1",
        fact="budget evidence is available",
        confidence=0.95,
        tenant_id=tenant,
        domain=domain,
        provenance={"principal_id": principal},
    )
    return ContextPack(
        query=ContextQuery(
            question="validate budget integration",
            tenant_id=tenant,
            domain=domain,
            principal_id=principal,
            request_id="req-011",
            correlation_id="corr-011",
        ),
        sources=(source,),
        evidence=(evidence,),
    )


def observation(evidence_id: str = "budget-source-1", *, status=DiagnosticStatus.SUPPORTED):
    return DiagnosticObservation(
        evidence_id=evidence_id,
        dimension="capacity",
        value=1.0,
        statement="capacity evidence is consistent",
        confidence=0.95,
        lens=DiagnosticLens.EVIDENCE,
        status=status,
    )


def test_context_preserves_tenant_domain_principal_and_evidence_scope():
    pack = build_context()
    scoped = pack.scoped_evidence()
    assert len(scoped) == 1
    assert scoped[0].source_id == "budget-source-1"
    assert pack.query.tenant_id == "tenant-a"
    assert pack.query.domain == "ORCAMENTO"
    assert pack.query.principal_id == "principal-a"


def test_context_blocks_cross_tenant_evidence():
    pack = build_context(tenant="tenant-a")
    foreign = ContextEvidence(
        source_id="foreign-source",
        fact="foreign evidence",
        confidence=0.99,
        tenant_id="tenant-b",
        domain="ORCAMENTO",
    )
    restricted = ContextPack(query=pack.query, sources=pack.sources, evidence=(foreign,))
    assert restricted.scoped_evidence() == ()
    assert restricted.integrity_gaps() == ()


def test_cross_domain_relation_preserves_provenance_and_rejects_tenant_mismatch():
    relation = CrossDomainRelation(
        relation_id="r-011",
        origin_domain=CorporateDomain.COMMERCIAL,
        destination_domain=CorporateDomain.BUDGET,
        relation_type="INFORMS",
        statement="commercial demand informs budget premise",
        tenant_id="tenant-a",
        principal_id="principal-a",
        source_id="commercial-source",
        evidence_ids=("commercial-e1",),
        valid_from="2026-08-18",
        confidence=0.9,
        provenance={
            "origin_domain": CorporateDomain.COMMERCIAL.value,
            "destination_domain": CorporateDomain.BUDGET.value,
        },
    )
    governance = CrossDomainGovernance()
    assert governance.validate(relation, expected_tenant_id="tenant-a").status == "VALID"
    assert governance.validate(relation, expected_tenant_id="tenant-b").status == "BLOCKED"


def test_core_loop_never_authorizes_execution_even_when_evidence_is_sufficient():
    request = CoreLoopRequest(
        context=build_context(),
        scenario=DiagnosticScenario(scenario_id="scenario-011", question="is budget evidence ready?"),
        observations=(observation(),),
    )
    result = CoreLoopEngine().run(request)
    assert result.status == "RECOMMENDATION"
    assert result.handoff_required is False
    assert result.can_execute is False
    assert result.evidence_ids == ("budget-source-1",)


def test_core_loop_blocks_when_no_diagnostic_evidence_is_supplied():
    request = CoreLoopRequest(
        context=build_context(),
        scenario=DiagnosticScenario(scenario_id="scenario-011-empty", question="validate integration"),
    )
    result = CoreLoopEngine().run(request)
    assert result.status == "BLOCKED"
    assert result.handoff_required is True
    assert result.can_execute is False


def test_multi_scenario_gate_blocks_incomplete_scenario_set():
    scenario = DiagnosticScenario(
        scenario_id="baseline-only",
        question="compare budget",
        observations=(observation(),),
        metadata={"scenario_type": "BASELINE", "metrics": "cost", "metric:cost": "100"},
    )
    result = MultiScenarioGate().evaluate((scenario,))
    assert result.status == "BLOCKED"
    assert result.ready_for_reasoning is False
    assert any("missing scenario types" in gap for gap in result.gaps)


def test_multi_scenario_gate_blocks_conflicting_evidence():
    scenario = DiagnosticScenario(
        scenario_id="failure-conflict",
        question="compare failure mode",
        observations=(observation(status=DiagnosticStatus.CONFLICTING),),
        metadata={"scenario_type": "FAILURE", "metrics": "cost", "metric:cost": "100"},
    )
    result = MultiScenarioGate().evaluate((scenario,))
    assert result.status == "BLOCKED"
    assert any("conflicting evidence" in gap for gap in result.gaps)


def test_decision_and_outcome_feedback_remain_linked_by_decision_id():
    decision = DecisionRecord(
        decision_id="decision-011",
        decision="prepare revised budget",
        rationale="evidence indicates a capacity gap",
        evidence_ids=("budget-source-1",),
        expected_outcome="revised budget recommendation",
    )
    feedback = OutcomeFeedback(
        decision_id=decision.decision_id,
        expected=decision.expected_outcome or "",
        observed="revised budget recommendation produced",
        evidence_ids=("budget-source-1",),
    )
    assert feedback.decision_id == decision.decision_id
    assert feedback.evidence_ids == decision.evidence_ids


def test_context_handoff_is_bounded_and_contains_no_reasoning_trace():
    payload = build_context().consultation_payload()
    assert payload["request_id"] == "req-011"
    assert payload["correlation_id"] == "corr-011"
    assert "reasoning_trace" not in payload
    assert payload["evidence_ids"] == ("budget-source-1",)


def test_cross_domain_evidence_is_explicit_not_inferred_from_flow_order():
    relation = CrossDomainRelation(
        relation_id="r-011-explicit",
        origin_domain=CorporateDomain.TENDERS,
        destination_domain=CorporateDomain.BUDGET,
        relation_type="INFORMS",
        statement="tender requirement informs budget premise",
        tenant_id="tenant-a",
        principal_id="principal-a",
        source_id="tender-source",
        evidence_ids=("tender-e1",),
        valid_from="2026-08-18",
        confidence=0.9,
    )
    assert relation.evidence_ids == ("tender-e1",)
    assert relation.origin_domain != relation.destination_domain
