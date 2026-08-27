"""Governed cognitive execution loop for the ELO symbiont.

This orchestrator composes existing cognitive responsibilities. It does not
make tenant methodology canonical and does not permit unverified experience
promotion.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


class MethodProvider(Protocol):
    def load(self, context: dict[str, Any]) -> Any: ...


class Planner(Protocol):
    def plan(self, task: Any, method: Any, context: dict[str, Any]) -> list[Any]: ...


class Executor(Protocol):
    def execute(self, step: Any, context: dict[str, Any]) -> Any: ...


class Verifier(Protocol):
    def verify(self, result: Any, step: Any, method: Any, context: dict[str, Any]) -> bool: ...


class ExperienceRecorder(Protocol):
    def record(self, experience: dict[str, Any]) -> Any: ...


@dataclass
class ExecutionTrace:
    task: Any
    tenant_id: str
    method: Any
    steps: list[Any] = field(default_factory=list)
    results: list[Any] = field(default_factory=list)
    verified: list[bool] = field(default_factory=list)
    experience: Any = None


@dataclass
class CognitiveExecutionLoop:
    method_provider: MethodProvider
    planner: Planner
    executor: Executor
    verifier: Verifier
    experience_recorder: ExperienceRecorder

    def run(self, task: Any, *, tenant_id: str, context: dict[str, Any] | None = None) -> ExecutionTrace:
        if not tenant_id:
            raise ValueError("tenant_id is required")
        runtime_context = dict(context or {})
        runtime_context["tenant_id"] = tenant_id

        method = self.method_provider.load(runtime_context)
        steps = self.planner.plan(task, method, runtime_context)
        trace = ExecutionTrace(task=task, tenant_id=tenant_id, method=method, steps=list(steps))

        for step in steps:
            result = self.executor.execute(step, runtime_context)
            verified = self.verifier.verify(result, step, method, runtime_context)
            trace.results.append(result)
            trace.verified.append(verified)
            if not verified:
                raise RuntimeError(f"verification failed for step: {step!r}")

        trace.experience = self.experience_recorder.record({
            "tenant_id": tenant_id,
            "task": task,
            "steps": trace.steps,
            "results": trace.results,
            "verified": trace.verified,
        })
        return trace
