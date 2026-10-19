from pathlib import Path
import re


MIGRATION = Path(
    "supabase/migrations/20261019061500_split_pcp_admin_write_policies.sql"
)

TABLE_POLICIES = {
    "lista_mae": "p_pcp_lista_mae",
    "modelos": "p_pcp_modelos",
    "dimensoes": "p_pcp_dimensoes",
    "kits": "p_pcp_kits",
    "kit_itens": "p_pcp_kit_itens",
    "fluxo_produtivo_modular": "p_pcp_fluxo",
    "fluxo_produtivo_modular_etapas": "p_pcp_fluxo_etapas",
}


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def _executable(sql: str) -> str:
    return "\n".join(
        line for line in sql.splitlines() if not line.lstrip().startswith("--")
    )


def test_only_the_seven_known_for_all_policies_are_dropped() -> None:
    sql = _executable(_sql())
    dropped = set(re.findall(r"DROP\s+POLICY\s+([a-zA-Z0-9_]+)", sql, re.IGNORECASE))
    assert dropped == {
        f"{prefix}_admin_write" for prefix in TABLE_POLICIES.values()
    }
    assert len(re.findall(r"DROP\s+POLICY\b", sql, re.IGNORECASE)) == 7


def test_each_table_gets_exactly_insert_update_delete_admin_policies() -> None:
    sql = _executable(_sql())
    created = re.findall(
        r"CREATE\s+POLICY\s+([a-zA-Z0-9_]+)\s+ON\s+public\.([a-zA-Z0-9_]+)\s+FOR\s+(INSERT|UPDATE|DELETE)\s+TO\s+authenticated",
        sql,
        re.IGNORECASE,
    )
    assert len(created) == 21

    by_table: dict[str, set[tuple[str, str]]] = {}
    for policy, table, command in created:
        by_table.setdefault(table.lower(), set()).add((policy.lower(), command.upper()))

    for table, prefix in TABLE_POLICIES.items():
        assert by_table[table] == {
            (f"{prefix}_admin_insert", "INSERT"),
            (f"{prefix}_admin_update", "UPDATE"),
            (f"{prefix}_admin_delete", "DELETE"),
        }


def test_migration_never_recreates_for_all_or_select_policy() -> None:
    sql = _executable(_sql()).lower()
    assert "for all" not in sql
    assert "for select" not in sql
    for prefix in TABLE_POLICIES.values():
        assert f"{prefix}_select" not in sql


def test_write_predicate_is_preserved_in_scalar_initplan_shape() -> None:
    sql = _executable(_sql())
    # Per table: INSERT has WITH CHECK (1), UPDATE has USING + WITH CHECK (2),
    # DELETE has USING (1). Seven tables therefore carry 28 predicate copies.
    assert sql.count("elo_private.has_capability('PCP_ADMIN'::text)") == 28
    assert sql.count("= 'admin'::text") == 28
    assert len(re.findall(r"\(\s*SELECT\s+auth\.jwt\(\)\s*\)", sql, re.IGNORECASE)) == 28

    without_wrapped = re.sub(
        r"\(\s*SELECT\s+auth\.jwt\(\)\s*\)",
        "",
        sql,
        flags=re.IGNORECASE,
    )
    assert "auth.jwt()" not in without_wrapped.lower()


def test_no_grant_revoke_or_rls_enablement_changes() -> None:
    sql = _executable(_sql()).lower()
    for forbidden in (
        "grant ",
        "revoke ",
        "enable row level security",
        "disable row level security",
        "force row level security",
    ):
        assert forbidden not in sql
