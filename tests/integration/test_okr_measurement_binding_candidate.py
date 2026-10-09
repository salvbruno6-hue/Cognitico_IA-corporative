from pathlib import Path


SQL_PATH = Path("docs/implementation/sql/ELO_OKR_MEASUREMENT_BINDING_CANDIDATE.sql")


def _sql() -> str:
    return SQL_PATH.read_text(encoding="utf-8").lower()


def test_m2_candidate_creates_binding_owner_only() -> None:
    sql = _sql()

    assert "create table if not exists public.elo_strategic_kr_snapshot_bindings" in sql
    assert "references public.elo_strategic_key_results (tenant_id, key_result_id)" in sql
    assert "references public.mt_snapshots_kpi (id)" in sql
    assert "unique (tenant_id, key_result_id, snapshot_id)" in sql
    assert "cardinality(evidence_refs) > 0" in sql
    assert "authorization_ref text not null" in sql
    assert "elo_strategic_kr_snapshot_bindings_authorization_required" in sql


def test_m2_candidate_does_not_mutate_existing_kpi_owners() -> None:
    sql = _sql()

    forbidden = (
        "alter table public.mt_snapshots_kpi",
        "alter table public.mt_definicoes_kpi",
        "insert into public.mt_snapshots_kpi",
        "insert into public.mt_definicoes_kpi",
        "update public.mt_snapshots_kpi",
        "update public.mt_definicoes_kpi",
        "delete from public.mt_snapshots_kpi",
        "delete from public.mt_definicoes_kpi",
    )
    for statement in forbidden:
        assert statement not in sql


def test_m2_candidate_is_backend_only_and_rls_fail_closed() -> None:
    sql = _sql()

    assert "enable row level security" in sql
    assert "revoke all on table public.elo_strategic_kr_snapshot_bindings from anon, authenticated" in sql
    assert "grant select, insert, update, delete on table public.elo_strategic_kr_snapshot_bindings to service_role" in sql
    assert "create policy" not in sql
