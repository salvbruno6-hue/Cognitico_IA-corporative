"""Framework-neutral orchestration for GPT↔ELO knowledge access."""

from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Protocol

from elo.observability.cognitive_timing import (
    CognitiveTimingObservation,
    CognitiveTimingSink,
)

from .contracts import (
    IntentSpec, KnowledgeCandidate, KnowledgeContext, KnowledgeConflict,
    KnowledgeGap, KnowledgeRequirement,
)
from .curation import curate


class KnowledgeProvider(Protocol):
    """Read-only provider boundary implemented by ELO adapters."""
    def retrieve(self, intent: IntentSpec, requirement: KnowledgeRequirement) -> tuple[KnowledgeCandidate, ...]: ...


@dataclass(frozen=True)
class OrchestrationLimits:
    max_requirements: int = 20
    max_candidates: int = 50
    max_retrieval_rounds: int = 2
    common_response_p95_target_ms: int = 3000
    quality_speed_policy: str = "BY_CRITICALITY"
    retrieval_stop_policy: str = "BY_CRITICALITY"

    def __post_init__(self) -> None:
        if self.common_response_p95_target_ms <= 0:
            raise ValueError("common_response_p95_target_ms must be positive")
        if self.quality_speed_policy != "BY_CRITICALITY":
            raise ValueError("quality_speed_policy must remain BY_CRITICALITY")
        if self.retrieval_stop_policy != "BY_CRITICALITY":
            raise ValueError("retrieval_stop_policy must remain BY_CRITICALITY")


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
        # An explicit requirement list is a bounded caller contract. Do not
        # silently append the domain defaults, because that would defeat callers
        # that intentionally test one requirement or verify an unresolved key.
        if intent.required_knowledge:
            templates = tuple((k, k) for k in intent.required_knowledge)
        else:
            key = (intent.domain or "").casefold()
            family = "budget" if "orç" in key or "budget" in key else key
            if "engen" in key:
                family = "engineering"
            elif "compr" in key or "purchase" in key:
                family = "purchasing"
            elif "planej" in key or "planning" in key:
                family = "planning"
            templates = self.DEFAULT_REQUIREMENTS.get(family, ())

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
    def __init__(
        self,
        provider: KnowledgeProvider,
        limits: OrchestrationLimits | None = None,
        *,
        timing_sink: CognitiveTimingSink | None = None,
        clock: Callable[[], float] = perf_counter,
    ) -> None:
        self.provider = provider
        self.limits = limits or OrchestrationLimits()
        self.planner = KnowledgeNeedPlanner()
        self.timing_sink = timing_sink
        self._clock = clock

    @staticmethod
    def _decision_criticality(intent: IntentSpec) -> str:
        value = str(intent.metadata.get("decision_criticality", "")).strip().upper()
        return value if value in {"LOW", "MEDIUM", "HIGH", "CRITICAL"} else "UNSPECIFIED"

    @classmethod
    def _retrieval_strategy(cls, intent: IntentSpec) -> str:
        criticality = cls._decision_criticality(intent)
        if criticality == "LOW":
            return "EARLY_STOP_ELIGIBLE"
        if criticality == "MEDIUM":
            return "CONFIRMATION_REQUIRED"
        return "FULL_EVIDENCE_REQUIRED"

    def _record_timing(
        self,
        *,
        intent: IntentSpec,
        stage: str,
        duration_ms: float,
        requirement_key: str = "",
        candidate_count: int = 0,
        metadata: dict[str, str] | None = None,
    ) -> None:
        if self.timing_sink is None:
            return
        observation = CognitiveTimingObservation(
            stage=stage,
            duration_ms=max(0.0, duration_ms),
            correlation_id=str(intent.metadata.get("correlation_id", "")),
            requirement_key=requirement_key,
            candidate_count=candidate_count,
            metadata=metadata or {},
        )
        try:
            self.timing_sink.record(observation)
        except Exception:  # observability must never change cognitive output
            return

    def run(self, intent: IntentSpec) -> KnowledgeContext:
        total_started = self._clock()
        requirements = self.planner.plan(intent, self.limits)
        candidates: list[KnowledgeCandidate] = []
        gaps: list[KnowledgeGap] = []
        conflicts: list[KnowledgeConflict] = []
        retrieval_calls = 0

        for requirement in requirements:
            retrieval_started = self._clock()
            found = self.provider.retrieve(intent, requirement)
            retrieval_calls += 1
            self._record_timing(
                intent=intent,
                stage="knowledge.retrieve",
                duration_ms=(self._clock() - retrieval_started) * 1000.0,
                requirement_key=requirement.key,
                candidate_count=len(found),
                metadata={
                    "required": str(requirement.required).lower(),
                    "decision_criticality": self._decision_criticality(intent),
                    "retrieval_strategy": self._retrieval_strategy(intent),
                },
            )
            if not found and requirement.required:
                gaps.append(
                    KnowledgeGap(
                        key=requirement.key,
                        reason=f"no governed knowledge returned for requirement: {requirement.key}",
                        blocks_decision=requirement.key not in {"conflicts", "gaps"},
                    )
                )
            candidates.extend(found)

        curation_started = self._clock()
        curated = curate(tuple(candidates), self.limits.max_candidates, intent=intent)
        self._record_timing(
            intent=intent,
            stage="knowledge.curate",
            duration_ms=(self._clock() - curation_started) * 1000.0,
            candidate_count=len(curated),
            metadata={"input_candidates": str(len(candidates))},
        )
        for item in curated:
            if item.status == "CONFLICTING":
                conflicts.append(
                    KnowledgeConflict(
                        subject=item.source_id,
                        sources=(item.source_id,),
                        description="candidate marked as conflicting by the governed source",
                    )
                )
        provenance = {item.source_id: item.provenance for item in curated if item.provenance}
        context = KnowledgeContext(
            intent=intent,
            candidates=curated,
            gaps=tuple(gaps),
            conflicts=tuple(conflicts),
            provenance=provenance,
        )
        self._record_timing(
            intent=intent,
            stage="knowledge.total",
            duration_ms=(self._clock() - total_started) * 1000.0,
            candidate_count=len(curated),
            metadata={
                "requirements": str(len(requirements)),
                "retrieval_calls": str(retrieval_calls),
                "gaps": str(len(gaps)),
                "conflicts": str(len(conflicts)),
                "common_response_p95_target_ms": str(
                    self.limits.common_response_p95_target_ms
                ),
                "quality_speed_policy": self.limits.quality_speed_policy,
                "retrieval_stop_policy": self.limits.retrieval_stop_policy,
                "decision_criticality": self._decision_criticality(intent),
                "retrieval_strategy": self._retrieval_strategy(intent),
            },
        )
        return context
