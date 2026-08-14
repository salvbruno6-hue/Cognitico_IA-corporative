"""Autonomous source discovery for ELO consulting.

The planner converts a user question and temporal context into a source-neutral
search plan. It does not hard-code a single repository path or provider. Actual
retrieval is performed by authorized adapters, and all retrieved material must
enter Temporal Conversation Memory before promotion.
"""

from dataclasses import dataclass, field
from typing import Literal, Mapping

SourceKind = Literal[
    "ELO_MEMORY",
    "GITHUB",
    "CHATGPT_PROJECTS",
    "DOCUMENTS",
    "WEB",
    "AI_PROVIDER",
]


@dataclass(frozen=True)
class SourceCandidate:
    kind: SourceKind
    reason: str
    priority: int
    query: str
    required_capability: str


@dataclass(frozen=True)
class DiscoveryPlan:
    intent: str
    entities: tuple[str, ...]
    questions: tuple[str, ...]
    candidates: tuple[SourceCandidate, ...]
    temporal_context_id: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


class SourceDiscoveryEngine:
    """Infer where information should be sought without requiring user paths."""

    _keywords = {
        "empresa": ("external_entity", "WEB", "CHATGPT_PROJECTS", "AI_PROVIDER"),
        "cliente": ("commercial_analysis", "ELO_MEMORY", "CHATGPT_PROJECTS", "WEB"),
        "projeto": ("project_context", "CHATGPT_PROJECTS", "GITHUB", "DOCUMENTS"),
        "contrato": ("contract_analysis", "ELO_MEMORY", "DOCUMENTS", "AI_PROVIDER"),
        "arquitetura": ("architecture_review", "GITHUB", "ELO_MEMORY", "AI_PROVIDER"),
        "elo": ("elo_state", "ELO_MEMORY", "GITHUB", "CHATGPT_PROJECTS"),
    }

    _intent_priority = {
        "architecture_review": 100,
        "contract_analysis": 90,
        "external_entity": 80,
        "commercial_analysis": 70,
        "project_context": 60,
        "elo_state": 10,
    }

    def plan(
        self,
        question: str,
        *,
        temporal_context_id: str | None = None,
        known_entities: tuple[str, ...] = (),
    ) -> DiscoveryPlan:
        if not question.strip():
            raise ValueError("question is required")

        normalized = question.casefold()
        intent = "general_consulting"
        ranked: dict[str, int] = {}
        reasons: dict[str, str] = {}
        capabilities: dict[str, str] = {}
        matched_intents: list[tuple[int, str, str]] = []
        matched_sources: dict[str, tuple[str, ...]] = {}

        for keyword, (candidate_intent, *sources) in self._keywords.items():
            if keyword not in normalized:
                continue
            matched_intents.append(
                (self._intent_priority.get(candidate_intent, 0), candidate_intent, keyword)
            )
            matched_sources[candidate_intent] = tuple(sources)

        if "possível cliente" in normalized or "possivel cliente" in normalized:
            matched_intents.append(
                (self._intent_priority["external_entity"], "external_entity", "possível cliente")
            )

        if matched_intents:
            _, intent, _ = max(matched_intents, key=lambda item: (item[0], item[2]))

            # The winning intent controls source order. Other matched intents
            # remain useful as secondary coverage, but cannot outrank it.
            primary_sources = matched_sources.get(intent, ())
            for index, source in enumerate(primary_sources):
                ranked[source] = 100 - index
                reasons[source] = f"primary source for intent: {intent}"
                capabilities[source] = intent

            for _, secondary_intent, keyword in sorted(
                matched_intents,
                key=lambda item: (-item[0], item[2]),
            ):
                for index, source in enumerate(matched_sources.get(secondary_intent, ())):
                    if source in ranked:
                        continue
                    ranked[source] = 50 - index
                    reasons[source] = f"secondary coverage from keyword: {keyword}"
                    capabilities[source] = secondary_intent

        if not ranked:
            for index, source in enumerate(("ELO_MEMORY", "CHATGPT_PROJECTS", "GITHUB", "WEB", "AI_PROVIDER")):
                ranked[source] = 5 - index
                reasons[source] = "default discovery coverage"
                capabilities[source] = intent

        if intent != "elo_state":
            for source in ranked:
                if capabilities[source] == "elo_state":
                    capabilities[source] = intent

        candidates = tuple(
            SourceCandidate(
                kind=source,  # type: ignore[arg-type]
                reason=reasons[source],
                priority=priority,
                query=question,
                required_capability=capabilities[source],
            )
            for source, priority in sorted(ranked.items(), key=lambda item: (-item[1], item[0]))
        )
        return DiscoveryPlan(
            intent=intent,
            entities=known_entities,
            questions=(question,),
            candidates=candidates,
            temporal_context_id=temporal_context_id,
        )
