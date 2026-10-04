"""Canonical runtime adapter for the governed Symbiont skills."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from elo.core.capability_registry import CapabilityProbe, CapabilityRegistry, CapabilitySnapshot
from elo.core.decision_outcome_loop import DecisionLifecycle
from elo.agent_intake.hermes_functional_value_proof import FunctionalValueEvidence
from elo.agent_intake.runtime_operational_evidence_collector import RuntimeEvidenceGroup
from .capability_absorption import CapabilityCandidate, NativeCapabilityAbsorption
from .symbionte_lab import SymbiontLabEvaluation, SymbiontLabObservation
from .symbiont_operational_contract import SymbiontRequestGuard, validate_operation


@dataclass(frozen=True)
class SymbiontSkillRuntime:
    """Thin facade; authorization and promotion remain outside this runtime."""

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
    def evaluate_runtime_evidence(group: RuntimeEvidenceGroup) -> FunctionalValueEvidence:
        """Consume only a collector-approved repeated runtime evidence group."""
        if not group.repeatable:
            raise ValueError("runtime evidence is not repeatable")
        return group.to_operational_outcome()

    @staticmethod
    def register_capability(
        registry: CapabilityRegistry,
        capability: CapabilityProbe,
    ) -> CapabilitySnapshot:
        """Make a newly registered Symbiont capability visible to the canonical selector.

        The Symbiont writes only to the existing CapabilityRegistry. It does not
        create a parallel registry or grant execution authority. The selector
        and downstream canonical routers observe the same registry snapshot.
        """
        registry.register(capability)
        return next(
            item for item in registry.snapshot()
            if item.name == capability.name
        )

    def propose_capability(self, observation: SymbiontLabObservation) -> CapabilityCandidate:
        return self.absorption.propose(observation)


__all__ = ["SymbiontSkillRuntime"]
