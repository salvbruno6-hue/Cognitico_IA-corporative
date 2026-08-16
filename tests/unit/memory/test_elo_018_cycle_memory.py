import json
from pathlib import Path


FIXTURE = Path(__file__).parents[2] / "fixtures" / "elo_018_cycle_memory.json"


def test_cycle_memory_is_sequential_and_correlated() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    cycles = data["cycles"]
    assert len(cycles) == 3
    assert cycles[1]["parent_cycle_id"] == cycles[0]["cycle_id"]
    assert cycles[2]["parent_cycle_id"] == cycles[1]["cycle_id"]
    assert len({cycle["correlation_id"] for cycle in cycles}) == 1


def test_context_and_provenance_are_preserved() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for cycle in data["cycles"]:
        assert cycle["evidence"]
        assert cycle["provenance"]
        assert cycle["state_before"] is not None
        assert cycle["state_after"] is not None


def test_learning_is_not_automatically_canonical() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert all(cycle["learning_status"] != "canonical" for cycle in data["cycles"])
    expected = {item["case"]: item["expected"] for item in data["learning_cases"]}
    assert expected["repeated_general_mechanic"] == "faculty_candidate"
    assert expected["tenant_specific_mechanic"] == "overlay"
    assert expected["missing_evidence"] == "gap"
    assert expected["incompatible_evidence"] == "conflict"


def test_governance_invariants_forbid_parallel_memory_authority() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    invariants = set(data["invariants"])
    assert "history_immutable" in invariants
    assert "context_derived" in invariants
    assert "promotion_requires_validation" in invariants
    assert "no_parallel_memory_authority" in invariants
