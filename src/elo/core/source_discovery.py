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

        # Specific semantic phrases take precedence over the generic ELO state
        # keyword. This keeps discovery aligned with the user's actual intent.
        if "possível cliente" in normalized or "possivel cliente" in normalized:
            intent = "external_entity"
            matched = ("cliente", "empresa")
            for keyword in matched:
                if keyword not in normalized:
                    continue
                sources = self._keywords[keyword][1:]
                for index, source in enumerate(sources):
                    ranked[source] = max(ranked.get(source, 0), len(sources) - index)
                    reasons[source] = f"question matches external-entity phrase: {keyword}"
                    capabilities[source] = intent
        else:
            matches = [
                (keyword, values)
                for keyword, values in self._keywords.items()
                if keyword in normalized
            ]
            if matches:
                # Prefer the most specific matched semantic keyword. Generic
                # terms such as 'elo' must not overwrite a concrete intent.
                keyword, (intent, *sources) = max(
                    matches,
                    key=lambda item: len(item[0]),
                )
                for index, source in enumerate(sources):
                    ranked[source] = max(ranked.get(source, 0), len(sources) - index)
                    reasons[source] = f"question contains context keyword: {keyword}"
                    capabilities[source] = intent

        if not ranked:
            for index, source in enumerate(("ELO_MEMORY", "CHATGPT_PROJECTS", "GITHUB", "WEB", "AI_PROVIDER")):
                ranked[source] = 5 - index
                reasons[source] = "default discovery coverage"
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
