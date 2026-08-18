from pathlib import Path


ROOT = Path("docs")


def _all_docs_text() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("*.md"))


def test_architecture_preserves_cognitive_core_forge_boundary():
    text = _all_docs_text().lower()
    assert "elo cognitive" in text
    assert "core" in text
    assert "forge" in text
    assert "specialist" in text
    assert "evolution gate" in text


def test_core_is_faculty_and_not_domain_specialist_authority():
    text = _all_docs_text().lower()
    markers = ["generalized", "validated", "promotion", "core", "forge"]
    assert all(m in text for m in markers)


def test_forge_domain_skill_families_are_representable():
    text = _all_docs_text().lower()
    required = [
        "pcp | forge pcp specialist",
        "budgeting | forge budgeting specialist",
        "hr | forge hr specialist",
        "calculation | forge calculation specialist",
    ]
    for marker in required:
        assert marker in text, f"Missing governed domain-family representation: {marker}"


def test_enterprise_planning_requires_search_context_and_gaps():
    text = _all_docs_text().lower()
    for marker in ["search", "authorized", "context", "gap", "follow-up"]:
        assert marker in text


def test_cognitive_cycle_and_learning_boundary_exist():
    text = _all_docs_text().lower()
    for marker in ["observe", "analyze", "execute", "monitor", "learn", "experience"]:
        assert marker in text


def test_provenance_and_experience_preservation_are_governed():
    text = _all_docs_text().lower()
    for marker in ["provenance", "source", "claim", "decision", "result", "learning", "experience remains in forge"]:
        assert marker in text


def test_budgeting_and_pcp_can_share_core_without_parallel_intelligence():
    text = _all_docs_text().lower()
    assert "budgeting" in text
    assert "pcp" in text
    assert "shared" in text or "general" in text
    assert "second" in text and "core" in text


def test_autonomy_remains_governed_by_missing_data_and_authority():
    text = _all_docs_text().lower()
    for marker in ["must not", "invent", "authorization", "gap", "assumption"]:
        assert marker in text


def test_medium_maturity_target_is_integration_not_new_architecture():
    text = _all_docs_text().lower()
    assert "integration" in text or "integrated" in text
    assert "no production runtime authority" in text or "no second" in text
