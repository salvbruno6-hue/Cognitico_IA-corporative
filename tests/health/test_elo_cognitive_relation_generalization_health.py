from pathlib import Path


SUMMARY = Path("supabase/health/elo_intuitive_health_summary.sql").read_text(encoding="utf-8").lower()


def test_health_summary_consumes_generalization_contract() -> None:
    assert "elo_learning.vw_cognitive_relation_generalization" in SUMMARY
    for token in (
        "generalization_unconfirmed",
        "generalization_partial",
        "generalization_confirmed",
        "ready_for_symbiont_review",
        "strengthen_relations",
        "blocked_relations",
    ):
        assert token in SUMMARY


def test_relation_health_is_fail_closed_for_blocked_candidates() -> None:
    assert "when blocked_relations>0 then 'block'" in SUMMARY
    assert "repair invalid/inactive relation endpoints" in SUMMARY


def test_confirmed_relations_route_to_review_not_auto_promotion() -> None:
    assert "when ready_for_symbiont_review>0 then 'promotion_review'" in SUMMARY
    assert "symbiont -> evolution gate -> governed learning" in SUMMARY
    assert "do not auto-promote" in SUMMARY


def test_unconfirmed_or_partial_relations_require_independent_evidence() -> None:
    assert "partial_relations>0 or unconfirmed_relations>0" in SUMMARY
    assert "collect and validate independent experiences explicitly referencing both relation endpoints" in SUMMARY
