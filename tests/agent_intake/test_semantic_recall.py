"""Controlled evaluation of semantic recall attached to ELO Memory."""

from elo.agent_intake.semantic_recall import evaluate_semantic_recall_adaptation, semantic_recall


def test_semantic_recall_ranks_relevant_records_within_tenant():
    records = (
        {"id": "a", "tenant_scope": "multiteiner", "text": "memory semantic recall context"},
        {"id": "b", "tenant_scope": "multiteiner", "text": "unrelated production note"},
        {"id": "c", "tenant_scope": "multiteiner", "text": "semantic memory retrieval"},
    )
    result = semantic_recall(request_id="semantic-001", tenant_scope="multiteiner", query="semantic memory", records=records)
    assert result.capability_id == "HERMES-MEMORY"
    assert result.matched_ids == ("a", "c")
    assert result.status == "completed"
    assert result.learning_candidate == {"promotion_state": "candidate_only", "canonical_mutation": False}


def test_semantic_recall_never_crosses_tenant_boundary():
    records = (
        {"id": "allowed", "tenant_scope": "multiteiner", "text": "semantic memory"},
        {"id": "foreign", "tenant_scope": "other", "text": "semantic memory"},
    )
    result = semantic_recall(request_id="semantic-002", tenant_scope="multiteiner", query="semantic memory", records=records)
    assert result.matched_ids == ("allowed",)
    assert "foreign" not in result.matched_ids


def test_semantic_recall_is_deterministic_and_does_not_mutate_records():
    records = (
        {"id": "b", "tenant_scope": "multiteiner", "text": "memory semantic"},
        {"id": "a", "tenant_scope": "multiteiner", "text": "memory semantic"},
    )
    before = tuple(dict(record) for record in records)
    first = semantic_recall(request_id="semantic-003", tenant_scope="multiteiner", query="memory semantic", records=records, top_k=2)
    second = semantic_recall(request_id="semantic-003", tenant_scope="multiteiner", query="memory semantic", records=records, top_k=2)
    assert first == second
    assert records == before


def test_no_match_is_not_learning_evidence():
    result = semantic_recall(
        request_id="semantic-004",
        tenant_scope="multiteiner",
        query="missing topic",
        records=({"id": "a", "tenant_scope": "multiteiner", "text": "known subject"},),
    )
    assert result.status == "no_match"
    assert result.matched_ids == ()
    assert result.learning_candidate["canonical_mutation"] is False


def test_adaptation_is_repeatable_without_promotion():
    records = (
        {"id": "retention", "tenant_scope": "multiteiner", "text": "context memory retention"},
        {"id": "other", "tenant_scope": "multiteiner", "text": "production cost note"},
    )
    result = evaluate_semantic_recall_adaptation(
        tenant_scope="multiteiner",
        query="context memory recall",
        records=records,
        target_id="retention",
        top_k=2,
    )
    assert result.capability_id == "HERMES-MEMORY"
    assert result.baseline_target_hit is True
    assert result.adapted_target_hit is True
    assert result.gain == 0
    assert result.repeatable is True
    assert result.regression is False
    assert result.learning_candidate == {"promotion_state": "candidate_only", "canonical_mutation": False}


def test_adaptation_exposes_target_retrieval_gain_for_controlled_paraphrase():
    records = (
        {"id": "retrieval", "tenant_scope": "multiteiner", "text": "retrieval"},
        {"id": "other", "tenant_scope": "multiteiner", "text": "production cost"},
    )
    result = evaluate_semantic_recall_adaptation(
        tenant_scope="multiteiner",
        query="recall",
        records=records,
        target_id="retrieval",
        top_k=1,
    )
    assert result.baseline_matches == ()
    assert result.adapted_matches == ("retrieval",)
    assert result.baseline_target_hit is False
    assert result.adapted_target_hit is True
    assert result.gain == 1
    assert result.repeatable is True
    assert result.regression is False
