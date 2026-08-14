from dataclasses import dataclass, field
from typing import Literal, Mapping

SourceKind = Literal["ELO_MEMORY", "GITHUB", "CHATGPT_PROJECTS", "DOCUMENTS", "WEB", "AI_PROVIDER"]

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
    _intent_specificity = {
        "external_entity": 60,
        "commercial_analysis": 60,
        "project_context": 50,
        "contract_analysis": 60,
        "architecture_review": 70,
        "elo_state": 10,
    }

    def plan(self, question: str, *, temporal_context_id: str | None = None,
             known_entities: tuple[str, ...] = ()) -> DiscoveryPlan:
        if not question.strip():
            raise ValueError("question is required")
        normalized = question.casefold()
        intent = "general_consulting"
        intent_score = -1
        ranked: dict[str, int] = {}
        reasons: dict[str, str] = {}
        capabilities: dict[str, str] = {}
        for keyword, (candidate_intent, *sources) in self._keywords.items():
            if keyword not in normalized:
                continue
            score = self._intent_specificity[candidate_intent]
            if score > intent_score:
                intent, intent_score = candidate_intent, score
            for index, source in enumerate(sources):
                ranked[source] = max(ranked.get(source, 0), len(sources) - index)
                reasons[source] = f"question contains context keyword: {keyword}"
                capabilities[source] = candidate_intent
        if not ranked:
            for index, source in enumerate(("ELO_MEMORY", "CHATGPT_PROJECTS", "GITHUB", "WEB", "AI_PROVIDER")):
                ranked[source] = 5 - index
                reasons[source] = "default discovery coverage"
                capabilities[source] = intent
        candidates = tuple(SourceCandidate(kind=source, reason=reasons[source], priority=priority,
            query=question, required_capability=capabilities[source])
            for source, priority in sorted(ranked.items(), key=lambda item: (-item[1], item[0])))
        return DiscoveryPlan(intent=intent, entities=known_entities, questions=(question,),
            candidates=candidates, temporal_context_id=temporal_context_id)
