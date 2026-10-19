from pathlib import Path

MIGRATION = Path(
    "supabase/migrations/20261019062400_remove_duplicate_calculation_indexes.sql"
)


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def _executable(sql: str) -> str:
    return "\n".join(
        line for line in sql.splitlines() if not line.lstrip().startswith("--")
    )


def test_only_legacy_duplicate_indexes_are_dropped() -> None:
    sql = _executable(_sql()).lower()
    assert "drop index if exists public.idx_elo_calc_aprendidos_hash;" in sql
    assert "drop index if exists public.idx_elo_calculos_aprendidos_memoria;" in sql
    assert sql.count("drop index") == 2


def test_canonical_later_indexes_are_preserved() -> None:
    sql = _executable(_sql()).lower()
    assert "drop index if exists public.idx_calculos_aprendidos_hash" not in sql
    assert "drop index if exists public.idx_calculos_aprendidos_memoria" not in sql


def test_cleanup_has_no_authorization_or_data_mutation() -> None:
    sql = _executable(_sql()).lower()
    for forbidden in (
        "insert ",
        "update ",
        "delete ",
        "grant ",
        "revoke ",
        "policy ",
        "row level security",
        "alter table",
    ):
        assert forbidden not in sql
