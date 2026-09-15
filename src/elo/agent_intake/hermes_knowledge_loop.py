"""Governed read-only intake loop for learning from Hermes capabilities.

Layer: cognitive
Owner: ELO cognitive orchestrator
Status: implemented
Authority: implementation
Related: ELO_HERMES_CAPABILITY_SCAN_20260912.md, ELO_ARTIFACT_METADATA_STANDARD.md
Depends_on: ELO governance gates, Hermes exported capability evidence

The loop consumes explicitly supplied Hermes evidence. It never calls Hermes,
never mutates Hermes, never executes business operations and never promotes a
candidate without all declared gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Iterable, Mapping, Protocol

CANDIDATE = "candidate"
VALIDATED = "validated"


@dataclass(frozen=True)
class HermesMechanism:
    mechanism_id: str
    category: str
    name: str
    interface: str
    metadata: Mapping[str, str] = field(default_factory=dict)
    dependencies: tuple[str, ...] = ()
    relations: tuple[str, ...] = ()


@dataclass(frozen=True)
class HermesSnapshot:
    source: str
    revision: str
    captured_at: str
    mechanisms: tuple[HermesMechanism, ...]


@dataclass(frozen=True)
class LearningCandidate:
    candidate_id: str
    mechanism_id: str
    status: str
    evidence: tuple[str, ...]
    provenance: Mapping[str, str]
    promotion_requirements: tuple[str, ...]


class SnapshotSource(Protocol):
    def read(self) -> HermesSnapshot: ...


class HermesKnowledgeLoop:
    """Deterministic discovery → evidence → validation → promotion loop."""

    def discover(self, snapshot: HermesSnapshot) -> tuple[LearningCandidate, ...]:
        mechanism_ids = [m.mechanism_id for m in snapshot.mechanisms]
        if len(mechanism_ids) != len(set(mechanism_ids)):
            raise ValueError("Hermes snapshot contains duplicate mechanism_id values")
        if not snapshot.source or not snapshot.revision:
            raise ValueError("Hermes snapshot requires source and revision provenance")

        candidates: list[LearningCandidate] = []
        for mechanism in snapshot.mechanisms:
            candidates.append(
                LearningCandidate(
                    candidate_id=f"HERMES-{mechanism.mechanism_id}",
                    mechanism_id=mechanism.mechanism_id,
                    status=CANDIDATE,
                    evidence=(
                        f"source={snapshot.source}",
                        f"revision={snapshot.revision}",
                        f"captured_at={snapshot.captured_at}",
                        f"interface={mechanism.interface}",
                    ),
                    provenance={
                        "source": snapshot.source,
                        "source_revision": snapshot.revision,
                        "mechanism": mechanism.mechanism_id,
                    },
                    promotion_requirements=(
                        "implementation test passes",
                        "provenance remains intact",
                        "ELO Evolution Gate approval",
                    ),
                )
            )
        return tuple(candidates)

    @staticmethod
    def validate(
        candidate: LearningCandidate,
        *,
        implementation_passed: bool,
        provenance_passed: bool,
        evolution_gate_approved: bool,
    ) -> LearningCandidate:
        approved = (
            implementation_passed
            and provenance_passed
            and evolution_gate_approved
        )
        return replace(candidate, status=VALIDATED if approved else CANDIDATE)

    @staticmethod
    def promote(
        candidates: Iterable[LearningCandidate],
    ) -> tuple[LearningCandidate, ...]:
        """Return only candidates already approved by every promotion gate."""
        return tuple(c for c in candidates if c.status == VALIDATED)

    @staticmethod
    def build_memory_markdown(
        snapshot: HermesSnapshot,
        candidates: Iterable[LearningCandidate],
    ) -> str:
        rows = [
            f"- `{candidate.candidate_id}` — `{candidate.status}` — "
            f"mechanism `{candidate.mechanism_id}`; source `{snapshot.source}` "
            f"revision `{snapshot.revision}`."
            for candidate in candidates
        ]
        body = "\n".join(rows) or "- No mechanisms discovered."
        return (
            "# ELO — Hermes Knowledge Memory\n\n"
            "```yaml\n"
            "id: ELO-HERMES-MEMORY-001\n"
            "name: Hermes Knowledge Intake Memory\n"
            "type: reference\n"
            "layer: knowledge\n"
            "owner: ELO cognitive orchestrator\n"
            "status: draft\n"
            "authority: reference\n"
            "version: 0.1\n"
            "```\n\n"
            "> This memory records evidence and learning candidates recovered from\n"
            "> Hermes. It is not canonical ELO knowledge until the Evolution Gate\n"
            "> explicitly promotes an item.\n\n"
            f"Snapshot: `{snapshot.source}` / `{snapshot.revision}` / `{snapshot.captured_at}`\n\n"
            "## Candidates\n\n"
            f"{body}\n\n"
            "## Admission rule\n\n"
            "Discovery never equals learning. A candidate becomes validated only\n"
            "after implementation tests, provenance checks and ELO Evolution Gate\n"
            "approval. Git merge is separate from cognitive promotion.\n"
        )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
