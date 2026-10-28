from pathlib import Path


MIGRATION = Path(
    "supabase/migrations/20261028151000_index_hot_learning_fk_especializacao.sql"
).read_text(encoding="utf-8").lower()


def test_indexes_only_evidence_ranked_learning_fk() -> None:
    assert "idx_elo_aprendizado_conceitos_especializacao_id" in MIGRATION
    assert "elo_aprendizado_conceitos (especializacao_id)" in MIGRATION


def test_does_not_index_tiny_learning_tables_without_volume_evidence() -> None:
    assert "create index" in MIGRATION
    assert MIGRATION.count("create index") == 1
    assert "on public.elo_aprendizado_padroes_raciocinio" not in MIGRATION
    assert "on public.elo_aprendizado_pcp_planejamento" not in MIGRATION
    assert "on public.elo_aprendizado_producao_fluxo_modular" not in MIGRATION
