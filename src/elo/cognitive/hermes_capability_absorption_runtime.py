"""Executable orchestration for Hermes capability absorption.

Acquisition is injected: ELO Core does not gain implicit repository/network
authority. The runtime proves the complete local flow from an authorized
snapshot provider through extraction, canonical Evolution Gate classification,
and candidate-only absorption.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol

from .hermes_capability_extractor import HermesCapabilityPattern, extract_patterns, to_external_pattern, to_observation
from .symbiont_capability_absorption import ELOCapabilityCandidate, SymbiontCapabilityAbsorber
from .symbiont_pattern_intake import PatternIntakeDecision, SymbiontPatternIntake


@dataclass(frozen=True)
class HermesSnapshot:
    source_repository: str
    source_commit: str
    files: Mapping[str, str]


class HermesSnapshotProvider(Protocol):
    """Authorized host boundary for obtaining a verified Hermes snapshot."""

    def snapshot(self) -> HermesSnapshot: ...


@dataclass(frozen=True)
class HermesAbsorptionResult:
    source_repository: str
    source_commit: str
    extracted: tuple[HermesCapabilityPattern, ...]
    decisions: tuple[PatternIntakeDecision, ...]
    candidates: tuple[ELOCapabilityCandidate, ...]


class HermesCapabilityAbsorptionRuntime:
    """Run the real extraction→intake→candidate pipeline without persistence."""

    def __init__(self, *, provider: HermesSnapshotProvider, intake: SymbiontPatternIntake | None = None) -> None:
        self.provider = provider
        self.intake = intake or SymbiontPatternIntake()

    def run(self, *, tenant_id: str) -> HermesAbsorptionResult:
        snapshot = self.provider.snapshot()
        if not snapshot.source_repository or not snapshot.source_commit:
            raise ValueError("Hermes snapshot requires repository and commit provenance")
        patterns = extract_patterns(snapshot.files)
        if not patterns:
            raise ValueError("Hermes snapshot contains no complete evidence-backed capability")

        decisions: list[PatternIntakeDecision] = []
        candidates: list[ELOCapabilityCandidate] = []
        for pattern in patterns:
            external = to_external_pattern(pattern, tenant_id=tenant_id, source_commit=snapshot.source_commit)
            decision = self.intake.classify(external)
            decisions.append(decision)
            if decision.candidate_creation_allowed:
                observation = to_observation(pattern, tenant_id=tenant_id, source_commit=snapshot.source_commit)
                candidate = SymbiontCapabilityAbsorber.absorb(
                    observation,
                    decision,
                    validation_contract="Hermes evidence + ELO Evolution Gate + laboratory regression",
                )
                if candidate is not None:
                    candidates.append(candidate)

        return HermesAbsorptionResult(
            source_repository=snapshot.source_repository,
            source_commit=snapshot.source_commit,
            extracted=patterns,
            decisions=tuple(decisions),
            candidates=tuple(candidates),
        )
