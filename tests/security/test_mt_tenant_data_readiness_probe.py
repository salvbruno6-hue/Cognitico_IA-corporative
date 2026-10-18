from pathlib import Path


PROBE = Path("supabase/health/elo_mt_tenant_data_readiness.sql")


def _source() -> str:
    return PROBE.read_text(encoding="utf-8").lower()


def test_tenant_data_probe_is_read_only() -> None:
    source = _source()
    assert "authz_mt_tenant_data_readiness" in source
    assert "gap_high" in source
    assert "mt_tenants" in source
    assert "tenant_id" in source

    for mutation in (
        "insert into ",
        "update public.",
        "delete from ",
        "alter table ",
        "create policy ",
        "alter policy ",
        "drop policy ",
        "grant ",
        "revoke ",
    ):
        assert mutation not in source


def test_tenant_data_probe_does_not_infer_or_backfill_tenant() -> None:
    source = _source()
    assert "does not create a" in source
    assert "infer ownership" in source
    assert "backfill tenant_id" in source
    assert "repair_rows_without_tenant" in source


def test_tenant_data_probe_keeps_estimates_distinct_from_exact_repair_truth() -> None:
    source = _source()
    assert "pg_stat_user_tables" in source
    assert "estimated_populated_tables" in source
    assert "repair_truth" in source
    assert "count(*) filter (where tenant_id is null)" in source
