from pathlib import Path


SQL = Path("supabase/migrations/20261028152000_harden_pcp_read_rls_batch1.sql").read_text(encoding="utf-8").lower()


def test_predicate_requires_identity_capability_enterprise_and_domain() -> None:
    for token in (
        "elo_private.can_read_pcp_tenant",
        "i.auth_user_id = auth.uid()",
        "c.code = 'pcp_read'",
        "s.scope_type = 'enterprise'",
        "s.scope_key = t.codigo",
        "s.scope_type = 'domain'",
        "s.scope_key = 'pcp-lista-mae'",
    ):
        assert token in SQL


def test_batch_hardens_only_select_policies() -> None:
    assert "p_mt_planos_pcp_read" in SQL
    assert "p_mt_ordens_producao_read" in SQL
    assert "for select" in SQL
    assert "for update" not in SQL
    assert "for insert" not in SQL
    assert "for delete" not in SQL


def test_batch_removes_literal_true_from_target_selects() -> None:
    assert "using (true)" not in SQL
    assert "using (elo_private.can_read_pcp_tenant(tenant_id))" in SQL


def test_private_predicate_is_not_publicly_executable() -> None:
    assert "revoke all on function elo_private.can_read_pcp_tenant(uuid) from public" in SQL
    assert "grant execute on function elo_private.can_read_pcp_tenant(uuid) to authenticated" in SQL
