import json
from pathlib import Path


FIXTURE = Path(__file__).parent / "fixtures" / "elo_018_cycle_memory.json"


def load_cycles():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return payload["cycles"]


def relationship_report(cycles):
    by_id = {cycle["cycle_id"]: cycle for cycle in cycles}
    report = []
    for cycle in cycles:
        parent = by_id.get(cycle.get("parent_cycle_id"))
        report.append(
            {
                "decision": cycle["decision"],
                "cycle": cycle["cycle_id"],
                "specialists": cycle["specialists"],
                "evidence": cycle["evidence"],
                "premise": cycle["state_before"],
                "dependencies": cycle.get("parent_cycle_id"),
                "impact": cycle["outcome"],
                "authority": cycle["authority"],
                "action": cycle["action"],
                "result": cycle["state_after"],
                "status": cycle["learning_status"],
                "previous_decision": parent["decision"] if parent else None,
                "derived_from_cycle": parent["cycle_id"] if parent else None,
            }
        )
    return report


def test_decision_relationship_report_preserves_cycle_chain():
    report = relationship_report(load_cycles())
    assert [row["cycle"] for row in report] == ["C1", "C2", "C3"]
    assert report[1]["previous_decision"] == "supported"
    assert report[2]["previous_decision"] == "supported_with_impact"


def test_decision_relationships_preserve_specialist_and_evidence_provenance():
    report = relationship_report(load_cycles())
    assert "comercial" in report[0]["specialists"]
    assert "orcamento" in report[1]["specialists"]
    assert report[0]["evidence"] == ["fixture:demand:D1"]
    assert report[2]["evidence"] == ["fixture:result:R1"]


def test_decision_relationship_report_distinguishes_authority_and_action():
    report = relationship_report(load_cycles())
    assert report[0]["authority"] == "analysis_only"
    assert report[1]["authority"] == "authorized"
    assert report[0]["action"] == "handoff"
    assert report[1]["action"] == "recalculate_and_monitor"


def test_decision_relationship_report_links_change_to_outcome():
    report = relationship_report(load_cycles())
    assert report[1]["impact"] == "impact_propagated"
    assert report[1]["result"]["plan"] == "P2"
    assert report[1]["result"]["budget"] == "B2"
    assert report[2]["status"] == "faculty_candidate"


def test_decision_relationship_report_is_derived_not_mutating_history():
    cycles = load_cycles()
    before = json.dumps(cycles, sort_keys=True)
    report = relationship_report(cycles)
    after = json.dumps(cycles, sort_keys=True)
    assert report
    assert before == after


def test_decision_relationship_report_flags_conflict_cases_explicitly():
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    learning = {case["case"]: case["expected"] for case in payload["learning_cases"]}
    assert learning["incompatible_evidence"] == "conflict"
    assert learning["missing_evidence"] == "gap"
    assert learning["tenant_specific_mechanic"] == "overlay"
    assert learning["repeated_general_mechanic"] == "faculty_candidate"
