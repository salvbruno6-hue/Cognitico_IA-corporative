from pathlib import Path
import re


MIGRATIONS = Path("supabase/migrations")
BASELINE = "20261019061500_split_pcp_admin_write_policies.sql"
TARGET_TABLES = {
    "lista_mae",
    "modelos",
    "dimensoes",
    "kits",
    "kit_itens",
    "fluxo_produtivo_modular",
    "fluxo_produtivo_modular_etapas",
}
LEGACY_ALL_POLICIES = {
    "p_pcp_lista_mae_admin_write",
    "p_pcp_modelos_admin_write",
    "p_pcp_dimensoes_admin_write",
    "p_pcp_kits_admin_write",
    "p_pcp_kit_itens_admin_write",
    "p_pcp_fluxo_admin_write",
    "p_pcp_fluxo_etapas_admin_write",
}


def _future_migrations() -> list[Path]:
    return sorted(
        path
        for path in MIGRATIONS.glob("*.sql")
        if path.name > BASELINE
    )


def _executable(path: Path) -> str:
    return "\n".join(
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("--")
    )


def test_future_migrations_do_not_reintroduce_legacy_admin_write_policies() -> None:
    violations: list[str] = []
    for path in _future_migrations():
        sql = _executable(path).lower()
        for policy in LEGACY_ALL_POLICIES:
            if re.search(
                rf"\b(?:create|alter)\s+policy\s+{re.escape(policy.lower())}\b",
                sql,
                re.IGNORECASE,
            ):
                violations.append(f"{path.name}:{policy}")
    assert violations == []


def test_future_migrations_do_not_add_authenticated_for_all_to_guarded_tables() -> None:
    violations: list[str] = []
    pattern = re.compile(
        r"create\s+policy\s+([a-zA-Z0-9_]+)\s+on\s+(?:public\.)?([a-zA-Z0-9_]+)"
        r"(?:(?!;).)*?for\s+all\s+to\s+authenticated",
        re.IGNORECASE | re.DOTALL,
    )
    for path in _future_migrations():
        sql = _executable(path)
        for policy, table in pattern.findall(sql):
            if table.lower() in TARGET_TABLES:
                violations.append(f"{path.name}:{table}:{policy}")
    assert violations == []
