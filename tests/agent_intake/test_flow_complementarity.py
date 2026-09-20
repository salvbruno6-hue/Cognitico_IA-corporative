from elo.agent_intake.flow_complementarity import (
    ComplementarityEngine,
    ConnectionStatus,
    FlowProfile,
    RelationKind,
    hermes_relation,
)


def profiles():
    return (
        FlowProfile(
            "CONTROLLED_TEST",
            "ELO Evolution",
            accepts=("candidate",),
            produces=("controlled_evidence",),
            success_outcomes=("PASS",),
            failure_outcomes=("RETEST", "BLOCKED"),
            evidence_required=("baseline", "adapted", "repeatable"),
            provenance_required=("source",),
            allowed_next_relations=(RelationKind.FEEDS,),
        ),
        FlowProfile(
            "MEASURED_GAIN",
            "ELO Evolution",
            accepts=("controlled_evidence",),
            produces=("measured_gain",),
            prerequisites=("baseline", "adapted", "repeatable"),
            success_outcomes=("PASS",),
            failure_outcomes=("RETEST",),
            evidence_required=("baseline", "adapted", "repeatable"),
            provenance_required=("source",),
            allowed_next_relations=(RelationKind.FEEDS,),
        ),
    )


def test_hermes_relation_is_not_canonical():
    relation = hermes_relation(
        relation_id="hermes-rel-1",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("hermes:evaluation:1",),
        provenance_refs=("hermes:source:1",),
        confidence=1.0,
    )
    assert relation.source == "HERMES"
    assert relation.canonical is False


def test_compatible_evidenced_connection_becomes_eligible():
    relation = hermes_relation(
        relation_id="hermes-rel-2",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("hermes:evaluation:2",),
        provenance_refs=("hermes:source:2",),
        confidence=1.0,
    )
    decision = ComplementarityEngine(profiles(), (relation,)).evaluate(
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        relation_kind=RelationKind.FEEDS,
        outcome="PASS",
        available_evidence={
            "baseline": True,
            "adapted": True,
            "repeatable": True,
        },
        provenance_refs=("hermes:source:2",),
    )
    assert decision.status is ConnectionStatus.ELIGIBLE


def test_unknown_relation_stops_fail_closed():
    decision = ComplementarityEngine(profiles()).evaluate(
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        relation_kind=RelationKind.FEEDS,
        outcome="PASS",
        available_evidence={"baseline": True, "adapted": True, "repeatable": True},
        provenance_refs=("source:1",),
    )
    assert decision.status is ConnectionStatus.REVIEW_REQUIRED


def test_missing_prerequisite_waits():
    relation = hermes_relation(
        relation_id="hermes-rel-3",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("hermes:evaluation:3",),
        provenance_refs=("hermes:source:3",),
        confidence=1.0,
    )
    decision = ComplementarityEngine(profiles(), (relation,)).evaluate(
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        relation_kind=RelationKind.FEEDS,
        outcome="PASS",
        available_evidence={"baseline": True, "adapted": True},
        provenance_refs=("hermes:source:3",),
    )
    assert decision.status is ConnectionStatus.WAITING


def test_consequential_target_requires_authorization():
    origin = FlowProfile(
        "A", "owner", ("x",), ("y",), success_outcomes=("PASS",),
        allowed_next_relations=(RelationKind.HANDOFF,),
    )
    target = FlowProfile(
        "B", "owner", ("y",), ("z",), success_outcomes=("PASS",),
        side_effect_class="consequential",
        allowed_next_relations=(),
    )
    relation = hermes_relation(
        relation_id="hermes-rel-4",
        origin_flow="A",
        target_flow="B",
        kind=RelationKind.HANDOFF,
        evidence_refs=("h1",),
        provenance_refs=("p1",),
        confidence=1.0,
    )
    decision = ComplementarityEngine((origin, target), (relation,)).evaluate(
        origin_flow="A",
        target_flow="B",
        relation_kind=RelationKind.HANDOFF,
        outcome="PASS",
        available_evidence={"authorized": False},
        provenance_refs=("p1",),
    )
    assert decision.status is ConnectionStatus.WAITING
