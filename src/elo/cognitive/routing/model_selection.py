"""Evidence-aware model selection for ELO.

Models are executors of a capability, not capabilities themselves. Selection is
contextual and must remain tenant-scoped when tenant policy participates.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ModelCandidate:
    model_id: str
    capabilities: frozenset[str]
    quality: float = 0.0
    latency_ms: float = 0.0
    cost: float = 0.0
    evidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def score(self, *, preferred: set[str] | None = None) -> float:
        preference = 0.1 if preferred and self.model_id in preferred else 0.0
        latency = 1.0 / (1.0 + max(self.latency_ms, 0.0) / 1000.0)
        cost = 1.0 / (1.0 + max(self.cost, 0.0))
        return (0.45 * self.quality) + (0.30 * self.evidence) + (0.15 * latency) + (0.10 * cost) + preference


class ModelSelector:
    def select(
        self,
        capability: str,
        candidates: list[ModelCandidate],
        *,
        preferred: set[str] | None = None,
        minimum_score: float = 0.0,
    ) -> ModelCandidate:
        eligible = [c for c in candidates if capability in c.capabilities]
        ranked = sorted(eligible, key=lambda c: c.score(preferred=preferred), reverse=True)
        if not ranked:
            raise LookupError(f"no model supports capability: {capability}")
        winner = ranked[0]
        if winner.score(preferred=preferred) < minimum_score:
            raise LookupError(f"no model meets minimum score for capability: {capability}")
        return winner
