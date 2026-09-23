"""PCP planned-vs-actual confrontation layer.

This layer composes already calculated PCP facts into a comparable record.
It does not infer causes, create forecasts, persist results, learn, or mutate
canonical state. Cause fields are evidence references supplied by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class PCPConfrontation:
    dimension: str
    key: str
    planned: object | None
    actual: object | None
    variance: float | int | None
    status: str
    evidence_ids: tuple[str, ...]
    cause_evidence_ids: tuple[str, ...]
    impact: str | None


def confront(
    *,
    dimension: str,
    key: str,
    planned: float | int | None,
    actual: float | int | None,
    variance: float | int | None = None,
    evidence_ids: Sequence[str] = (),
    cause_evidence_ids: Sequence[str] = (),
    impact: str | None = None,
) -> PCPConfrontation:
    evidence = tuple(dict.fromkeys(evidence_ids))
    causes = tuple(dict.fromkeys(cause_evidence_ids))
    if planned is None or actual is None:
        status = "NAO_LOCALIZADO"
    else:
        status = "CONFRONTADO"
    return PCPConfrontation(
        dimension=dimension,
        key=key,
        planned=planned,
        actual=actual,
        variance=variance,
        status=status,
        evidence_ids=evidence,
        cause_evidence_ids=causes,
        impact=impact,
    )


def confront_batch(
    records: Sequence[Mapping[str, object]],
) -> tuple[PCPConfrontation, ...]:
    result = []
    for record in records:
        result.append(
            confront(
                dimension=str(record.get("dimension", "")),
                key=str(record.get("key", "")),
                planned=record.get("planned"),  # type: ignore[arg-type]
                actual=record.get("actual"),    # type: ignore[arg-type]
                variance=record.get("variance"),  # type: ignore[arg-type]
                evidence_ids=record.get("evidence_ids", ()),  # type: ignore[arg-type]
                cause_evidence_ids=record.get("cause_evidence_ids", ()),  # type: ignore[arg-type]
                impact=record.get("impact"),  # type: ignore[arg-type]
            )
        )
    return tuple(result)


def summarize_status(
    confrontations: Sequence[PCPConfrontation],
) -> dict[str, int]:
    summary: dict[str, int] = {}
    for item in confrontations:
        summary[item.status] = summary.get(item.status, 0) + 1
    return summary
