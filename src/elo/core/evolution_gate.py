"""Provider-neutral executable Evolution Gate for canonical ELO changes.

The gate classifies proposals; it does not mutate Soul/Core or execute merges.
Alternatives remain explicitly non-canonical until a governed promotion occurs.
"""
from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class EvolutionClassification(StrEnum):
    COMPATIBLE = "COMPATIBLE"
    ADAPT_REQUIRED = "ADAPT_REQUIRED"
    EVOLUTIONARY_CONFLICT = "EVOLUTIONARY_CONFLICT"
    INCOMPATIBLE = "INCOMPATIBLE"
    DUPLICATE_SUPERSEDED = "DUPLICATE/SUPERSEDED"


@dataclass(frozen=True)
class EvolutionProposal:
    proposal_id: str
    tenant_id: str
    source_id: str
    summary: str
    purpose_alignment: bool
    identity_compatible: bool
    architecture_compatible: bool
    governance_compatible: bool
    evidence_ids: tuple[str, ...] = ()
    maturity_score: float = 0.0
    existing_owner: str | None = None
    provenance: Mapping[str, str] = None  # type: ignore[assignment]
    skill_id: str | None = None

    def __post_init__(self) -> None:
        if not all((self.proposal_id, self.tenant_id, self.source_id, self.summary)):
            raise ValueError("proposal identity fields are required")
        if not 0.0 <= self.maturity_score <= 1.0:
            raise ValueError("maturity_score must be between 0 and 1")
        if self.provenance is None or not self.provenance:
            raise ValueError("provenance is required")
        provenance_skill = self.provenance.get("skill_id")
        if self.skill_id and provenance_skill is not None and provenance_skill != self.skill_id:
            raise ValueError("provenance skill_id must match proposal skill_id")


@dataclass(frozen=True)
class EvolutionDecision:
    proposal_id: str
    classification: EvolutionClassification
    canonical_mutation_allowed: bool
    preserve_as_alternative: bool
    human_decision_required: bool
    rationale: str
    evidence_ids: tuple[str, ...]


class EvolutionGate:
    """Deterministic classification boundary; never changes canonical state."""

    def evaluate(self, proposal: EvolutionProposal) -> EvolutionDecision:
        if proposal.existing_owner:
            return EvolutionDecision(proposal.proposal_id, EvolutionClassification.DUPLICATE_SUPERSEDED,
                                     False, False, False, "existing canonical owner must be reused", proposal.evidence_ids)
        if not proposal.identity_compatible or not proposal.governance_compatible:
            return EvolutionDecision(proposal.proposal_id, EvolutionClassification.INCOMPATIBLE,
                                     False, False, True, "identity or non-negotiable governance conflict", proposal.evidence_ids)
        if not proposal.purpose_alignment:
            return EvolutionDecision(proposal.proposal_id, EvolutionClassification.EVOLUTIONARY_CONFLICT,
                                     False, True, True, "purpose alignment is unresolved", proposal.evidence_ids)
        if not proposal.architecture_compatible:
            return EvolutionDecision(proposal.proposal_id, EvolutionClassification.EVOLUTIONARY_CONFLICT,
                                     False, True, True, "architecture conflict requires explicit evolution decision", proposal.evidence_ids)
        if not proposal.evidence_ids or proposal.maturity_score < 0.5:
            return EvolutionDecision(proposal.proposal_id, EvolutionClassification.ADAPT_REQUIRED,
                                     False, True, False, "compatible direction but evidence/maturity is incomplete", proposal.evidence_ids)
        return EvolutionDecision(proposal.proposal_id, EvolutionClassification.COMPATIBLE,
                                 False, False, False, "compatible proposal; promotion remains a separate governed action", proposal.evidence_ids)
