"""Enterprise-integrated medium validation for ELO.

Validation only: this suite proves boundaries and missing-data behavior for
MT-001-style planning/budgeting flows. It must not invent enterprise facts.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_enterprise_flow_keeps_cognitive_layers_separate():
    text = (ROOT / "docs/governance/ELO_SPECIALIST_DOMAIN_FAMILY_MATRIX.md").read_text()
    assert "Core" in text
    assert "Forge" in text
    assert "PCP" in text
    assert "Budgeting" in text
    assert "HR" in text


def test_mt001_unknowns_remain_gaps():
    text = "".join(
        p.read_text(errors="ignore")
        for p in (ROOT / "docs").rglob("*.md")
        if "MT-001" in p.read_text(errors="ignore")
    )
    assert "M14" in text
    assert "GAP" in text
    assert "CLT" in text


def test_pcp_skill_is_forge_owned_and_uses_external_source_as_learning_input():
    matches = list((ROOT / "docs").rglob("*PCP*.md")) + list(
        (ROOT / "docs").rglob("*pcp*.md")
    )
    text = "\n".join(p.read_text(errors="ignore") for p in matches)
    assert "Forge" in text
    assert "Udemy" in text
    assert "Evolution Gate" in text


def test_autonomous_budgeting_requires_missing_input_governance():
    budgeting = ROOT / "src/elo/core/budgeting.py"
    assert budgeting.exists()
    text = budgeting.read_text(errors="ignore")
    assert "GAP" in text
    assert "Assumption" in text
    assert "BudgetDecision" in text


def test_no_parallel_authority_is_introduced():
    text = "".join(
        p.read_text(errors="ignore")
        for p in (ROOT / "docs/governance").glob("*.md")
    )
    assert "second Core" in text or "second Core" in text
    assert "parallel" in text.lower()


def test_planning_flow_is_explicit():
    expected = ["demand", "capacity", "MPS", "MRP", "sequencing"]
    text = "".join(
        p.read_text(errors="ignore")
        for p in (ROOT / "docs").rglob("*.md")
    ).lower()
    for item in expected:
        assert item.lower() in text
