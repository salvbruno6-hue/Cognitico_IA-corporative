"""Formal KPI resolution for the OKR read capability.

Layer: cognitive
Owner: strategic-objective-domain (consumer) / formal KPI registry (authority)
Status: implemented
Authority: implementation
Related: mt_definicoes_kpi, mt_snapshots_kpi, elo.contracts.okr

This module never defines or promotes a KPI. It only verifies that a KeyResult's
``metric_code`` is present and active in the existing formal KPI registry and
selects the latest already-governed Measurement as ``current``.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Mapping, Protocol

from elo.application.queries.okr import KeyResultContext


class FormalKpiRegistryReader(Protocol):
    """Read port over the canonical formal KPI registry."""

    def get_definition(self, *, metric_code: str) -> Mapping[str, object] | None: ...


@dataclass(frozen=True, slots=True)
class FormalKpiLink:
    metric_code: str
    name: str
    unit: str
    formula: str
    state: str = "KPI_FORMAL_REGISTRADO"


@dataclass(frozen=True, slots=True)
class KeyResultMetricState:
    key_result_id: str
    metric_state: str
    kpi: FormalKpiLink | None
    current: Decimal | None
    current_measurement_id: str | None
    current_evidence_refs: tuple[str, ...]


class OkrMetricResolver:
    """Resolve KR -> formal KPI -> current without inventing missing state."""

    def __init__(self, registry: FormalKpiRegistryReader) -> None:
        self._registry = registry

    def resolve(self, context: KeyResultContext) -> KeyResultMetricState:
        definition = self._registry.get_definition(metric_code=context.key_result.metric_code)
        if definition is None or definition.get("ativo") is not True:
            return KeyResultMetricState(
                key_result_id=context.key_result.key_result_id,
                metric_state="SEM_KPI_FORMAL_REGISTRADO",
                kpi=None,
                current=None,
                current_measurement_id=None,
                current_evidence_refs=(),
            )

        code = str(definition.get("codigo_kpi") or "").strip()
        if code != context.key_result.metric_code:
            raise ValueError("formal KPI definition code does not match KeyResult metric_code")

        kpi = FormalKpiLink(
            metric_code=code,
            name=str(definition.get("nome") or "").strip(),
            unit=str(definition.get("unidade") or "").strip(),
            formula=str(definition.get("formula") or "").strip(),
        )

        if not context.measurements:
            return KeyResultMetricState(
                key_result_id=context.key_result.key_result_id,
                metric_state="KPI_FORMAL_SEM_MEDICAO",
                kpi=kpi,
                current=None,
                current_measurement_id=None,
                current_evidence_refs=(),
            )

        latest = max(context.measurements, key=lambda item: item.measured_at)
        return KeyResultMetricState(
            key_result_id=context.key_result.key_result_id,
            metric_state="KPI_FORMAL_COM_MEDICAO",
            kpi=kpi,
            current=latest.value,
            current_measurement_id=latest.measurement_id,
            current_evidence_refs=latest.evidence_refs,
        )


__all__ = [
    "FormalKpiLink",
    "FormalKpiRegistryReader",
    "KeyResultMetricState",
    "OkrMetricResolver",
]
