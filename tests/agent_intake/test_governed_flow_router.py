from elo.agent_intake.elo_flow_cadence import CadenceOutcome
from elo.agent_intake.flow_complementarity import (
    ComplementarityEngine,
    FlowProfile,
    RelationKind,
    hermes_relation,
)
from elo.agent_intake.governed_flow_router import GovernedFlowRouter


def test_router_requires_both_relation_and_registered_cadence():
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
        relation_id="r-router-1",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("h1",),
        provenance_refs=("p1",),
        confidence=1.0,
    )
    router = GovernedFlowRouter(
        complementarity=ComplementarityEngine(profiles, (relation,))
    )
    result = router.resolve(
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        outcome=CadenceOutcome.PASS,
        relation_kind=RelationKind.FEEDS,
        evidence={"baseline": True, "adapted": True, "repeatable": True},
        provenance_refs=("p1",),
    )
    assert result.status == "ELIGIBLE"
    assert result.cadence_next == "MEASURED_GAIN"


def test_router_does_not_execute_or_authorize():
    profiles = (
        FlowProfile(
            "CONTROLLED_TEST", "ELO", ("candidate",), ("controlled_evidence",),
            success_outcomes=("PASS",),
            allowed_next_relations=(RelationKind.FEEDS,),
        ),
        FlowProfile(
            "MEASURED_GAIN", "ELO", ("controlled_evidence",), ("measured_gain",),
            success_outcomes=("PASS",),
        ),
    )
    relation = hermes_relation(
        relation_id="r-router-2",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("h2",),
        provenance_refs=("p2",),
        confidence=1.0,
    )
    router = GovernedFlowRouter(
        complementarity=ComplementarityEngine(profiles, (relation,))
    )
    result = router.resolve(
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        outcome=CadenceOutcome.PASS,
        relation_kind=RelationKind.FEEDS,
        evidence={},
        provenance_refs=("p2",),
    )
    assert result.status == "WAITING"
    assert result.capability is None
