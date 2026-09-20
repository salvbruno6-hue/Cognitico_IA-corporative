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
            prerequisites=("baseline",),
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



def test_router_discovers_the_single_governed_complementary_next_flow():
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
        relation_id="r-router-discovery-1",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("h-discovery",),
        provenance_refs=("p-discovery",),
        confidence=1.0,
    )
    router = GovernedFlowRouter(
        complementarity=ComplementarityEngine(profiles, (relation,))
    )

    result = router.resolve_next(
        origin_flow="CONTROLLED_TEST",
        outcome=CadenceOutcome.PASS,
        evidence={"baseline": True, "adapted": True, "repeatable": True},
        provenance_refs=("p-discovery",),
    )

    assert result.status == "ELIGIBLE"
    assert result.selected_next == "MEASURED_GAIN"
    assert len(result.candidates) == 1


def test_router_never_selects_an_ambiguous_or_unregistered_next_flow():
    profiles = (
        FlowProfile(
            "CONTROLLED_TEST", "ELO", ("candidate",), ("controlled_evidence",),
            success_outcomes=("PASS",),
            allowed_next_relations=(RelationKind.FEEDS, RelationKind.ENRICHES),
        ),
        FlowProfile(
            "MEASURED_GAIN", "ELO", ("controlled_evidence",), ("measured_gain",),
            success_outcomes=("PASS",),
        ),
    )
    relation = hermes_relation(
        relation_id="r-router-discovery-2",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.ENRICHES,
        evidence_refs=("h-ambiguous",),
        provenance_refs=("p-ambiguous",),
        confidence=1.0,
    )
    relation_2 = hermes_relation(
        relation_id="r-router-discovery-3",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("h-feeds",),
        provenance_refs=("p-feeds",),
        confidence=1.0,
    )
    router = GovernedFlowRouter(
        complementarity=ComplementarityEngine(profiles, (relation, relation_2))
    )

    result = router.resolve_next(
        origin_flow="CONTROLLED_TEST",
        outcome=CadenceOutcome.PASS,
        evidence={"baseline": True},
        provenance_refs=("p-ambiguous", "p-feeds"),
    )

    assert result.status == "REVIEW_REQUIRED"
    assert result.selected_next is None

def test_router_reports_capability_requirement_without_selector_as_configuration_gap():
    profiles = (
        FlowProfile(
            "CONTROLLED_TEST", "ELO", ("candidate",), ("controlled_evidence",),
            success_outcomes=("PASS",), allowed_next_relations=(RelationKind.FEEDS,),
        ),
        FlowProfile(
            "MEASURED_GAIN", "ELO", ("controlled_evidence",), ("measured_gain",),
            prerequisites=("baseline",), success_outcomes=("PASS",),
        ),
    )
    relation = hermes_relation(
        relation_id="r-capability-gap",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("h-capability-gap",),
        provenance_refs=("p-capability-gap",),
        confidence=1.0,
    )
    router = GovernedFlowRouter(
        complementarity=ComplementarityEngine(profiles, (relation,))
    )
    try:
        router.resolve(
            origin_flow="CONTROLLED_TEST",
            target_flow="MEASURED_GAIN",
            outcome=CadenceOutcome.PASS,
            relation_kind=RelationKind.FEEDS,
            evidence={"baseline": True},
            provenance_refs=("p-capability-gap",),
            capability_requirement=object(),
        )
    except ValueError as exc:
        assert "capability selector" in str(exc)
    else:
        raise AssertionError("missing capability selector must not be silently bypassed")
