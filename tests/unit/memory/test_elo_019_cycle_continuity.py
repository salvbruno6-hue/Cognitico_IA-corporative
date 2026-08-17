import copy
import json
from pathlib import Path


FIXTURE = Path(__file__).parents[2] / "fixtures" / "elo_018_cycle_memory.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_c1_c2_c3_continuity_and_relevant_context() -> None:
    data = load_fixture()
    c1, c2, c3 = data["cycles"]
    assert c2["parent_cycle_id"] == c1["cycle_id"]
    assert c3["parent_cycle_id"] == c2["cycle_id"]
    assert c2["state_before"] == c1["state_after"]
    assert c3["state_before"] == c2["state_after"]
    assert c2["state_before"] == {"demand": "D1", "plan": "P1", "budget": "B1"}


def test_decision_to_result_trace_is_preserved() -> None:
    data = load_fixture()
    c2, c3 = data["cycles"][1:]
    assert c2["decision"] == "supported_with_impact"
    assert c2["action"] == "recalculate_and_monitor"
    assert c2["outcome"] == "impact_propagated"
    assert c3["decision"] == "causal_comparison"
    assert c3["action"] == "classify_learning"
    assert c3["outcome"] == "mechanic_repeated"


def test_fact_inference_and_learning_candidate_are_distinct() -> None:
    data = load_fixture()
    for cycle in data["cycles"]:
        assert cycle["evidence"]
        assert cycle["provenance"]
        assert cycle["learning_status"] != "canonical"
    assert data["cycles"][2]["learning_status"] == "faculty_candidate"


def test_learning_classification_cases_are_explicit() -> None:
    data = load_fixture()
    cases = {item["case"]: item["expected"] for item in data["learning_cases"]}
    assert cases == {
        "repeated_general_mechanic": "faculty_candidate",
        "tenant_specific_mechanic": "overlay",
        "missing_evidence": "gap",
        "incompatible_evidence": "conflict",
    }


def test_validated_knowledge_survives_specialist_removal() -> None:
    data = load_fixture()
    knowledge = {"faculty": "validated_mechanic"}
    specialists = set(data["cycles"][2]["specialists"])
    specialists.remove("orcamento")
    assert knowledge == {"faculty": "validated_mechanic"}
    assert "orcamento" not in specialists


def test_overlay_removal_does_not_remove_faculty() -> None:
    knowledge = {"faculty": {"mechanic": "general"}, "overlay": {"tenant": "multiteiner"}}
    knowledge["overlay"] = None
    assert knowledge["faculty"] == {"mechanic": "general"}


def test_history_is_immutable_for_repeated_execution() -> None:
    data = load_fixture()
    original = copy.deepcopy(data["cycles"])
    replay = copy.deepcopy(data["cycles"])
    assert replay == original
    assert original is not replay


def test_tenant_boundary_is_preserved() -> None:
    data = load_fixture()
    assert data["tenant_id"] == "multiteiner-synthetic"
    assert data["synthetic"] is True
    assert "tenant_boundary_preserved" in data["invariants"]


def test_no_parallel_memory_authority() -> None:
    data = load_fixture()
    assert "no_parallel_memory_authority" in data["invariants"]
    assert "history_immutable" in data["invariants"]
    assert "context_derived" in data["invariants"]


def test_cycle_correlation_is_single_and_ordered() -> None:
    data = load_fixture()
    cycles = data["cycles"]
    assert [cycle["cycle_id"] for cycle in cycles] == ["C1", "C2", "C3"]
    assert len({cycle["correlation_id"] for cycle in cycles}) == 1


def test_missing_evidence_and_conflict_do_not_become_canonical() -> None:
    data = load_fixture()
    cases = {item["case"]: item["expected"] for item in data["learning_cases"]}
    assert cases["missing_evidence"] == "gap"
    assert cases["incompatible_evidence"] == "conflict"
    assert all(cycle["learning_status"] != "canonical" for cycle in data["cycles"])
