"""Autonomous source discovery for ELO consulting.

Discovery is semantic and source-neutral. It emits adapter capabilities using
canonical capability identifiers so the plan can be executed by SourceResolver
without leaking provider-specific implementation details into Core.
"""

from dataclasses import dataclass, field
from typing import Literal, Mapping

SourceKind = Literal[
    "ELO_MEMORY", "GITHUB", "CHATGPT_PROJECTS", "DOCUMENTS", "WEB", "AI_PROVIDER"
]

CANONICAL_CAPABILITIES: Mapping[str, str] = {
    "ELO_MEMORY": "source.elo_memory.read",
    "GITHUB": "source.github.read",
    "CHATGPT_PROJECTS": "source.chatgpt_projects.read",
    "DOCUMENTS": "source.documents.read",
    "WEB": "source.web.read",
    "AI_PROVIDER": "source.ai_provider.read",
}


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
    """Infer authorized source capabilities without requiring user paths."""

    _keywords = {
        "possível cliente": ("external_entity", "WEB", "CHATGPT_PROJECTS", "ELO_MEMORY"),
        "empresa": ("external_entity", "WEB", "CHATGPT_PROJECTS", "AI_PROVIDER"),
        "cliente": ("commercial_analysis", "ELO_MEMORY", "CHATGPT_PROJECTS", "WEB"),
        "projeto": ("project_context", "CHATGPT_PROJECTS", "GITHUB", "DOCUMENTS"),
        "contrato": ("contract_analysis", "ELO_MEMORY", "DOCUMENTS", "AI_PROVIDER"),
        "arquitetura": ("architecture_review", "GITHUB", "ELO_MEMORY", "AI_PROVIDER"),
        "elo": ("elo_state", "ELO_MEMORY", "GITHUB", "CHATGPT_PROJECTS"),
    }
    _intent_specificity = {
        "general_consulting": 0, "elo_state": 10, "project_context": 20,
        "contract_analysis": 30, "architecture_review": 40,
        "commercial_analysis": 50, "external_entity": 60,
    }
    _preferred_source = {
        "architecture_review": "GITHUB", "external_entity": "WEB",
        "commercial_analysis": "ELO_MEMORY", "contract_analysis": "ELO_MEMORY",
        "project_context": "CHATGPT_PROJECTS", "elo_state": "ELO_MEMORY",
    }

    def plan(self, question: str, *, temporal_context_id: str | None = None,
             known_entities: tuple[str, ...] = ()) -> DiscoveryPlan:
        if not question.strip():
            raise ValueError("question is required")
        normalized = question.casefold()
        intent = "general_consulting"
        intent_score = 0
        ranked: dict[str, int] = {}
        reasons: dict[str, str] = {}
        for keyword, (candidate_intent, *sources) in self._keywords.items():
            if keyword not in normalized:
                continue
            candidate_score = self._intent_specificity[candidate_intent]
            if candidate_score > intent_score:
                intent, intent_score = candidate_intent, candidate_score
            for index, source in enumerate(sources):
                ranked[source] = max(ranked.get(source, 0), len(sources) - index)
                reasons[source] = f"question contains context keyword: {keyword}"
        if not ranked:
            for index, source in enumerate(("ELO_MEMORY", "CHATGPT_PROJECTS", "GITHUB", "WEB", "AI_PROVIDER")):
                ranked[source] = 5 - index
                reasons[source] = "default discovery coverage"
        preferred = self._preferred_source.get(intent)
        candidates = tuple(
            SourceCandidate(
                kind=source,  # type: ignore[arg-type]
                reason=reasons[source],
                priority=priority,
                query=question,
                required_capability=CANONICAL_CAPABILITIES[source],
            )
            for source, priority in sorted(
                ranked.items(), key=lambda item: (-item[1], 0 if item[0] == preferred else 1, item[0])
            )
        )
        return DiscoveryPlan(intent=intent, entities=known_entities, questions=(question,),
                             candidates=candidates, temporal_context_id=temporal_context_id)
