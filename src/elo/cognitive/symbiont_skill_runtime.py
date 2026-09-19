"""Canonical runtime adapter for the four governed Symbiont skills.

This module is a thin dispatch boundary only. It does not own authorization,
memory, Evolution Gate, persistence or promotion. Each skill delegates to its
existing canonical implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.core.decision_outcome_loop import DecisionLifecycle
from .capability_absorption import CapabilityCandidate, NativeCapabilityAbsorption
from .symbionte_lab import SymbiontLabEvaluation, SymbiontLabObservation
from .symbiont_operational_contract import SymbiontRequestGuard, validate_operation


@dataclass(frozen=True)
class SymbiontSkillRuntime:
    """Thin operational facade over already-canonical skill implementations."""

    absorption: NativeCapabilityAbsorption

    def __init__(self, *, absorption: NativeCapabilityAbsorption | None = None) -> None:
        object.__setattr__(self, "absorption", absorption or NativeCapabilityAbsorption())

    @staticmethod
    def validate_boundary(request: Any) -> None:
        SymbiontRequestGuard.validate(request)

    @staticmethod
    def validate_operation(operation: str) -> str:
        return validate_operation(operation).value

    @staticmethod
    def handoff_decision(
        lifecycle: DecisionLifecycle,
        *,
        adapter: Any,
        observation: SymbiontLabObservation,
        principal_id: str,
        dataset_version: str,
    ) -> SymbiontLabEvaluation:
        return lifecycle.handoff_to_symbiont(
            adapter=adapter,
            observation=observation,
            principal_id=principal_id,
            dataset_version=dataset_version,
        )

    @staticmethod
    def evaluate_lab(
        adapter: Any,
        observation: SymbiontLabObservation,
        *,
        principal_id: str,
        dataset_version: str,
    ) -> SymbiontLabEvaluation:
        return adapter.evaluate(
            observation,
            principal_id=principal_id,
            dataset_version=dataset_version,
        )

    def propose_capability(self, observation: SymbiontLabObservation) -> CapabilityCandidate:
        return self.absorption.propose(observation)


__all__ = ["SymbiontSkillRuntime"]
