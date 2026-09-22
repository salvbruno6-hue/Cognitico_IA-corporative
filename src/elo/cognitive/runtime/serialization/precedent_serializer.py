"""Serialização de Precedent ↔ JSON."""
from __future__ import annotations
from typing import Any
from elo.core.precedent_index import Precedent

def to_dict(precedent: Precedent) -> dict[str, Any]:
    return {"decision_id": precedent.decision_id, "domain": precedent.domain, "context_keys": list(precedent.context_keys), "outcome_summary": precedent.outcome_summary, "evidence_ids": list(precedent.evidence_ids)}

def from_dict(data: dict[str, Any]) -> Precedent:
    return Precedent(decision_id=data["decision_id"], domain=data["domain"], context_keys=tuple(data["context_keys"]), outcome_summary=data["outcome_summary"], evidence_ids=tuple(data["evidence_ids"]))
