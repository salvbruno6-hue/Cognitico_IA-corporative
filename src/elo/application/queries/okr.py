"""Read-side OKR capability used by the canonical GovernedOrchestrator.

Layer: cognitive
Owner: strategic-objective-domain
Status: implemented
Authority: implementation
Related: elo.contracts.okr, GovernedOrchestrator

This service is intentionally read-only. It does not persist OKRs, define KPIs,
authorize access, calculate progress/status, or orchestrate execution. The
caller must already have an authorized tenant scope and may expose this service
as one capability under the existing orchestrator.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from elo.contracts.okr import KeyResult, Measurement, Objective


class OkrReadRepository(Protocol):
    """Persistence port; concrete storage remains an infrastructure concern."""

    def get_objective(self, *, tenant_id: str, objective_id: str) -> Objective | None: ...

    def get_key_result(self, *, tenant_id: str, key_result_id: str) -> KeyResult | None: ...

    def list_key_results(self, *, tenant_id: str, objective_id: str) -> tuple[KeyResult, ...]: ...

    def list_measurements(self, *, tenant_id: str, key_result_id: str) -> tuple[Measurement, ...]: ...


@dataclass(frozen=True, slots=True)
class ObjectiveContext:
    objective: Objective
    key_results: tuple[KeyResult, ...]


@dataclass(frozen=True, slots=True)
class KeyResultContext:
    key_result: KeyResult
    measurements: tuple[Measurement, ...]


class OkrQueryService:
    """Resolve strategic entities for the orchestrator without owning orchestration."""

    def __init__(self, repository: OkrReadRepository) -> None:
        self._repository = repository

    def objective_context(self, *, tenant_id: str, objective_id: str) -> ObjectiveContext | None:
        objective = self._repository.get_objective(tenant_id=tenant_id, objective_id=objective_id)
        if objective is None:
            return None
        self._assert_tenant(tenant_id, objective.tenant_id)

        key_results = self._repository.list_key_results(
            tenant_id=tenant_id,
            objective_id=objective.objective_id,
        )
        for item in key_results:
            self._assert_tenant(tenant_id, item.tenant_id)
            if item.objective_id != objective.objective_id:
                raise ValueError("repository returned a KeyResult for a different Objective")

        return ObjectiveContext(objective=objective, key_results=key_results)

    def key_result_context(self, *, tenant_id: str, key_result_id: str) -> KeyResultContext | None:
        key_result = self._repository.get_key_result(tenant_id=tenant_id, key_result_id=key_result_id)
        if key_result is None:
            return None
        self._assert_tenant(tenant_id, key_result.tenant_id)

        measurements = self._repository.list_measurements(
            tenant_id=tenant_id,
            key_result_id=key_result.key_result_id,
        )
        for item in measurements:
            self._assert_tenant(tenant_id, item.tenant_id)
            if item.key_result_id != key_result.key_result_id:
                raise ValueError("repository returned a Measurement for a different KeyResult")
            if item.metric_code != key_result.metric_code:
                raise ValueError("measurement metric_code does not match KeyResult metric_code")

        return KeyResultContext(key_result=key_result, measurements=measurements)

    @staticmethod
    def _assert_tenant(expected: str, observed: str) -> None:
        if expected != observed:
            raise PermissionError("OKR data crossed the authorized tenant boundary")


__all__ = [
    "KeyResultContext",
    "ObjectiveContext",
    "OkrQueryService",
    "OkrReadRepository",
]
