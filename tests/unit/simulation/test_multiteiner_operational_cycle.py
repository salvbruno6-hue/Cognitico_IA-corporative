import json
from pathlib import Path


FIXTURE = Path(__file__).parents[2] / "fixtures" / "multiteiner_operational_cycle.json"


def test_multiteiner_fixture_preserves_governance_invariants() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    assert data["synthetic"] is True
    assert data["source_status"] == "controlled_fixture"
    assert len(data["cycles"]) >= 2
    assert all(cycle["execution"]["authorized"] is False for cycle in data["cycles"][:1])
    assert data["cycles"][1]["execution"]["authorized"] is True

    required = set(data["required_invariants"])
    assert {
        "no_new_core",
        "no_new_memory",
        "no_new_orchestrator",
        "no_new_organizational_seed",
        "tenant_boundary_preserved",
        "provenance_preserved",
        "management_view_is_not_absolute_truth",
        "execution_requires_authority",
        "unvalidated_knowledge_is_not_canonical",
    } <= required


def test_multiteiner_adversarial_cases_have_expected_outcomes() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected = {case["case"]: case["expected"] for case in data["adversarial_cases"]}

    assert expected["specialist_conflict"] == "conflicting"
    assert expected["insufficient_evidence"] == "inconclusive"
    assert expected["unauthorized_action"] == "blocked"
    assert expected["authorized_execution"] == "monitored"
    assert expected["faculty_vs_overlay"] == "classified_before_promotion"


def test_management_view_remains_observation_layer() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for cycle in data["cycles"]:
        assert cycle["management_view"]["authority"] == "observation_only"
