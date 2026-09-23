"""PCP operational data contract.

Maps rows already retrieved from the canonical PCP data authority into the
confrontation layer. This module does not query, persist, or mutate Supabase.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from .pcp_confrontation import PCPConfrontation, confront


def confront_plan_lines(
    rows: Sequence[Mapping[str, object]],
) -> tuple[PCPConfrontation, ...]:
    """Compare planned line quantity with produced quantity when available."""
    result = []
    for row in rows:
        planned = row.get("quantidade_planejada")
        actual = row.get("quantidade_produzida")
        variance = (
            actual - planned
            if isinstance(actual, (int, float)) and isinstance(planned, (int, float))
            else None
        )
        result.append(
            confront(
                dimension="PRODUCAO",
                key=str(row.get("id", "")),
                planned=planned if isinstance(planned, (int, float)) else None,
                actual=actual if isinstance(actual, (int, float)) else None,
                variance=variance,
                evidence_ids=tuple(
                    str(value) for value in row.get("evidence_ids", ())
                ),
                impact=row.get("impact") if isinstance(row.get("impact"), str) else None,
            )
        )
    return tuple(result)


def confront_operations(
    rows: Sequence[Mapping[str, object]],
) -> tuple[PCPConfrontation, ...]:
    """Compare planned and completed operation quantities."""
    result = []
    for row in rows:
        planned = row.get("quantidade_planejada")
        actual = row.get("quantidade_concluida")
        variance = (
            actual - planned
            if isinstance(actual, (int, float)) and isinstance(planned, (int, float))
            else None
        )
        result.append(
            confront(
                dimension="OPERACAO",
                key=str(row.get("id", "")),
                planned=planned if isinstance(planned, (int, float)) else None,
                actual=actual if isinstance(actual, (int, float)) else None,
                variance=variance,
                evidence_ids=tuple(
                    str(value) for value in row.get("evidence_ids", ())
                ),
            )
        )
    return tuple(result)


def confront_materials(
    rows: Sequence[Mapping[str, object]],
) -> tuple[PCPConfrontation, ...]:
    """Compare gross material need with allocated and purchased quantities."""
    result = []
    for row in rows:
        gross = row.get("quantidade_bruta")
        allocated = row.get("quantidade_alocada")
        purchased = row.get("quantidade_comprada")
        actual = (
            allocated + purchased
            if isinstance(allocated, (int, float))
            and isinstance(purchased, (int, float))
            else None
        )
        variance = (
            actual - gross
            if isinstance(actual, (int, float)) and isinstance(gross, (int, float))
            else None
        )
        result.append(
            confront(
                dimension="MATERIAL",
                key=str(row.get("id", "")),
                planned=gross if isinstance(gross, (int, float)) else None,
                actual=actual,
                variance=variance,
                evidence_ids=tuple(
                    str(value) for value in row.get("evidence_ids", ())
                ),
            )
        )
    return tuple(result)
