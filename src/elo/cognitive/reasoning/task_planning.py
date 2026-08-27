"""Deterministic task decomposition primitives for ELO reasoning.

The planner creates an explicit execution graph. It does not execute tools or
silently invent missing tenant methodology.
"""
from dataclasses import dataclass, field
from enum import Enum


class StepKind(str, Enum):
    DISCOVER = "discover"
    RETRIEVE = "retrieve"
    REASON = "reason"
    EXECUTE = "execute"
    VERIFY = "verify"
    RECORD = "record"


@dataclass(frozen=True)
class TaskStep:
    id: str
    kind: StepKind
    objective: str
    depends_on: tuple[str, ...] = ()
    required_capabilities: tuple[str, ...] = ()
    tenant_method_required: bool = True
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class TaskPlan:
    goal: str
    steps: tuple[TaskStep, ...]
    version: str = "0.1"

    def validate(self) -> None:
        ids = {step.id for step in self.steps}
        if not self.goal:
            raise ValueError("goal is required")
        if len(ids) != len(self.steps):
            raise ValueError("task step ids must be unique")
        for step in self.steps:
            if any(dep not in ids for dep in step.depends_on):
                raise ValueError(f"unknown dependency in {step.id}")
            if step.id in step.depends_on:
                raise ValueError(f"self dependency in {step.id}")

    def ready(self, completed: set[str]) -> tuple[TaskStep, ...]:
        return tuple(
            step for step in self.steps
            if step.id not in completed and set(step.depends_on).issubset(completed)
        )


def build_default_plan(goal: str) -> TaskPlan:
    """Build the safe cognitive lifecycle; execution remains elsewhere."""
    steps = (
        TaskStep("discover", StepKind.DISCOVER, "discover context and tenant method"),
        TaskStep("retrieve", StepKind.RETRIEVE, "retrieve evidenced knowledge", ("discover",)),
        TaskStep("reason", StepKind.REASON, "reason over the resolved context", ("retrieve",)),
        TaskStep("execute", StepKind.EXECUTE, "execute selected capability", ("reason",)),
        TaskStep("verify", StepKind.VERIFY, "verify result against constraints and method", ("execute",)),
        TaskStep("record", StepKind.RECORD, "record experience and provenance", ("verify",)),
    )
    plan = TaskPlan(goal=goal, steps=steps)
    plan.validate()
    return plan
