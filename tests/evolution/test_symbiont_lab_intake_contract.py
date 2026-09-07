from pathlib import Path


def test_symbiont_lab_intake_is_candidate_only():
    path = Path("docs/evolution/SIMBIONTE_LAB_INTAKE_2026-09-06.md")
    text = path.read_text(encoding="utf-8")
    assert "CANDIDATE-ONLY" in text
    assert "não cria novo Core" in text
    assert "não promove aprendizado automaticamente" in text
    assert "Evolution Gate" in text


def test_symbiont_lab_has_explicit_evidence_boundary():
    text = Path("docs/evolution/SIMBIONTE_LAB_INTAKE_2026-09-06.md").read_text(encoding="utf-8")
    for marker in (
        "source_ref",
        "source_commit",
        "tenant_scope",
        "evidence_refs",
        "baseline",
        "experiment",
        "result",
        "generalization_status",
        "risk",
        "promotion_state",
    ):
        assert marker in text


def test_symbiont_lab_preserves_unknown_conflict_and_blocked_states():
    text = Path("docs/evolution/SIMBIONTE_LAB_INTAKE_2026-09-06.md").read_text(encoding="utf-8")
    assert "GAP | UNKNOWN | CONFLICT | BLOCKED" in text
    assert "Conflitos devem ser preservados como conflito" in text


def test_symbiont_lab_keeps_canonical_authorities_outside_its_ownership():
    text = Path("docs/evolution/SIMBIONTE_LAB_INTAKE_2026-09-06.md").read_text(encoding="utf-8")
    for authority in (
        "Soul",
        "Core",
        "ExecutionRouter",
        "Evolution Gate",
        "canonical write boundary",
        "aprovação humana",
    ):
        assert authority in text
