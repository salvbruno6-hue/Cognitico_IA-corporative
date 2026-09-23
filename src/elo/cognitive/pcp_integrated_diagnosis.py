"""Integrated deterministic PCP diagnosis.

Combines already observed PCP confrontations. It classifies evidence state
and aggregates impact without inferring causal explanations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .pcp_confrontation import PCPConfrontation


@dataclass(frozen=True)
class PCPDiagnostic:
    total: int
    confronted: int
    not_located: int
    dimensions: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    impact: tuple[str, ...]
    status: str


def diagnose_confrontations(
    confrontations: Sequence[PCPConfrontation],
) -> PCPDiagnostic:
    items = tuple(confrontations)
    evidence = tuple(
        dict.fromkeys(
            evidence_id
            for item in items
            for evidence_id in item.evidence_ids
        )
    )
    impacts = tuple(
        dict.fromkeys(
            item.impact for item in items
            if item.impact is not None
        )
    )
    dimensions = tuple(dict.fromkeys(item.dimension for item in items))
    confronted = sum(item.status == "CONFRONTADO" for item in items)
    not_located = sum(item.status == "NAO_LOCALIZADO" for item in items)

    if not items:
        status = "SEM_DADOS"
    elif not_located:
        status = "DADOS_INCOMPLETOS"
    else:
        status = "DIAGNOSTICO_CONFRONTADO"

    return PCPDiagnostic(
        total=len(items),
        confronted=confronted,
        not_located=not_located,
        dimensions=dimensions,
        evidence_ids=evidence,
        impact=impacts,
        status=status,
    )
