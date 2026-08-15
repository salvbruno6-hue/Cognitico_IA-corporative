"""Governed promotion metadata for knowledge learned from members."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PromotionDecision(str, Enum):
    PROMOTE = "PROMOTE"
    OVERLAY = "OVERLAY"
    PRESERVE_ALTERNATIVE = "PRESERVE_ALTERNATIVE"
    REJECT = "REJECT"


@dataclass(frozen=True)
class KnowledgePromotionRecord:
    source_member: str
    source_version: str
    domain: str
    knowledge_id: str
    decision: PromotionDecision
    evidence_ref: str
    reason: str
    valid_from: str
    valid_until: Optional[str] = None
    supersedes: Optional[str] = None


def validate_promotion(record: KnowledgePromotionRecord) -> None:
    """Reject promotion records that cannot be audited later."""
    required = {
        "source_member": record.source_member,
        "source_version": record.source_version,
        "domain": record.domain,
        "knowledge_id": record.knowledge_id,
        "evidence_ref": record.evidence_ref,
        "reason": record.reason,
        "valid_from": record.valid_from,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise ValueError(f"missing promotion provenance: {', '.join(missing)}")


def member_detached_knowledge_survives(record: KnowledgePromotionRecord) -> bool:
    """Promoted knowledge is owned by its ELO lifecycle record, not the member."""
    validate_promotion(record)
    return record.decision in {
        PromotionDecision.PROMOTE,
        PromotionDecision.PRESERVE_ALTERNATIVE,
    }
