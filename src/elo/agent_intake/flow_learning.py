"""Persistent, non-canonical learning for ELO flow complementarity.

The learning store records relation observations and outcomes so ELO can adapt
future routing evidence without promoting observations directly to canonical
authority. Persistence is append-only; adaptation produces a candidate view.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class FlowOutcomeRecord:
    relation_id: str
    origin_flow: str
    target_flow: str
    outcome: str
    success: bool
    evidence_refs: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    metrics: tuple[tuple[str, float], ...] = ()


@dataclass(frozen=True, slots=True)
class FlowAdaptation:
    relation_id: str
    observations: int
    successes: int
    success_rate: float
    status: str


class FlowLearningStore(Protocol):
    def append(self, record: FlowOutcomeRecord) -> None: ...
    def history(self, relation_id: str) -> tuple[FlowOutcomeRecord, ...]: ...


class SQLiteFlowLearningStore:
    """Small append-only persistent store for complementarity outcomes."""

    def __init__(self, path: str | Path) -> None:
        self._path = str(path)
        if self._path != ":memory:":
            Path(self._path).parent.mkdir(parents=True, exist_ok=True)
        # Keep one connection alive for in-memory stores; each connect call would create a fresh database.
        self._connection = sqlite3.connect(self._path)
        conn = self._connection
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS elo_flow_learning (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    relation_id TEXT NOT NULL,
                    origin_flow TEXT NOT NULL,
                    target_flow TEXT NOT NULL,
                    outcome TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    evidence_refs TEXT NOT NULL,
                    provenance_refs TEXT NOT NULL,
                    metrics TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def append(self, record: FlowOutcomeRecord) -> None:
        self._connection.execute(
                """
                INSERT INTO elo_flow_learning
                (relation_id, origin_flow, target_flow, outcome, success,
                 evidence_refs, provenance_refs, metrics)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.relation_id,
                    record.origin_flow,
                    record.target_flow,
                    record.outcome,
                    int(record.success),
                    json.dumps(record.evidence_refs),
                    json.dumps(record.provenance_refs),
                    json.dumps(record.metrics),
                ),
            )
        self._connection.commit()

    def history(self, relation_id: str) -> tuple[FlowOutcomeRecord, ...]:
        rows = self._connection.execute(
                """
                SELECT relation_id, origin_flow, target_flow, outcome, success,
                       evidence_refs, provenance_refs, metrics
                FROM elo_flow_learning
                WHERE relation_id = ?
                ORDER BY id
                """,
                (relation_id,),
            ).fetchall()
        return tuple(
            FlowOutcomeRecord(
                relation_id=row[0],
                origin_flow=row[1],
                target_flow=row[2],
                outcome=row[3],
                success=bool(row[4]),
                evidence_refs=tuple(json.loads(row[5])),
                provenance_refs=tuple(json.loads(row[6])),
                metrics=tuple(tuple(item) for item in json.loads(row[7])),
            )
            for row in rows
        )


class FlowAdaptationEngine:
    """Turn persisted outcomes into a bounded candidate adaptation."""

    def __init__(self, store: FlowLearningStore) -> None:
        self._store = store

    def record(self, record: FlowOutcomeRecord) -> FlowAdaptation:
        self._store.append(record)
        return self.assess(record.relation_id)

    def assess(self, relation_id: str) -> FlowAdaptation:
        history = self._store.history(relation_id)
        observations = len(history)
        successes = sum(item.success for item in history)
        rate = successes / observations if observations else 0.0
        if observations < 2:
            status = "INSUFFICIENT_EVIDENCE"
        elif rate == 1.0:
            status = "REPEATABLE_CANDIDATE"
        elif rate >= 0.5:
            status = "REVIEW_REQUIRED"
        else:
            status = "REJECT_CANDIDATE"
        return FlowAdaptation(relation_id, observations, successes, rate, status)

    def learning_candidate(self, relation_id: str) -> dict[str, object] | None:
        """Adapt persisted flow evidence into the existing ELO learning intake shape.

        This is an intake adapter only. It emits a candidate for the existing
        ELO learning/evolution pipeline; it never promotes or mutates canonical
        knowledge. A repeatable result is required before a candidate exists.
        """
        adaptation = self.assess(relation_id)
        if adaptation.status != "REPEATABLE_CANDIDATE":
            return None
        history = self._store.history(relation_id)
        latest = history[-1]
        evidence_refs = tuple(
            dict.fromkeys(ref for item in history for ref in item.evidence_refs)
        )
        provenance_refs = tuple(
            dict.fromkeys(ref for item in history for ref in item.provenance_refs)
        )
        if not evidence_refs or not provenance_refs:
            return None
        return {
            "candidate_id": f"FLOW-{relation_id}",
            "source": "elo-flow-complementarity",
            "relation_id": relation_id,
            "origin_flow": latest.origin_flow,
            "target_flow": latest.target_flow,
            "observations": adaptation.observations,
            "success_rate": adaptation.success_rate,
            "evidence_refs": evidence_refs,
            "provenance_refs": provenance_refs,
            "promotion_state": "candidate_only",
        }


__all__ = [
    "FlowAdaptation",
    "FlowAdaptationEngine",
    "FlowLearningStore",
    "FlowOutcomeRecord",
    "SQLiteFlowLearningStore",
]
