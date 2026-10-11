"""Bounded historical retrieval policy for the canonical ELO Context owner.

The policy narrows retrieval with explicit temporal bounds and makes relaxed
recall an explicit retry mode. It does not create a memory store, retrieval
engine, provider, or persistence authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class RecallMode(StrEnum):
    STRICT = "STRICT"
    OR_RELAXED_RETRY = "OR_RELAXED_RETRY"


@dataclass(frozen=True, slots=True)
class BoundedRetrievalPolicy:
    query: str
    after: datetime | None = None
    before: datetime | None = None
    recall_mode: RecallMode = RecallMode.STRICT

    def validate(self) -> "BoundedRetrievalPolicy":
        if not self.query.strip():
            raise ValueError("query must not be empty")
        if self.after is not None and self.before is not None and self.after > self.before:
            raise ValueError("after must not be later than before")
        return self

    def admits_timestamp(self, timestamp: datetime) -> bool:
        self.validate()
        if self.after is not None and timestamp < self.after:
            return False
        if self.before is not None and timestamp > self.before:
            return False
        return True

    def relaxed_retry(self) -> "BoundedRetrievalPolicy":
        """Return an explicit retry policy without widening temporal scope."""
        self.validate()
        return BoundedRetrievalPolicy(
            query=self.query.strip(),
            after=self.after,
            before=self.before,
            recall_mode=RecallMode.OR_RELAXED_RETRY,
        )


def normalize_bounded_retrieval(
    *,
    query: str,
    after: datetime | None = None,
    before: datetime | None = None,
) -> BoundedRetrievalPolicy:
    return BoundedRetrievalPolicy(
        query=query.strip(), after=after, before=before
    ).validate()


__all__ = [
    "BoundedRetrievalPolicy",
    "RecallMode",
    "normalize_bounded_retrieval",
]
