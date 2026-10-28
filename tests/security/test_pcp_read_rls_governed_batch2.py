from pathlib import Path


SQL = Path("supabase/migrations/20261028153000_harden_pcp_read_rls_batch2.sql").read_text(encoding="utf-8").lower()


def test_plan_line_read_delegates_to_parent_tenant_authorization() -> None:
    for token in (
        "elo_private.can_read_pcp_plan",
        "from public.mt_planos_pcp p",
        "p.id = p_plan_id",
        "elo_private.can_read_pcp_tenant(p.tenant_id)",
    ):
        assert token in SQL


def test_batch_hardens_only_select_policy() -> None:
    assert "p_mt_linhas_plano_pcp_read" in SQL
    assert "for select" in SQL
    assert "for update" not in SQL
    assert "for insert" not in SQL
    assert "for delete" not in SQL
    assert "using (true)" not in SQL


def test_child_predicate_is_not_publicly_executable() -> None:
    assert "revoke all on function elo_private.can_read_pcp_plan(uuid) from public" in SQL
    assert "grant execute on function elo_private.can_read_pcp_plan(uuid) to authenticated" in SQL
