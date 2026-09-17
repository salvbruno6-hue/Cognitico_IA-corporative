"""Application orchestration for bounded insistence over a Core decision.

The Core capability decision is an input to this boundary. This module does
not infer an intent-to-condition mapping, choose a capability, authorize it,
or mutate canonical knowledge. It only coordinates the already-governed
execution boundary with the bounded insistence/recovery runtime.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from elo.core.capability_resolution import CoreCapabilityDecision
from elo.core.insistence_runtime import (
    AttemptResult,
    InsistenceAction,
    InsistenceRun,
    InsistenceState,
    run_insistence_experience,
)


@dataclass(frozen=True, slots=True)
class GovernedInsistenceRequest:
    objective: str
    core_capability_decision: CoreCapabilityDecision
    max_attempts: int = 5
    no_progress_limit: int = 2


GovernedAttemptExecutor = Callable[
    [CoreCapabilityDecision, InsistenceAction, InsistenceState], AttemptResult
]


class GovernedInsistenceUseCase:
    """Run an already-resolved capability through bounded recovery."""

    def run(
        self,
        request: GovernedInsistenceRequest,
        *,
        execute: GovernedAttemptExecutor,
    ) -> InsistenceRun:
        decision = request.core_capability_decision
        if not decision.executable:
            raise ValueError("Core capability decision is not executable")

        return run_insistence_experience(
            objective=request.objective,
            execute=lambda action, state: execute(decision, action, state),
            max_attempts=request.max_attempts,
            no_progress_limit=request.no_progress_limit,
        )


__all__ = [
    "GovernedAttemptExecutor",
    "GovernedInsistenceRequest",
    "GovernedInsistenceUseCase",
]
