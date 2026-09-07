"""Framework-neutral contracts for GPT↔ELO knowledge orchestration.

These contracts are deliberately read/query oriented. They do not grant the
agentic runtime any authority to mutate canonical ELO state.
"""

from dataclasses import dataclass, field
from typing import Literal, Mapping

KnowledgeStatus = Literal[
    "APPLICABLE", "CANONICAL", "GOVERNED", "CURRENT", "REFERENCE", "HISTORICAL",
    "CONFLICTING", "OUTDATED", "UNVERIFIED", "INSUFFICIENT",
]


@dataclass(frozen=True)
class IntentSpec:
    question: str
    intent: str
    domain: str | None = None
    task: str | None = None
    entity: str | None = None
    active_context: str | None = None
    required_knowledge: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class KnowledgeRequirement:
    key: str
    purpose: str
    priority: int = 0
    required: bool = True


@dataclass(frozen=True)
class KnowledgeCandidate:
    source_id: str
    content: str
    source_type: str
    status: KnowledgeStatus
    relevance: float
    confidence: float
    context_match: float
    authority: str | None = None
    provenance: Mapping[str, str] = field(default_factory=dict)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class KnowledgeGap:
    key: str
    reason: str
    blocks_decision: bool = False


@dataclass(frozen=True)
class KnowledgeConflict:
    subject: str
    sources: tuple[str, ...]
    description: str
    requires_human_decision: bool = True


@dataclass(frozen=True)
class KnowledgeContext:
    intent: IntentSpec
    candidates: tuple[KnowledgeCandidate, ...] = ()
    gaps: tuple[KnowledgeGap, ...] = ()
    conflicts: tuple[KnowledgeConflict, ...] = ()
    uncertainties: tuple[str, ...] = ()
    provenance: Mapping[str, Mapping[str, str]] = field(default_factory=dict)

    @property
    def grounded(self) -> bool:
        return bool(self.candidates) and not any(
            gap.blocks_decision for gap in self.gaps
        )

    @property
    def requires_human_decision(self) -> bool:
        return bool(self.conflicts) or any(
            gap.blocks_decision for gap in self.gaps
        )
