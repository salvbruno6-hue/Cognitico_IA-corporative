"""Deadline and quality mappings for PCP operational evidence."""

from __future__ import annotations

from typing import Mapping, Sequence

from .pcp_confrontation import PCPConfrontation, confront


def confront_deadlines(rows: Sequence[Mapping[str, object]]) -> tuple[PCPConfrontation, ...]:
    result = []
    for row in rows:
        promised = row.get("data_prometida")
        delivered = row.get("data_entrega")
        on_time = row.get("no_prazo")
        result.append(confront(
            dimension="PRAZO",
            key=str(row.get("id", "")),
            planned=promised,
            actual=delivered,
            variance=(
                0 if on_time is True else 1 if on_time is False else None
            ),
            evidence_ids=tuple(str(v) for v in row.get("evidence_ids", ())),
        ))
    return tuple(result)


def confront_quality(rows: Sequence[Mapping[str, object]]) -> tuple[PCPConfrontation, ...]:
    result = []
    for row in rows:
        approved = row.get("aprovado_sem_retrabalho")
        completed = row.get("total_concluido")
        actual = (
            approved / completed
            if isinstance(approved, (int, float))
            and isinstance(completed, (int, float))
            and completed != 0
            else None
        )
        planned = row.get("fpy_planejado")
        variance = (
            actual - planned
            if isinstance(actual, (int, float))
            and isinstance(planned, (int, float))
            else None
        )
        result.append(confront(
            dimension="QUALIDADE",
            key=str(row.get("id", "")),
            planned=planned,
            actual=actual,
            variance=variance,
            evidence_ids=tuple(str(v) for v in row.get("evidence_ids", ())),
        ))
    return tuple(result)
