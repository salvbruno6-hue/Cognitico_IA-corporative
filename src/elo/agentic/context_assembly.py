"""Governed context assembly over ELO's distributed memory fabric.

This module composes already-resolved knowledge. It does not persist, promote,
authorize, or redefine canonical ELO knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .contracts import IntentSpec, KnowledgeCandidate, KnowledgeContext, KnowledgeGap
from .supabase_memory_adapter import SupabaseLearningMemoryAdapter


@dataclass(frozen=True)
class ContextAssemblyPolicy:
    """Bounded policy for deterministic context composition."""

    max_candidates: int = 50
    required_roles: tuple[str, ...] = ()


class ELOContextAssembler:
    """Assemble scoped context without copying or mutating source memory."""

    def __init__(
        self,
        adapter: SupabaseLearningMemoryAdapter,
        policy: ContextAssemblyPolicy | None = None,
    ) -> None:
        self.adapter = adapter
        self.policy = policy or ContextAssemblyPolicy()

    def assemble(self, intent: IntentSpec, requirements: Iterable[str]) -> KnowledgeContext:
        candidates: list[KnowledgeCandidate] = []
        gaps: list[KnowledgeGap] = []

        # Requirement order is preserved: it is part of the context contract.
        seen: set[str] = set()
        for key in requirements:
            if key in seen:
                continue
            seen.add(key)
            requirement = self._requirement(key)
            found = self.adapter.retrieve(intent, requirement)
            if not found:
                gaps.append(
                    KnowledgeGap(
                        key=key,
                        reason=f"no governed knowledge returned for requirement: {key}",
                        blocks_decision=True,
                    )
                )
                continue
            candidates.extend(found)

        # Stable de-duplication by source identity prevents the same source row
        # from being copied into context through multiple requirements.
        unique: dict[str, KnowledgeCandidate] = {}
        for candidate in candidates:
            unique.setdefault(candidate.source_id, candidate)

        ordered = tuple(
            sorted(
                unique.values(),
                key=lambda item: (-item.context_match, -item.relevance, -item.confidence, item.source_id),
            )[: self.policy.max_candidates]
        )

        provenance = {item.source_id: item.provenance for item in ordered if item.provenance}
        return KnowledgeContext(
            intent=intent,
            candidates=ordered,
            gaps=tuple(gaps),
            provenance=provenance,
        )

    @staticmethod
    def _requirement(key: str):
        from .contracts import KnowledgeRequirement

        return KnowledgeRequirement(key=key, purpose=key, priority=0)


__all__ = ["ContextAssemblyPolicy", "ELOContextAssembler"]
