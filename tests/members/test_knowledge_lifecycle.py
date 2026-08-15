import pytest

from members.faculty.knowledge_lifecycle import (
    KnowledgePromotionRecord,
    PromotionDecision,
    member_detached_knowledge_survives,
    validate_promotion,
)


def record(decision: PromotionDecision) -> KnowledgePromotionRecord:
    return KnowledgePromotionRecord(
        source_member="ELO-COMERCIAL-A",
        source_version="1.0",
        domain="COMERCIAL",
        knowledge_id="commercial-faculty-001",
        decision=decision,
        evidence_ref="evidence://commercial/a/001",
        reason="repeated validated mechanism",
        valid_from="2026-08-14T00:00:00Z",
    )


def test_promoted_knowledge_survives_member_detachment() -> None:
    assert member_detached_knowledge_survives(record(PromotionDecision.PROMOTE)) is True


def test_preserved_alternative_survives_member_detachment() -> None:
    assert member_detached_knowledge_survives(record(PromotionDecision.PRESERVE_ALTERNATIVE)) is True


def test_overlay_does_not_become_permanent_faculty() -> None:
    assert member_detached_knowledge_survives(record(PromotionDecision.OVERLAY)) is False


def test_promotion_requires_provenance() -> None:
    invalid = record(PromotionDecision.PROMOTE)
    invalid = KnowledgePromotionRecord(**{**invalid.__dict__, "evidence_ref": ""})
    with pytest.raises(ValueError, match="provenance"):
        validate_promotion(invalid)
