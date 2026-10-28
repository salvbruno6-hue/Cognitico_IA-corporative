from pathlib import Path


MIGRATION = Path(
    "supabase/migrations/20261028141000_mt_rls_duplicate_policy_consolidation.sql"
).read_text(encoding="utf-8").lower()


DROPPED = (
    "p_mt_eventos_reparo_append",
    "p_mt_eventos_reparo_read",
    "p_mt_lotes_estoque_insert",
    "p_mt_lotes_estoque_read",
    "p_mt_lotes_estoque_update",
    "p_mt_movimentacoes_estoque_append",
    "p_mt_movimentacoes_estoque_read",
    "p_mt_ordens_reparo_insert",
    "p_mt_ordens_reparo_read",
    "p_mt_ordens_reparo_update",
)

SURVIVORS = (
    "p_pcp_eventos_insert",
    "p_pcp_eventos_select",
    "p_pcp_lotes_insert",
    "p_pcp_lotes_select",
    "p_pcp_lotes_update",
    "p_pcp_mov_insert",
    "p_pcp_mov_select",
    "p_pcp_reparo_insert",
    "p_pcp_reparo_select",
    "p_pcp_reparo_update",
)


def test_only_exact_duplicate_mt_family_is_removed() -> None:
    for policy in DROPPED:
        assert f"drop policy if exists {policy}" in MIGRATION
    assert MIGRATION.count("drop policy if exists") == 10


def test_canonical_pcp_family_is_never_dropped() -> None:
    for policy in SURVIVORS:
        assert f"drop policy if exists {policy}" not in MIGRATION
        assert policy in MIGRATION


def test_migration_does_not_change_authorization_predicates_or_grants() -> None:
    forbidden = (
        "create policy",
        "alter policy",
        " grant ",
        " revoke ",
        "auth.uid()",
        "has_capability(",
        "using (",
        "with check (",
    )
    assert all(token not in MIGRATION for token in forbidden)
