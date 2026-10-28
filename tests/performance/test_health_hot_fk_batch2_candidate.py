from pathlib import Path


SQL = Path("docs/implementation/sql/ELO_HEALTH_HOT_FK_BATCH2_CANDIDATE.sql").read_text(encoding="utf-8")


EXPECTED_INDEXES = {
    "idx_mt_unidades_modulares_ordem_producao_id": "mt_unidades_modulares (ordem_producao_id)",
    "idx_mt_unidades_modulares_modelo_id": "mt_unidades_modulares (modelo_id)",
    "idx_mt_unidades_modulares_pedido_venda_item_id": "mt_unidades_modulares (pedido_venda_item_id)",
    "idx_mt_unidades_modulares_local_atual_id": "mt_unidades_modulares (local_atual_id)",
    "idx_elo_automation_runs_automation_id": "elo_automation_runs (automation_id)",
}


def test_candidate_contains_exact_bounded_index_batch() -> None:
    assert SQL.upper().count("CREATE INDEX IF NOT EXISTS") == len(EXPECTED_INDEXES)
    for index_name, target in EXPECTED_INDEXES.items():
        assert index_name in SQL
        assert target in SQL


def test_candidate_does_not_mutate_application_or_authorization_state() -> None:
    upper = SQL.upper()
    forbidden = (
        "INSERT INTO",
        "UPDATE ",
        "DELETE FROM",
        "ALTER TABLE",
        "DROP POLICY",
        "CREATE POLICY",
        "GRANT ",
        "REVOKE ",
        "DROP TABLE",
    )
    assert all(token not in upper for token in forbidden)


def test_candidate_does_not_try_to_fix_all_advisor_findings() -> None:
    assert "145" not in SQL
    assert "CREATE INDEX IF NOT EXISTS" in SQL
