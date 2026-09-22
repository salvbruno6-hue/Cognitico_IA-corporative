"""Canonical runtime adapter for the governed Symbiont skills.

This module is a thin dispatch boundary only. It does not own authorization,
memory, Evolution Gate, persistence or promotion. Each skill delegates to its
existing canonical implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from elo.core.decision_outcome_loop import DecisionLifecycle
from elo.core.specialist_skill_resolution import (
    SpecialistSkill,
    SpecialistSkillResolver,
    SkillPreIntakeComponent,
    SkillPreIntakeResult,
)
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
        if not isinstance(request, SymbiontRequestGuard):
            raise TypeError("runtime boundary requires the canonical SymbiontRequestGuard")
        request.human_escalation()

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

    @staticmethod
    def pre_intake_skill(
        *,
        skills: Iterable[SpecialistSkill],
        skill_id: str,
        domain_family: str,
        required_components: Iterable[SkillPreIntakeComponent],
        authorized: Any = None,
        minimum_maturity: str = "STRUCTURED",
    ) -> SkillPreIntakeResult:
        """Run the read-only pre-intake gate before Symbiont skill intake."""
        resolver = SpecialistSkillResolver(skills)
        return resolver.pre_intake(
            skill_id=skill_id,
            domain_family=domain_family,
            required_components=required_components,
            authorized=authorized,
            minimum_maturity=minimum_maturity,
        )

    def propose_capability(self, observation: SymbiontLabObservation) -> CapabilityCandidate:
        return self.absorption.propose(observation)


__all__ = ["SymbiontSkillRuntime"]
