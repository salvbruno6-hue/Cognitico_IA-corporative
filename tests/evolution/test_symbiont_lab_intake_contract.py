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


def test_symbionte_external_intake_preserves_source_authority():
    text = Path("docs/architecture/SIMBIONTE_EXTERNAL_INTAKE_BOUNDARY.md").read_text(encoding="utf-8")
    assert "AUTHORIZED SOURCE → OBSERVE → UNDERSTAND → RELATE → ASSESS UTILITY → CANDIDATE → GOVERN" in text
    assert "A fonte continua funcionando normalmente" in text
    assert "A Simbionte não controla o source" not in text


def test_symbionte_external_intake_keeps_figma_as_design_only():
    text = Path("docs/architecture/SIMBIONTE_EXTERNAL_INTAKE_BOUNDARY.md").read_text(encoding="utf-8")
    assert "Figma remains an authorized design/UX surface." in text
    assert "ELO Web implementation" in text
    assert "GitHub/Main" in text
    assert "deployment" in text


def test_symbionte_external_intake_forbids_automatic_assimilation():
    text = Path("docs/architecture/SIMBIONTE_EXTERNAL_INTAKE_BOUNDARY.md").read_text(encoding="utf-8")
    assert "No automatic assimilation" in text
    assert "EVOLUTION_GATE" in text
    assert "POSSIBLE ASSIMILATION" in text
