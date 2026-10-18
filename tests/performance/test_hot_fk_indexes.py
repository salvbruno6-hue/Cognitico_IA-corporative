from pathlib import Path
import re

MIGRATION = Path(
    "supabase/migrations/20261018204200_add_hot_fk_performance_indexes.sql"
)

EXPECTED = {
    ("idx_elo_orcamento_memoria_orcamento_id", "public.elo_orcamento_memoria", "orcamento_id"),
    ("idx_mt_ordens_reparo_unidade_modular_id", "public.mt_ordens_reparo", "unidade_modular_id"),
    ("idx_mt_ordens_reparo_tenant_id", "public.mt_ordens_reparo", "tenant_id"),
    ("idx_mt_ordens_reparo_nao_conformidade_id", "public.mt_ordens_reparo", "nao_conformidade_id"),
    ("idx_mt_ordens_reparo_aprovado_por", "public.mt_ordens_reparo", "aprovado_por"),
}


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def test_exactly_five_bounded_fk_indexes_are_created() -> None:
    sql = _sql()
    found = set(
        re.findall(
            r"CREATE\s+INDEX\s+IF\s+NOT\s+EXISTS\s+([a-zA-Z0-9_]+)\s+"
            r"ON\s+([a-zA-Z0-9_.]+)\s*\(\s*([a-zA-Z0-9_]+)\s*\)",
            sql,
            re.IGNORECASE,
        )
    )
    assert found == EXPECTED


def test_migration_is_index_only() -> None:
    executable = "\n".join(
        line for line in _sql().splitlines() if not line.lstrip().startswith("--")
    ).lower()
    for forbidden in (
        "alter table",
        "drop ",
        "delete ",
        "update ",
        "insert ",
        "create policy",
        "alter policy",
        "grant ",
        "revoke ",
    ):
        assert forbidden not in executable
    assert executable.count("create index if not exists") == 5
