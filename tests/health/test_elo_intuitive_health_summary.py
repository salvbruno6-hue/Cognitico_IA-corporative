from pathlib import Path


SUMMARY = Path("supabase/health/elo_intuitive_health_summary.sql").read_text(encoding="utf-8")


def test_health_summary_is_read_only() -> None:
    upper = SUMMARY.upper()
    forbidden = (
        "CREATE TABLE",
        "CREATE VIEW",
        "ALTER TABLE",
        "DROP TABLE",
        "DROP VIEW",
        "INSERT INTO",
        "UPDATE ",
        "DELETE FROM",
        "GRANT ",
        "REVOKE ",
        "TRUNCATE ",
    )
    assert all(token not in upper for token in forbidden)


def test_health_summary_covers_systemic_signals() -> None:
    required = (
        "DATABASE_RLS",
        "MT_AUTHORIZATION",
        "RLS_POLICY_DUPLICATION",
        "FK_PERFORMANCE",
        "COGNITIVE_EXPERIENCE_MODEL",
        "OBJECTIVE_CONTINUITY",
        "CAPABILITIES",
        "COGNITIVE_RELATIONS",
    )
    assert all(signal in SUMMARY for signal in required)


def test_health_summary_reuses_existing_owners() -> None:
    required_objects = (
        "elo_objective_continuity_checkpoints",
        "elo_capabilities",
        "elo_conhecimento_itens",
        "elo_conhecimento_vinculos",
        "elo_cognitive_relations",
        "elo_experience_level_transitions",
        "elo_experiencia_transicoes",
    )
    assert all(name in SUMMARY for name in required_objects)


def test_experience_conflict_is_detected_from_material_thresholds() -> None:
    for field in (
        "min_validated_experiences",
        "experiencias_minimas",
        "min_confidence",
        "confianca_minima",
        "required_independent_decisions",
        "decisoes_independentes_minimas",
        "min_domain_depth",
        "profundidade_minima",
    ):
        assert field in SUMMARY
