from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MIGRATION = ROOT / "supabase/migrations/20261008000000_harden_legacy_security_definer_execute.sql"
SQL_REGRESSION = ROOT / "tests/security/test_elo_legacy_security_definer_execute.sql"

PRIVILEGED_FUNCTIONS = (
    "elo_aprendizado_classificar_experiencia",
    "elo_aprendizado_extrair_fontes",
    "elo_aprendizado_gerar_conceitos_e_padroes",
    "elo_aprendizado_gerar_relacoes",
)


def test_migration_revokes_data_api_execute_and_preserves_service_role():
    sql = MIGRATION.read_text(encoding="utf-8")

    for function_name in PRIVILEGED_FUNCTIONS:
        assert f"REVOKE ALL ON FUNCTION public.{function_name}" in sql
        assert "FROM PUBLIC, anon, authenticated;" in sql
        assert f"GRANT EXECUTE ON FUNCTION public.{function_name}" in sql
        assert "TO service_role;" in sql

    assert "REVOKE ALL ON FUNCTION public.lista_mae_guard()" in sql


def test_database_regression_assertions_cover_both_data_api_roles():
    sql = SQL_REGRESSION.read_text(encoding="utf-8")

    assert "has_function_privilege('anon', fn, 'EXECUTE')" in sql
    assert "has_function_privilege('authenticated', fn, 'EXECUTE')" in sql
    assert "has_function_privilege('service_role', fn, 'EXECUTE')" in sql

    for function_name in (*PRIVILEGED_FUNCTIONS, "lista_mae_guard"):
        assert function_name in sql
