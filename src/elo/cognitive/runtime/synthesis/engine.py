"""Motor de síntese.

Compara a análise externa (do ChatGPT) com o contexto do ELO
(aprendizado de SO, handbook, precedentes) e produz um delta
estruturado.

Normalização:
- texto é normalizado (lowercase + remoção de acentos) antes de
  tokenizar, para comparar 'módulos' com 'modulos' sem erro.

Refs: ADR-0014.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any

from .directives import DirectiveGenerator
from .types import DeltaItem, SynthesisDelta


STOPWORDS = {
    "a", "o", "e", "de", "do", "da", "em", "um", "uma", "para",
    "com", "por", "os", "as", "no", "na", "ao", "à", "que", "se",
    "como", "mais", "menos", "sem", "sob", "sobre", "entre",
}


def _strip_accents(text: str) -> str:
    """Remove acentos: 'módulos' -> 'modulos'."""
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def _normalize(text: str) -> str:
    return _strip_accents(text).lower()


def _tokenize(text: str) -> set[str]:
    normalized = _normalize(text)
    tokens = re.findall(r"\b[a-z]{4,}\b", normalized)
    return {t for t in tokens if t not in STOPWORDS}


class SynthesisEngine:
    def synthesize(
        self,
        external_analysis: str,
        so_context: dict[str, Any],
        max_items_per_category: int = 5,
    ) -> SynthesisDelta:
        so_id = so_context.get("so_id")
        learning = so_context.get("learning") or {}
        handbook = so_context.get("handbook", [])
        precedents = so_context.get("precedents", [])

        delta = SynthesisDelta(so_id=so_id)

        external_tokens = _tokenize(external_analysis)
        learning_tags = {_normalize(t) for t in learning.get("tags", [])}

        for tag in sorted(learning_tags):
            if tag in external_tokens:
                delta.aligned.append(DeltaItem(
                    category="aligned",
                    summary=f"Análise contempla '{tag}' presente no aprendizado da SO",
                    source="so_learning",
                    confidence=0.8,
                ))
                if len(delta.aligned) >= max_items_per_category:
                    break

        for tag in sorted(learning_tags):
            if tag not in external_tokens:
                delta.improvements.append(DeltaItem(
                    category="improvements",
                    summary=f"Aprendizado menciona '{tag}' que não aparece na análise",
                    source="so_learning",
                    confidence=0.6,
                ))
                if len(delta.improvements) >= max_items_per_category:
                    break

        for doc in handbook[:3]:
            doc_tags = {_normalize(t) for t in doc.get("tags", [])}
            missing = doc_tags - external_tokens
            if missing:
                delta.improvements.append(DeltaItem(
                    category="improvements",
                    summary=(
                        f"Handbook '{doc['title']}' cobre "
                        f"{', '.join(sorted(missing))} não mencionado"
                    ),
                    source="handbook",
                    evidence=[doc["path"]],
                    confidence=0.5,
                ))
                delta.handbook_used.append(doc["id"])

        for p in precedents[:3]:
            delta.precedents_used.append(p["decision_id"])

        total = (
            len(delta.aligned)
            + len(delta.improvements)
            + len(delta.corrections)
            + len(delta.conflicts)
        )
        if total == 0:
            delta.overall_confidence = 0.3
        else:
            delta.overall_confidence = min(
                0.9,
                0.4 + 0.5 * (len(delta.aligned) / max(total, 1)),
            )

        delta.learning_used = learning.get("so_id")

        generator = DirectiveGenerator()
        delta.directives = generator.generate(
            so_context=so_context,
            delta=delta.to_dict(),
        )

        return delta
