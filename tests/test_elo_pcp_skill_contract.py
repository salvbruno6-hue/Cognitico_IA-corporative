from pathlib import Path


SKILL = Path("docs/forge/skills/PCP_SKILL_UDEMY_APPLIED_KNOWLEDGE.md")


def _skill_text() -> str:
    assert SKILL.exists(), "PCP Skill Pack must exist"
    return SKILL.read_text(encoding="utf-8")


def test_pcp_skill_is_forge_owned_and_external_source_is_not_core_authority():
    text = _skill_text()
    assert "Forge PCP Specialist" in text
    assert "external learning source" in text
    assert "MUST NOT be copied into Core" in text
    assert "only generalized, validated learning" in text


def test_pcp_skill_contains_governed_planning_search_sequence():
    text = _skill_text()
    required = [
        "STEP 1 — Define the planning question",
        "STEP 2 — Search authorized enterprise sources",
        "STEP 3 — Build the planning fact base",
        "STEP 4 — Select the appropriate planning layer",
        "STEP 5 — Calculate feasibility",
        "STEP 6 — Identify gaps and request follow-up",
        "STEP 7 — Compare scenarios",
        "STEP 8 — Produce the planning result",
        "STEP 9 — Monitor and learn",
    ]
    for marker in required:
        assert marker in text, f"Missing governed PCP step: {marker}"


def test_pcp_skill_prioritizes_solution_relevant_methods():
    text = _skill_text()
    required = [
        "P1 — Demand and planning structure",
        "P2 — Capacity, sequencing and execution feasibility",
        "P3 — Materials and inventory",
        "P4 — Simulation and scenario analysis",
        "P5 — Monitoring and continuous improvement",
        "P6 — Lean and waste reduction",
        "DEMAND → AGGREGATE PLAN → MPS/PMP → MRP → CAPACITY → SEQUENCING → SCHEDULE",
    ]
    for marker in required:
        assert marker in text, f"Missing applied PCP capability: {marker}"


def test_mt001_unknowns_remain_gaps_instead_of_invented_facts():
    text = _skill_text()
    required = [
        "actual seasonal demand composition",
        "M01/M05/M14 quantities",
        "processing time for each module",
        "CLT availability and contractual allocation",
        "missing M14 processing time",
        "Missing information becomes GAP/follow-up",
    ]
    for marker in required:
        assert marker in text, f"MT-001 governance boundary missing: {marker}"


def test_pcp_skill_preserves_experience_and_governed_promotion():
    text = _skill_text()
    assert "The original experience remains in Forge" in text
    assert "Evolution Gate" in text
    assert "NOT_YET_EMPIRICALLY_VALIDATED_AS_ELO_SKILL" in text
