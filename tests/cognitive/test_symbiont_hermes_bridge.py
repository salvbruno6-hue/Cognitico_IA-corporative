import pytest

from elo.cognitive.agents.hermes_contract import HermesExecutionRequest
from elo.cognitive.symbiont_hermes_bridge import SymbiontHermesBridge


def _request(capabilities=("skill:execute",)):
    return HermesExecutionRequest(
        request_id="symbiont-hermes-001",
        intent="executar capacidade autorizada",
        context={"domain": "test"},
        tenant_scope="tenant-test",
        mission_class="skill_execution",
        authorized_capabilities=capabilities,
        evidence_requirements=("execution", "outcome"),
    )


def test_symbiont_forwards_only_an_authorized_capability():
    seen = {}

    def transport(endpoint, payload):
        seen["endpoint"] = endpoint
        seen["payload"] = payload
        return {
            "request_id": payload["request_id"],
            "status": "completed",
            "execution": {"runtime": "hermes"},
            "evidence": ({"type": "skill_execution"},),
            "outcome": {"result": "ok"},
            "learning_candidate": {"promotion_state": "candidate_only"},
        }

    receipt = SymbiontHermesBridge().execute(
        _request(),
        capability="skill:execute",
        endpoint="http://hermes.test",
        transport=transport,
    )

    assert receipt.request_id == "symbiont-hermes-001"
    assert receipt.capability == "skill:execute"
    assert seen["endpoint"] == "http://hermes.test"
    assert seen["payload"]["authorized_capabilities"] == ("skill:execute",)
    assert receipt.result.outcome["result"] == "ok"


def test_symbiont_rejects_capability_not_authorized_by_elo():
    with pytest.raises(ValueError, match="not authorized"):
        SymbiontHermesBridge().execute(
            _request(("skill:read",)),
            capability="skill:execute",
            endpoint="http://hermes.test",
            transport=lambda *_: {},
        )


def test_symbiont_rejects_result_without_required_outcome():
    def transport(endpoint, payload):
        return {
            "request_id": payload["request_id"],
            "status": "completed",
            "execution": {"runtime": "hermes"},
        }

    with pytest.raises(ValueError, match="outcome evidence"):
        SymbiontHermesBridge().execute(
            _request(),
            capability="skill:execute",
            endpoint="http://hermes.test",
            transport=transport,
        )


def test_symbiont_preserves_candidate_only_learning_boundary():
    def transport(endpoint, payload):
        return {
            "request_id": payload["request_id"],
            "status": "completed",
            "execution": {"runtime": "hermes"},
            "evidence": ({"type": "execution"},),
            "outcome": {"result": "ok"},
            "learning_candidate": {"promotion_state": "candidate_only"},
        }

    receipt = SymbiontHermesBridge().execute(
        _request(),
        capability="skill:execute",
        endpoint="http://hermes.test",
        transport=transport,
    )

    assert receipt.result.learning_candidate["promotion_state"] == "candidate_only"

from elo.agent_intake.flow_complementarity import (
    ComplementarityEngine,
    FlowProfile,
    RelationKind,
    hermes_relation,
)
from elo.agent_intake.governed_flow_router import GovernedFlowRouter
from elo.agent_intake.flow_learning import FlowAdaptationEngine, SQLiteFlowLearningStore


def test_symbiont_is_inside_the_governed_flow_and_persists_outcome():
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
        relation_id="r-symbiont-flow-1",
        origin_flow="CONTROLLED_TEST",
        target_flow="MEASURED_GAIN",
        kind=RelationKind.FEEDS,
        evidence_refs=("hermes-e1",),
        provenance_refs=("source",),
        confidence=1.0,
    )
    router = GovernedFlowRouter(
        complementarity=ComplementarityEngine(profiles, (relation,))
    )
    learning = FlowAdaptationEngine(SQLiteFlowLearningStore(":memory:"))

    def transport(endpoint, payload):
        return {
            "request_id": payload["request_id"],
            "status": "completed",
            "execution": {"ok": True},
            "evidence": ({"id": "hermes-e1"},),
            "outcome": {"status": "completed"},
            "metrics": {"quality": 1.0},
            "learning_candidate": {"promotion_state": "candidate_only"},
        }

    receipt, adaptation, routing = SymbiontHermesBridge().execute_flow_step(
        _request(),
        capability="skill:execute",
        endpoint="http://hermes.test",
        origin_flow="CONTROLLED_TEST",
        relation_id="r-symbiont-flow-1",
        next_flow="MEASURED_GAIN",
        evidence={"baseline": True, "adapted": True, "repeatable": True},
        provenance_refs=("source",),
        router=router,
        learning=learning,
        transport=transport,
    )

    assert receipt.result.status == "completed"
    assert adaptation.observations == 1
    assert adaptation.status == "INSUFFICIENT_EVIDENCE"
    assert routing.status == "ELIGIBLE"
    assert routing.selected_next == "MEASURED_GAIN"
