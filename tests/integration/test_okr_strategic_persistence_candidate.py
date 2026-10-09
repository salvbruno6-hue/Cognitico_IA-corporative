from pathlib import Path


SQL_PATH = Path("docs/implementation/sql/ELO_OKR_STRATEGIC_PERSISTENCE_CANDIDATE.sql")


def _sql() -> str:
    return SQL_PATH.read_text(encoding="utf-8")


def test_candidate_creates_only_approved_objective_and_key_result_owners() -> None:
    sql = _sql().lower()

    assert "create table if not exists public.elo_strategic_objectives" in sql
    assert "create table if not exists public.elo_strategic_key_results" in sql
    assert "create table if not exists public.elo_strategic_measurements" not in sql
    assert "create table if not exists public.elo_okr_measurements" not in sql


def test_tenant_identity_is_part_of_both_primary_keys_and_objective_fk() -> None:
    sql = _sql()

    assert "primary key (tenant_id, objective_id)" in sql
    assert "primary key (tenant_id, key_result_id)" in sql
    assert "foreign key (tenant_id, objective_id)" in sql
    assert "references public.elo_strategic_objectives (tenant_id, objective_id)" in sql


def test_key_result_reuses_existing_formal_kpi_registry() -> None:
    sql = _sql()

    assert "foreign key (metric_code)" in sql
    assert "references public.mt_definicoes_kpi (codigo_kpi)" in sql
    assert "create table if not exists public.mt_definicoes_kpi" not in sql
    assert "create table if not exists public.mt_snapshots_kpi" not in sql


def test_baseline_target_and_approval_are_fail_closed() -> None:
    sql = _sql()

    assert "baseline is null or cardinality(baseline_evidence_refs) > 0" in sql
    assert "target is null or cardinality(target_evidence_refs) > 0" in sql
    assert "target_approval_state in ('DRAFT', 'APPROVED')" in sql
    assert "target_approval_state <> 'APPROVED'" in sql
    assert "nullif(btrim(target_approval_ref), '') is not null" in sql
    assert "check (weight > 0)" in sql


def test_data_api_surface_is_backend_only_and_rls_enabled() -> None:
    sql = _sql()

    assert "alter table public.elo_strategic_objectives enable row level security" in sql
    assert "alter table public.elo_strategic_key_results enable row level security" in sql
    assert "revoke all on table public.elo_strategic_objectives from anon, authenticated" in sql
    assert "revoke all on table public.elo_strategic_key_results from anon, authenticated" in sql
    assert "to service_role" in sql
    assert "create policy" not in sql.lower()
    assert "security definer" not in sql.lower()


def test_candidate_does_not_mutate_existing_kpi_snapshot_or_learning_owners() -> None:
    sql = _sql().lower()

    forbidden_mutations = (
        "alter table public.mt_definicoes_kpi",
        "alter table public.mt_snapshots_kpi",
        "insert into public.mt_definicoes_kpi",
        "insert into public.mt_snapshots_kpi",
        "update public.mt_definicoes_kpi",
        "update public.mt_snapshots_kpi",
        "delete from public.mt_definicoes_kpi",
        "delete from public.mt_snapshots_kpi",
        "create table if not exists public.elo_learning",
        "create table if not exists public.elo_symbiont",
    )

    for statement in forbidden_mutations:
        assert statement not in sql
