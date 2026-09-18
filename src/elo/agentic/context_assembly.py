"""Governed context assembly over ELO's distributed memory fabric.

This module is the composition boundary over the canonical KnowledgeOrchestrator.
It does not create a competing planner/retrieval authority and does not persist,
promote, authorize, or redefine canonical ELO knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .contracts import IntentSpec, KnowledgeContext
from .orchestrator import KnowledgeOrchestrator, KnowledgeProvider, OrchestrationLimits
from .supabase_memory_adapter import SupabaseLearningMemoryAdapter\n
from ..core.resource_locator import ResourceLocator, ResourceResolutionError



@dataclass(frozen=True)
class ContextAssemblyPolicy:
    """Bounded policy for deterministic context composition."""

    max_candidates: int = 50
    max_requirements: int = 20

    def orchestration_limits(self) -> OrchestrationLimits:
        return OrchestrationLimits(
            max_requirements=self.max_requirements,
            max_candidates=self.max_candidates,
        )


class _AddressAwareProvider:
    """Resolve registered resource addresses before delegating the governed read."""

    def __init__(self, provider: KnowledgeProvider, locator: ResourceLocator) -> None:
        self.provider = provider
        self.locator = locator

    def retrieve(self, intent: IntentSpec, requirement):
        try:
            resolution = self.locator.resolve(requirement.key)
        except ResourceResolutionError:
            return self.provider.retrieve(intent, requirement)

        metadata = dict(intent.metadata)
        metadata["resource_address"] = resolution.physical_address
        metadata["resource_id"] = resolution.record.resource_id
        resolved_intent = IntentSpec(
            question=intent.question,
            intent=intent.intent,
            domain=intent.domain,
            task=intent.task,
            entity=intent.entity,
            active_context=intent.active_context,
            required_knowledge=intent.required_knowledge,
            metadata=metadata,
        )
        return self.provider.retrieve(resolved_intent, requirement)


class ELOContextAssembler:
    """Compose governed context through ELO's canonical knowledge orchestrator."""

    def __init__(
        self,
        provider: KnowledgeProvider | SupabaseLearningMemoryAdapter,
        policy: ContextAssemblyPolicy | None = None,
        orchestrator: KnowledgeOrchestrator | None = None,
    ) -> None:
        self.provider = provider
        self.policy = policy or ContextAssemblyPolicy()
        self.orchestrator = orchestrator or KnowledgeOrchestrator(
            provider, self.policy.orchestration_limits()
        )

    def assemble(self, intent: IntentSpec, requirements: Iterable[str] | None = None) -> KnowledgeContext:
        """Assemble context, optionally constraining the orchestrator to explicit requirements."""
        if requirements is None:
            return self.orchestrator.run(intent)

        # Preserve the canonical orchestrator as the only retrieval/curation path
        # while allowing callers such as domain pilots to specify a bounded subset.
        requested = tuple(dict.fromkeys(requirements))[: self.policy.max_requirements]
        constrained_intent = IntentSpec(
            question=intent.question,
            intent=intent.intent,
            domain=intent.domain,
            task=intent.task,
            entity=intent.entity,
            active_context=intent.active_context,
            required_knowledge=requested,
            metadata=intent.metadata,
        )
        return self.orchestrator.run(constrained_intent)


__all__ = ["ContextAssemblyPolicy", "ELOContextAssembler"]
