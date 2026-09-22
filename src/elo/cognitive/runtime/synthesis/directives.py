"""Diretrizes cognitivas.

Diretriz é uma pergunta que o ELO faz quando identifica lacuna
de informação. Não inventa — só evidencia.

Refs: ADR-0014, ELO_HUMAN_RESPONSE_PROTOCOL.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Directive:
    """Pergunta estruturada do ELO à IA/usuário."""
    id: str
    question: str
    why: str
    priority: str  # high | medium | low
    source: str  # so_learning | delta_correction
    resolvable_by: str  # human_confirmation | supplier_check | web_search
    context_keys: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "question": self.question,
            "why": self.why,
            "priority": self.priority,
            "source": self.source,
            "resolvable_by": self.resolvable_by,
            "context_keys": self.context_keys,
        }


TEMPORAL_PATTERNS = [
    r"h[áa]\s+\d+\s+(dia|dias|m[êe]s|meses|ano|anos)",
    r"em\s+20\d{2}",
    r"desde\s+20\d{2}",
    r"at[ée]\s+20\d{2}",
]

PREMISE_KEYWORDS = ["premissa", "a confirmar", "não confirmad", "pendente de"]


class DirectiveGenerator:
    """Detecta lacunas evidenciadas no aprendizado/delta.

    Conservador: só gera diretriz quando há evidência clara.
    """

    def __init__(self) -> None:
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"DIR-{self._counter:03d}"

    def generate(
        self,
        so_context: dict[str, Any],
        delta: dict[str, Any] | None = None,
    ) -> list[Directive]:
        directives: list[Directive] = []
        learning = so_context.get("learning") or {}
        tags = learning.get("tags", [])
        summary = learning.get("summary", "")

        for tag in tags:
            tag_lower = tag.lower()
            for kw in PREMISE_KEYWORDS:
                if kw in tag_lower:
                    directives.append(self._premise_directive(tag, learning))
                    break

        blob = f"{summary} {' '.join(tags)}"
        for pattern in TEMPORAL_PATTERNS:
            match = re.search(pattern, blob, re.IGNORECASE)
            if match:
                directives.append(
                    self._temporal_directive(match.group(0), learning)
                )
                break

        if delta:
            corrections = delta.get("corrections", [])
            for item in corrections[:2]:
                directives.append(
                    self._correction_directive(
                        item.get("summary", ""),
                        so_context.get("so_id"),
                    )
                )

        return directives

    def _premise_directive(self, tag: str, learning: dict) -> Directive:
        return Directive(
            id=self._next_id(),
            question=f"Confirme a premissa relacionada a '{tag}'",
            why=(
                "O aprendizado menciona essa premissa, mas ela ainda "
                "não foi confirmada por documento ou cliente."
            ),
            priority="high",
            source="so_learning",
            resolvable_by="human_confirmation",
            context_keys=[tag],
        )

    def _temporal_directive(self, marker: str, learning: dict) -> Directive:
        so_id = learning.get("so_id", "a SO")
        return Directive(
            id=self._next_id(),
            question=f"Atualize os dados de {so_id} — há registro de '{marker}'",
            why=(
                f"O aprendizado referencia período '{marker}'. "
                "Valores podem estar desatualizados."
            ),
            priority="medium",
            source="so_learning",
            resolvable_by="web_search",
            context_keys=learning.get("tags", [])[:3],
        )

    def _correction_directive(
        self, summary: str, so_id: str | None
    ) -> Directive:
        return Directive(
            id=self._next_id(),
            question=f"Confirme qual informação está correta: {summary}",
            why=(
                "A análise atual contradiz o que o ELO registrou "
                f"sobre {so_id or 'essa SO'}."
            ),
            priority="high",
            source="delta_correction",
            resolvable_by="human_confirmation",
            context_keys=[],
        )
