"""Serialização de DecisionLifecycle ↔ JSON.

Não cria API paralela ao Core. Apenas converte o estado para JSON e o reconstrói usando API pública.

Refs: ADR-0014, ADR-0015.
"""
from __future__ import annotations
from datetime import datetime
from typing import Any
from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState, DecisionTransition
from elo.core.systemic_primitives import DecisionRecord, OutcomeFeedback

def serialize(lifecycle: DecisionLifecycle) -> dict[str, Any]:
    return {
        "canonical_key": lifecycle.decision.decision_id,
        "decision": {
            "decision_id": lifecycle.decision.decision_id,
            "decision": lifecycle.decision.decision,
            "rationale": lifecycle.decision.rationale,
            "impact": list(lifecycle.decision.impact),
            "evidence_ids": list(lifecycle.decision.evidence_ids),
            "authority": lifecycle.decision.authority,
            "expected_outcome": lifecycle.decision.expected_outcome,
        },
        "state": lifecycle.state.value,
        "outcome": _outcome_to_dict(lifecycle.outcome),
        "attribution": dict(lifecycle.attribution),
        "learning_candidate": dict(lifecycle.learning_candidate) if lifecycle.learning_candidate is not None else None,
        "history": [_transition_to_dict(t) for t in lifecycle.history],
    }

def deserialize(data: dict[str, Any]) -> DecisionLifecycle:
    record = DecisionRecord(
        decision_id=data["decision"]["decision_id"],
        decision=data["decision"]["decision"],
        rationale=data["decision"]["rationale"],
        impact=tuple(data["decision"].get("impact", ())),
        evidence_ids=tuple(data["decision"].get("evidence_ids", ())),
        authority=data["decision"].get("authority"),
        expected_outcome=data["decision"].get("expected_outcome"),
    )
    outcome = _outcome_from_dict(data.get("outcome"))
    return DecisionLifecycle(
        decision=record,
        state=DecisionState(data["state"]),
        outcome=outcome,
        attribution=dict(data.get("attribution", {})),
        learning_candidate=data.get("learning_candidate"),
    )

def _outcome_to_dict(outcome: OutcomeFeedback | None) -> dict[str, Any] | None:
    if outcome is None:
        return None
    return {
        "decision_id": outcome.decision_id,
        "expected": outcome.expected,
        "observed": outcome.observed,
        "variance": outcome.variance,
        "evidence_ids": list(outcome.evidence_ids),
        "observed_at": outcome.observed_at.isoformat() if outcome.observed_at else None,
    }

def _outcome_from_dict(data: dict[str, Any] | None) -> OutcomeFeedback | None:
    if not data:
        return None
    return OutcomeFeedback(
        decision_id=data["decision_id"],
        expected=data["expected"],
        observed=data["observed"],
        variance=data.get("variance"),
        evidence_ids=tuple(data.get("evidence_ids", ())),
        observed_at=datetime.fromisoformat(data["observed_at"]) if data.get("observed_at") else None,
    )

def _transition_to_dict(t: DecisionTransition) -> dict[str, Any]:
    return {
        "decision_id": t.decision_id,
        "from_state": t.from_state.value,
        "to_state": t.to_state.value,
        "occurred_at": t.occurred_at.isoformat(),
        "evidence_ids": list(t.evidence_ids),
        "actor": t.actor,
    }
