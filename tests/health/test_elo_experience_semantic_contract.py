from pathlib import Path


MIGRATION = Path(
    "supabase/migrations/20261028111500_elo_experience_semantic_contract.sql"
).read_text(encoding="utf-8").lower()
HEALTH = Path(
    "supabase/health/elo_experience_semantic_health.sql"
).read_text(encoding="utf-8").lower()


def test_shared_level_semantics_have_one_read_contract() -> None:
    assert "vw_experience_level_contract" in MIGRATION
    assert "canonical_level_owner" in MIGRATION
    assert "'elo_experiencia_niveis'" in MIGRATION
    assert "compatibility_level_owner" in MIGRATION
    assert "'elo_experience_levels'" in MIGRATION
    assert "create or replace function public.elo_level_order" in MIGRATION
    assert "from elo_learning.vw_experience_level_contract" in MIGRATION


def test_threshold_conflict_is_visible_but_not_promotion_authority() -> None:
    assert "vw_experience_transition_contract" in MIGRATION
    assert "governed_conflict" in MIGRATION
    assert "false as canonical_promotion_authority" in MIGRATION
    assert "symbiont -> evolution gate -> governed learning -> required approval" in MIGRATION


def test_phase_one_is_non_destructive_and_does_not_rewrite_promotion_runtime() -> None:
    forbidden = (
        "drop table",
        "drop view",
        "drop function",
        "truncate ",
        "delete from",
        "update public.elo_experience_level_transitions",
        "update public.elo_experiencia_transicoes",
        "elo_refresh_learner_profile(",
    )
    assert all(token not in MIGRATION for token in forbidden)


def test_views_use_security_invoker() -> None:
    assert MIGRATION.count("with (security_invoker = true)") == 2


def test_health_probe_is_fail_closed_for_incomplete_transition_contract() -> None:
    assert "missing_counterparts" in HEALTH
    assert "semantic_status = 'pt_only'" in HEALTH
    assert "total = 0" in HEALTH
    assert "when matched = total then 'healthy'" in HEALTH
    assert "when total = 0 or missing_counterparts > 0 then 'review'" in HEALTH
