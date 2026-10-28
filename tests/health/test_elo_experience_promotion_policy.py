from pathlib import Path


MIGRATION = Path(
    "supabase/migrations/20261028113500_elo_govern_experience_promotion_policy.sql"
).read_text(encoding="utf-8").lower()


def test_promotion_policy_fails_closed_on_semantic_conflict() -> None:
    assert "vw_experience_promotion_policy" in MIGRATION
    assert "governance_required" in MIGRATION
    assert "autonomous_threshold_selection" in MIGRATION
    assert "false as autonomous_threshold_selection" in MIGRATION
    assert "semantic_status = 'match'" in MIGRATION


def test_refresh_runtime_uses_governed_policy_not_physical_threshold_table() -> None:
    function_start = MIGRATION.index("create or replace function public.elo_refresh_learner_profile")
    function_sql = MIGRATION[function_start:]
    assert "from elo_learning.vw_experience_promotion_policy" in function_sql
    assert "from public.elo_experience_level_transitions" not in function_sql
    assert "from public.elo_experiencia_transicoes" not in function_sql


def test_conflict_path_does_not_mutate_profile() -> None:
    assert "'mutated', false" in MIGRATION
    governance_pos = MIGRATION.index("if policy.policy_status <> 'ready'")
    update_pos = MIGRATION.index("update public.elo_learner_profiles")
    assert governance_pos < update_pos


def test_phase_two_preserves_physical_tables_and_thresholds() -> None:
    forbidden = (
        "drop table",
        "truncate ",
        "delete from public.elo_experience_level_transitions",
        "delete from public.elo_experiencia_transicoes",
        "update public.elo_experience_level_transitions",
        "update public.elo_experiencia_transicoes",
    )
    assert all(token not in MIGRATION for token in forbidden)


def test_policy_view_uses_security_invoker() -> None:
    assert "with (security_invoker = true)" in MIGRATION
