from pathlib import Path
import re


MIGRATION = Path(
    "supabase/migrations/20261028102000_authorize_multiteiner_pcp_read.sql"
).read_text(encoding="utf-8")


def test_reuses_canonical_scopes_and_verified_google_identity() -> None:
    source = MIGRATION.lower()
    assert "provider = 'google'" in source
    assert "authorized_email" in source
    assert "auth.users" in source
    assert "scope_type = 'enterprise'" in source
    assert "scope_key = 'multiteiner'" in source
    assert "scope_type = 'domain'" in source
    assert "scope_key = 'pcp-lista-mae'" in source


def test_grants_only_read_capability_through_existing_role() -> None:
    source = MIGRATION.lower()
    assert "code = 'elo_admin'" in source
    assert "code = 'pcp_read'" in source
    assert "insert into public.elo_role_capabilities" in source
    assert "pcp_update" in source  # documented explicit non-goal
    assert "lista_mae_insert" in source  # documented explicit non-goal
    assert "code = 'pcp_update'" not in source
    assert "code = 'lista_mae_insert'" not in source
    assert "insert into public.elo_roles" not in source
    assert "insert into public.elo_capabilities" not in source
    assert "insert into public.elo_scopes" not in source


def test_is_fail_closed_and_idempotent() -> None:
    source = MIGRATION.lower()
    assert "expected exactly 1 eligible verified google identity" in source
    assert "elo_admin is not exclusively bound" in source
    assert source.count("on conflict do nothing") == 2
    assert "where not exists" in source
    assert "authorize_mt_pcp_read" in source


def test_contains_no_hardcoded_uuid_or_rls_rewrite() -> None:
    assert not re.search(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
        MIGRATION,
        re.IGNORECASE,
    )
    source = MIGRATION.lower()
    assert "create policy" not in source
    assert "drop policy" not in source
    assert "alter policy" not in source
    assert "grant " not in source
    assert "revoke " not in source
