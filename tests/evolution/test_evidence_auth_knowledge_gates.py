from pathlib import Path


def test_evidence_guard_is_present_in_canonical_learning_governance() -> None:
    text = Path("src/elo/core/learning_governance.py").read_text(encoding="utf-8")
    assert "evidence_ids" in text
    assert "evidence_missing" in text
    assert "human approval is required for promotion" in text


def test_symbiont_runtime_requires_material_evolution_before_learning() -> None:
    text = Path("src/elo/cognitive/budget_symbiont_runtime.py").read_text(encoding="utf-8")
    assert "evolution_impact.validate()" in text
    assert "SymbiontLabAdapter" in text
    assert "ExecutionRouter" in text


def test_authz_audits_allow_and_deny_paths() -> None:
    text = Path("supabase/functions/elo-authz/index.ts").read_text(encoding="utf-8")
    assert "elo_authorization_audit" in text
    assert '"ALLOW"' in text
    assert '"DENY"' in text
    assert "active_elo_session_required" in text
    assert "repository_out_of_scope" in text


def test_knowledge_links_are_not_auto_created_by_runtime() -> None:
    text = Path("src/elo/cognitive/symbionte_lab.py").read_text(encoding="utf-8")
    assert "existing_owner" in text
    assert "DUPLICATE_SUPERSEDED" in text
    assert "LAB_ONLY" in text
