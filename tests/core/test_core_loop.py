from elo.core.context_resolution import ContextEvidence, ContextQuery, ContextResolutionEngine, ContextSource
from elo.agent_intake.elo_flow_cadence import CadenceOutcome
from elo.agent_intake.flow_complementarity import ComplementarityEngine, FlowProfile, RelationKind, hermes_relation
from elo.agent_intake.governed_flow_router import GovernedFlowRouter
from elo.core.core_loop import CoreLoopEngine, CoreLoopRequest
from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenario, DiagnosticStatus


def context():
    engine = ContextResolutionEngine()
    pack = engine.resolve(ContextQuery("avaliar capacidade", tenant_id="tenant-a", domain="PCP"))
    return engine.enrich(
        pack,
        sources=(ContextSource("e1", "document", "external", tenant_id="tenant-a", domain="PCP"),),
        evidence=(ContextEvidence("e1", "capacity evidence", 0.9, tenant_id="tenant-a", domain="PCP"),),
    )


def observation(evidence_id, lens, confidence=0.9, status=DiagnosticStatus.SUPPORTED):
    return DiagnosticObservation(
        evidence_id=evidence_id,
        dimension=lens.value,
        value=0.9,
        statement=f"finding-{lens.value}",
        confidence=confidence,
        lens=lens,
        status=status,
    )


def test_core_loop_covers_multiple_lenses_without_execution_authority():
    observations = (
        observation("e1", DiagnosticLens.OPERATIONAL),
        observation("e1", DiagnosticLens.CAPACITY),
        observation("e1", DiagnosticLens.MATERIAL),
        observation("e1", DiagnosticLens.FINANCIAL),
        observation("e1", DiagnosticLens.CUSTOMER),
        observation("e1", DiagnosticLens.RISK),
        observation("e1", DiagnosticLens.TEMPORAL),
        observation("e1", DiagnosticLens.SYSTEMIC),
    )
    scenario = DiagnosticScenario("s1", "avaliar capacidade", observations=observations)
    result = CoreLoopEngine().run(CoreLoopRequest(context(), scenario, observations))
    assert result.status == "RECOMMENDATION"
    assert set(result.covered_lenses) == {observation.lens.value for observation in observations}
    assert result.can_execute is False


def test_core_loop_blocks_conflicting_evidence_and_requires_handoff():
    observations = (
        observation("e1", DiagnosticLens.OPERATIONAL),
        observation("e1", DiagnosticLens.CAPACITY, status=DiagnosticStatus.CONFLICTING),
    )
    scenario = DiagnosticScenario("s2", "avaliar conflito", observations=observations)
    result = CoreLoopEngine().run(CoreLoopRequest(context(), scenario, observations))
    assert result.status == "HANDOFF"
    assert result.handoff_required is True
    assert "conflicting specialist evidence" in result.gaps


def test_core_loop_blocks_low_confidence_and_never_mutates_context():
    pack = context()
    observations = (observation("e1", DiagnosticLens.OPERATIONAL, confidence=0.4),)
    scenario = DiagnosticScenario("s3", "avaliar baixa confiança", observations=observations)
    before = pack
    result = CoreLoopEngine().run(CoreLoopRequest(pack, scenario, observations, minimum_confidence=0.7))
    assert result.status == "HANDOFF"
    assert result.handoff_required is True
    assert pack == before


def test_core_loop_with_no_observations_is_blocked_not_invented():
    scenario = DiagnosticScenario("s4", "avaliar sem evidência")
    result = CoreLoopEngine().run(CoreLoopRequest(context(), scenario))
    assert result.status == "BLOCKED"
    assert result.evidence_ids == ("e1",)
    assert result.handoff_required is True



def test_core_loop_uses_governed_complementarity_for_the_next_flow():
    profiles = (
        FlowProfile(
            "CONTROLLED_TEST", "ELO", ("candidate",), ("controlled_evidence",),
            success_outcomes=("PASS",),
            allowed_next_relations=(RelationKind.FEEDS,),
        ),
        FlowProfile(
            "MEASURED_GAIN", "ELO", ("controlled_evidence",), ("measured_gain",),
            prerequisites=("baseline", "adapted", "repeatable"),
            success_outcomes=("PASS",),
            evidence_required=("baseline", "adapted", "repeatable"),
            provenance_required=("source",),
        ),
    )
    relation = hermes_relation(
        relation_id="r-core-loop-1",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("h-core-loop",),
        provenance_refs=("p-core-loop",),
        confidence=1.0,
    )
    router = GovernedFlowRouter(
        complementarity=ComplementarityEngine(profiles, (relation,))
    )
    observations = (observation("e1", DiagnosticLens.OPERATIONAL),)
    scenario = DiagnosticScenario("s-flow", "avaliar fluxo", observations=observations)
    result = CoreLoopEngine(flow_router=router).run(
        CoreLoopRequest(
            context(),
            scenario,
            observations,
            flow_origin="CONTROLLED_TEST",
            flow_outcome=CadenceOutcome.PASS,
            flow_relation_kind=RelationKind.FEEDS,
            flow_evidence={"baseline": True, "adapted": True, "repeatable": True},
            flow_provenance_refs=("p-core-loop",),
        )
    )
    assert result.status == "RECOMMENDATION"
    assert result.next_flow == "MEASURED_GAIN"
    assert result.flow_routing_status == "ELIGIBLE"
    assert result.can_execute is False

def test_core_loop_withholds_next_flow_when_diagnostics_require_handoff():
    profiles = (
        FlowProfile(
            "CONTROLLED_TEST", "ELO", ("candidate",), ("controlled_evidence",),
            success_outcomes=("PASS",),
            allowed_next_relations=(RelationKind.FEEDS,),
        ),
        FlowProfile(
            "MEASURED_GAIN", "ELO", ("controlled_evidence",), ("measured_gain",),
            prerequisites=("baseline",), success_outcomes=("PASS",),
        ),
    )
    relation = hermes_relation(
        relation_id="r-core-loop-gated-1",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("h-core-gated",),
        provenance_refs=("p-core-gated",),
        confidence=1.0,
    )
    router = GovernedFlowRouter(
        complementarity=ComplementarityEngine(profiles, (relation,))
    )
    observations = (
        observation("e1", DiagnosticLens.OPERATIONAL),
        observation("e1", DiagnosticLens.CAPACITY, status=DiagnosticStatus.CONFLICTING),
    )
    scenario = DiagnosticScenario("s-flow-gated", "avaliar fluxo conflitante", observations=observations)
    result = CoreLoopEngine(flow_router=router).run(
        CoreLoopRequest(
            context(),
            scenario,
            observations,
            flow_origin="CONTROLLED_TEST",
            flow_outcome=CadenceOutcome.PASS,
            flow_relation_kind=RelationKind.FEEDS,
            flow_evidence={"baseline": True},
            flow_provenance_refs=("p-core-gated",),
        )
    )
    assert result.status == "HANDOFF"
    assert result.next_flow is None
    assert result.flow_routing_status is None
    assert "next flow withheld by core-loop diagnostic gate" in result.gaps
