"""Canonical production-flow model for ELO.

ELO observes production end-to-end rather than acting as another transactional
module. The model keeps planning, execution, deviation, outcome and feedback
connected so systemic reasoning can identify bottlenecks and consequences.
"""

from dataclasses import dataclass, field
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
    resource_id: str | None = None
    material_id: str | None = None
    occurred_at: str | None = None
    quantity: float | None = None
    status: str | None = None
    deviation: str | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ProductionFlow:
    flow_id: str
    events: tuple[ProductionEvent, ...] = ()

    def events_at(self, stage: ProductionStage) -> tuple[ProductionEvent, ...]:
        return tuple(event for event in self.events if event.stage == stage)

    def deviations(self) -> tuple[ProductionEvent, ...]:
        return tuple(event for event in self.events if event.deviation)

    def has_feedback(self) -> bool:
        return bool(self.events_at(ProductionStage.FEEDBACK))

    def outcome_exists(self) -> bool:
        return bool(self.events_at(ProductionStage.OUTCOME))

    def lifecycle_complete(self) -> bool:
        required = {
            ProductionStage.DEMAND,
            ProductionStage.PLANNING,
            ProductionStage.EXECUTION,
            ProductionStage.OUTCOME,
        }
        return required.issubset({event.stage for event in self.events})
