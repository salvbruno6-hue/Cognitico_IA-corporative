"""Additional deterministic PCP operational mappings."""

from __future__ import annotations

from typing import Mapping, Sequence

from .pcp_confrontation import PCPConfrontation, confront


def confront_capacity(rows: Sequence[Mapping[str, object]]) -> tuple[PCPConfrontation, ...]:
    result = []
    for row in rows:
        planned = row.get("quantidade_padrao")
        actual = row.get("quantidade_disponivel")
        variance = actual - planned if isinstance(actual, (int, float)) and isinstance(planned, (int, float)) else None
        result.append(confront(
            dimension="CAPACIDADE",
            key=str(row.get("id", "")),
            planned=planned if isinstance(planned, (int, float)) else None,
            actual=actual if isinstance(actual, (int, float)) else None,
            variance=variance,
            evidence_ids=tuple(str(v) for v in row.get("evidence_ids", ())),
        ))
    return tuple(result)


def confront_stock(rows: Sequence[Mapping[str, object]]) -> tuple[PCPConfrontation, ...]:
    result = []
    for row in rows:
        planned = row.get("quantidade_reservada")
        actual = row.get("quantidade_disponivel")
        variance = actual - planned if isinstance(actual, (int, float)) and isinstance(planned, (int, float)) else None
        result.append(confront(
            dimension="ESTOQUE",
            key=str(row.get("id", "")),
            planned=planned if isinstance(planned, (int, float)) else None,
            actual=actual if isinstance(actual, (int, float)) else None,
            variance=variance,
            evidence_ids=tuple(str(v) for v in row.get("evidence_ids", ())),
        ))
    return tuple(result)


def confront_flow(rows: Sequence[Mapping[str, object]]) -> tuple[PCPConfrontation, ...]:
    result = []
    for row in rows:
        planned = row.get("inicio")
        actual = row.get("fim")
        result.append(confront(
            dimension="FLUXO",
            key=str(row.get("id", "")),
            planned=planned if isinstance(planned, (int, float)) else None,
            actual=actual if isinstance(actual, (int, float)) else None,
            evidence_ids=tuple(str(v) for v in row.get("evidence_ids", ())),
        ))
    return tuple(result)
