from pathlib import Path


MIGRATION = Path(
    "supabase/migrations/20261028144500_elo_cognitive_relation_generalization_contract.sql"
).read_text(encoding="utf-8").lower()


def test_generalization_reuses_existing_learning_owners() -> None:
    for owner in (
        "elo_aprendizado_relacoes",
        "elo_aprendizado_experiencias",
        "elo_aprendizado_conceitos",
        "elo_aprendizado_padroes_raciocinio",
    ):
        assert owner in MIGRATION
    assert "create table" not in MIGRATION


def test_only_validated_or_incorporated_experiences_count() -> None:
    assert "status_validacao in ('validada', 'incorporada')" in MIGRATION
    assert "'observada'" not in MIGRATION
    assert "'candidata'" not in MIGRATION
    assert "'em_validacao'" not in MIGRATION


def test_generalization_requires_two_independent_source_contexts() -> None:
    assert "count(distinct ve.source_reference)" in MIGRATION
    assert "independent_validated_contexts >= 2" in MIGRATION
    assert "when independent_validated_contexts = 1 then 'partial'" in MIGRATION
    assert "else 'unconfirmed'" in MIGRATION


def test_evidence_must_reference_both_relation_endpoints_explicitly() -> None:
    assert MIGRATION.count("jsonb_path_query") == 2
    assert "= rc.source_code" in MIGRATION
    assert "= rc.target_code" in MIGRATION


def test_contract_is_fail_closed_and_non_authoritative() -> None:
    assert "when not relation_active then 'block'" in MIGRATION
    assert "when source_code is null or target_code is null then 'block'" in MIGRATION
    assert "ready_for_symbiont_review" in MIGRATION
    assert "false as canonical_mutation_allowed" in MIGRATION
    forbidden = (
        "insert into",
        "update public.elo_aprendizado_relacoes",
        "delete from",
        "truncate ",
        "drop table",
    )
    assert all(token not in MIGRATION for token in forbidden)


def test_view_uses_security_invoker() -> None:
    assert "with (security_invoker = true)" in MIGRATION
