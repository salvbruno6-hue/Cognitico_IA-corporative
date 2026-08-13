"""Scenario primitives for consequence analysis without executing actions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScenarioAssumption:
    key: str
    value: str


@dataclass(frozen=True)
class ScenarioOutcome:
    scenario_id: str
    description: str
    confidence: float
    affected_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class Scenario:
    id: str
    assumptions: tuple[ScenarioAssumption, ...] = ()
    outcomes: tuple[ScenarioOutcome, ...] = ()

    def add_outcome(self, outcome: ScenarioOutcome) -> "Scenario":
        return Scenario(
            id=self.id,
            assumptions=self.assumptions,
            outcomes=self.outcomes + (outcome,),
        )
