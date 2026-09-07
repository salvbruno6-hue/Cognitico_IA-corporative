"""Framework-neutral orchestration for GPT↔ELO knowledge access.

LangGraph/LangChain are intentionally not imported here. The agentic runtime
may drive this pipeline, while ELO's canonical retrieval and governance
components remain authoritative.
"""

from dataclasses import dataclass
from typing import Protocol

from .contracts import (
    IntentSpec,
    KnowledgeCandidate,
    KnowledgeContext,
    KnowledgeConflict,
    KnowledgeGap,
    KnowledgeRequirement,
)


class KnowledgeProvider(Protocol):
    """Read-only provider boundary implemented by ELO adapters."""

    def retrieve(
        self,
        intent: IntentSpec,
        requirement: KnowledgeRequirement,
    ) -> tuple[KnowledgeCandidate, ...]:
        ...


@dataclass(frozen=True)
class OrchestrationLimits:
    max_requirements: int = 20
    max_candidates: int = 50
    max_retrieval_rounds: int = 2


class KnowledgeNeedPlanner:
    """Expand a natural-language intent into bounded knowledge requirements."""

    DEFAULT_REQUIREMENTS = {
        "budget": (
            ("current_requirements", "requirements and premises from the active context"),
            ("applicable_composition", "applicable current composition or cost basis"),
            ("materials", "materials/items required by the task"),
            ("labor", "labor inputs and composition"),
            ("equipment", "equipment, mobilization or external resources"),
            ("calculation_memory", "relevant calculation memory and formulas"),
            ("excesses", "applicable excess/excedente rules"),
            ("conflicts", "technical or documentary conflicts"),
            ("gaps", "missing inputs needed to close the task"),
        ),
        "engineering": (
            ("requirements", "technical requirements"),
            ("specifications", "applicable specifications"),
            ("standards", "applicable governed standards and references"),
            ("constraints", "constraints and interfaces"),
            ("calculations", "relevant calculations and assumptions"),
            ("conflicts", "technical conflicts"),
            ("gaps", "missing technical inputs"),
        ),
        "purchasing": (
            ("item", "required item or material"),
            ("specification", "technical specification"),
            ("supplier_reference", "relevant supplier/manufacturer reference"),
            ("price", "current applicable price basis"),
            ("lead_time", "relevant lead time"),
            ("alternatives", "governed alternatives, when applicable"),
            ("gaps", "missing purchasing inputs"),
        ),
        "planning": (
            ("scope", "scope of the task"),
            ("dependencies", "preceding and dependent work"),
            ("resources", "required resources/capacity"),
            ("duration", "relevant duration or planning basis"),
            ("constraints", "planning constraints"),
            ("gaps", "missing planning inputs"),
        ),
    }

    def plan(self, intent: IntentSpec, limits: OrchestrationLimits) -> tuple[KnowledgeRequirement, ...]:
        key = (intent.domain or "").casefold()
        family = "budget" if "orç" in key or "budget" in key else key
        family = "engineering" if "engen" in key else family
        family = "purchasing" if "compr" in key or "purchase" in key else family
        family = "planning" if "planej" in key or "planning" in key else family
        templates = self.DEFAULT_REQUIREMENTS.get(family, ())
        if intent.required_knowledge:
            templates = tuple((k, k) for k in intent.required_knowledge) + templates
        seen: set[str] = set()
        requirements: list[KnowledgeRequirement] = []
        for priority, (key_name, purpose) in enumerate(templates, start=1):
            if key_name in seen:
                continue
            seen.add(key_name)
            requirements.append(KnowledgeRequirement(key_name, purpose, priority=priority))
            if len(requirements) >= limits.max_requirements:
                break
        return tuple(requirements)


class KnowledgeOrchestrator:
    """Coordinate discovery/curation without owning canonical ELO truth."""

    def __init__(self, provider: KnowledgeProvider, limits: OrchestrationLimits | None = None) -> None:
        self.provider = provider
        self.limits = limits or OrchestrationLimits()
        self.planner = KnowledgeNeedPlanner()

    def run(self, intent: IntentSpec) -> KnowledgeContext:
        requirements = self.planner.plan(intent, self.limits)
        candidates: list[KnowledgeCandidate] = []
        gaps: list[KnowledgeGap] = []
        conflicts: list[KnowledgeConflict] = []

        for requirement in requirements:
            found = self.provider.retrieve(intent, requirement)
            if not found and requirement.required:
                gaps.append(
                    KnowledgeGap(
                        key=requirement.key,
                        reason=f"no governed knowledge returned for requirement: {requirement.key}",
                        blocks_decision=requirement.key not in {"conflicts", "gaps"},
                    )
                )
            candidates.extend(found)

        candidates = sorted(
            candidates,
            key=lambda item: (
                item.status not in {"APPLICABLE", "CANONICAL", "GOVERNED"},
                -item.context_match,
                -item.relevance,
                -item.confidence,
                item.source_id,
            ),
        )[: self.limits.max_candidates]

        for item in candidates:
            if item.status == "CONFLICTING":
                conflicts.append(
                    KnowledgeConflict(
                        subject=item.source_id,
                        sources=(item.source_id,),
                        description="candidate marked as conflicting by the governed source",
                    )
                )

        provenance = {
            item.source_id: item.provenance for item in candidates if item.provenance
        }
        return KnowledgeContext(
            intent=intent,
            candidates=tuple(candidates),
            gaps=tuple(gaps),
            conflicts=tuple(conflicts),
            provenance=provenance,
        )
