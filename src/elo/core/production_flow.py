"""Canonical end-to-end production flow model for ELO."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class ProductionStage(StrEnum):
    DEMAND = "DEMAND"
    PLANNING = "PLANNING"
    SCHEDULING = "SCHEDULING"
    MATERIAL = "MATERIAL"
    CAPACITY = "CAPACITY"
    EXECUTION = "EXECUTION"
    APPOINTMENT = "APPOINTMENT"
    QUALITY = "QUALITY"
    OUTCOME = "OUTCOME"
    FEEDBACK = "FEEDBACK"


@dataclass(frozen=True)
class ProductionEvent:
    event_id: str
    stage: ProductionStage
    production_order_id: str | None = None
    tenant_id: str | None = None
    unit_scope: str | None = None
    occurred_at: str | None = None
    quantity: float | None = None
    status: str | None = None
    deviation: str | None = None
    metadata: Mapping[str, str] | None = None


@dataclass(frozen=True)
class ProductionFlow:
    flow_id: str
    events: tuple[ProductionEvent, ...] = ()

    def events_at(self, stage: ProductionStage) -> tuple[ProductionEvent, ...]:
        return tuple(event for event in self.events if event.stage == stage)

    def deviations(self) -> tuple[ProductionEvent, ...]:
        return tuple(event for event in self.events if event.deviation)

    def lifecycle_complete(self) -> bool:
        required = {
            ProductionStage.DEMAND,
            ProductionStage.PLANNING,
            ProductionStage.EXECUTION,
            ProductionStage.OUTCOME,
        }
        return required.issubset({event.stage for event in self.events})

    def scoped(self, *, tenant_id: str, unit_scope: str | None = None) -> "ProductionFlow":
        return ProductionFlow(
            flow_id=self.flow_id,
            events=tuple(
                event for event in self.events
                if event.tenant_id == tenant_id
                and (unit_scope is None or event.unit_scope == unit_scope)
            ),
        )
