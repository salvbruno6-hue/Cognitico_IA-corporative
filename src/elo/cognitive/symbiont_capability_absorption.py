"""Governed conversion of external capabilities into ELO-native candidates.

The Symbiont may learn from Hermes or another external intelligence runtime, but it
must not copy external implementation details into the ELO Core automatically. This
module extracts a portable capability contract and leaves materialization/promotion
to the existing learning and Evolution Gate authorities.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from elo.cognitive.symbiont_pattern_intake import ExternalPatternInput, PatternIntakeDecision
from elo.core.evolution_gate import EvolutionClassification


class CapabilityState(StrEnum):
    EXTERNAL = "EXTERNAL"
    CANDIDATE = "CANDIDATE"
    NATIVE_PENDING_VALIDATION = "NATIVE_PENDING_VALIDATION"


@dataclass(frozen=True)
class ExternalCapabilityObservation:
    """Description of a capability observed in an external runtime."""

    capability_id: str
    provider: str
    capability: str
    purpose: str
    mechanism: str
    interface_contract: str
    evidence_ids: tuple[str, ...]
    source_ref: str
    source_commit: str
    tenant_id: str
    domain: str
    risk: str = "LOW"


@dataclass(frozen=True)
class ELOCapabilityCandidate:
    """Portable capability definition awaiting governed validation."""

    capability_id: str
    tenant_id: str
    domain: str
    title: str
    portable_principle: str
    interface_contract: str
    validation_contract: str
    source_ref: str
    source_commit: str
    evidence_ids: tuple[str, ...]
    provenance: dict[str, str]
    state: CapabilityState = CapabilityState.CANDIDATE


class SymbiontCapabilityAbsorber:
    """Extract a reusable ELO capability from an externally observed pattern."""

    @staticmethod
    def absorb(
        observation: ExternalCapabilityObservation,
        intake: PatternIntakeDecision,
        *,
        validation_contract: str,
    ) -> ELOCapabilityCandidate | None:
        """Create only a candidate; never writes or mutates canonical ELO state."""
        SymbiontCapabilityAbsorber._validate(observation, intake, validation_contract)

        if intake.classification is not EvolutionClassification.COMPATIBLE:
            return None

        return ELOCapabilityCandidate(
            capability_id=observation.capability_id,
            tenant_id=observation.tenant_id,
            domain=observation.domain,
            title=observation.capability.strip(),
            portable_principle=observation.mechanism.strip(),
            interface_contract=observation.interface_contract.strip(),
            validation_contract=validation_contract.strip(),
            source_ref=observation.source_ref,
            source_commit=observation.source_commit,
            evidence_ids=observation.evidence_ids,
            provenance={
                "provider": observation.provider,
                "source_ref": observation.source_ref,
                "source_commit": observation.source_commit,
                "pattern_id": intake.pattern.pattern_id,
                "origin": "symbiont-external-capability",
            },
        )

    @staticmethod
    def _validate(
        observation: ExternalCapabilityObservation,
        intake: PatternIntakeDecision,
        validation_contract: str,
    ) -> None:
        required = (
            observation.capability_id,
            observation.provider,
            observation.capability,
            observation.purpose,
            observation.mechanism,
            observation.interface_contract,
            observation.source_ref,
            observation.source_commit,
            observation.tenant_id,
            observation.domain,
            validation_contract,
        )
        if not all(required):
            raise ValueError("external capability requires identity, mechanism, contract and provenance")
        if not observation.evidence_ids:
            raise ValueError("external capability requires evidence")
        if observation.tenant_id != intake.pattern.tenant_id:
            raise ValueError("capability tenant does not match pattern intake")
        if observation.source_ref != intake.pattern.source_ref:
            raise ValueError("capability source does not match pattern intake")
        if observation.source_commit != intake.pattern.source_commit:
            raise ValueError("capability source commit does not match pattern intake")
        if observation.risk.upper() in {"CRITICAL", "CRITICO"}:
            raise ValueError("critical-risk capability cannot enter absorption")
