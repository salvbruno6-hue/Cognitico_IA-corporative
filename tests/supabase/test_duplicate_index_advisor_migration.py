from pathlib import Path


MIGRATION = Path("supabase/migrations/20260925160000_remove_duplicate_indexes_advisor.sql").read_text(encoding="utf-8")


DUPLICATE_INDEXES = [
    "ix_elo_orcamento_associacoes_lista_mae",
    "idx_elo_calc_aprendidos_hash",
    "idx_elo_calculos_aprendidos_memoria",
    "ix_elo_orcamento_decisoes_associacao",
    "ix_elo_orcamento_decisoes_orcamento",
]


CANONICAL_INDEXES = [
    "idx_elo_orc_lista_mae",
    "idx_calculos_aprendidos_hash",
    "idx_calculos_aprendidos_memoria",
    "idx_elo_orc_dec_associacao",
    "idx_elo_orc_dec_orcamento",
]


def test_migration_drops_only_advisor_identified_duplicates() -> None:
    drops = [f"DROP INDEX IF EXISTS public.{name};" for name in DUPLICATE_INDEXES]
    assert all(statement in MIGRATION for statement in drops)
    assert MIGRATION.count("DROP INDEX IF EXISTS") == len(DUPLICATE_INDEXES)


def test_migration_does_not_drop_preserved_canonical_indexes() -> None:
    for name in CANONICAL_INDEXES:
        assert f"DROP INDEX IF EXISTS public.{name};" not in MIGRATION


def test_migration_contains_no_application_data_mutation() -> None:
    upper = MIGRATION.upper()
    assert "INSERT INTO" not in upper
    assert "UPDATE " not in upper
    assert "DELETE FROM" not in upper
