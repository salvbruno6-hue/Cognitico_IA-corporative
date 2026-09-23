"""Controlled intake of external architectural patterns into the ELO Symbiont Lab.

This is deliberately an integration layer, not a second evolution engine. External
patterns enter through the existing laboratory/evidence boundary and are classified
by the canonical Evolution Gate before any learning candidate can be created.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from elo.core.evolution_gate import EvolutionClassification, EvolutionGate, EvolutionProposal
from elo.core.specialist_skill_resolution import SpecialistSkillResolver
from elo.cognitive.symbionte_lab import SymbiontLabObservation


@dataclass(frozen=True)
class ExternalPatternInput:
    """Minimal evidence-bearing description of an external pattern."""

    pattern_id: str
    tenant_id: str
    domain: str
    source_ref: str
    source_commit: str
    problem: str
    mechanism: str
    evidence_ids: tuple[str, ...]
    existing_owner: str | None = None
    scope: str = "symbiont-lab"
    tenant_scope: str | None = None
    source_kind: str = "repository"
    risk: str = "LOW"


@dataclass(frozen=True)
class PatternIntakeDecision:
    """Classification result; never mutates canonical ELO state."""

    pattern: ExternalPatternInput
    classification: EvolutionClassification
    disposition: str
    rationale: str
    proposal: EvolutionProposal

    @property
    def candidate_creation_allowed(self) -> bool:
        """Only compatible proposals may continue to the existing lab pipeline."""
        return self.classification is EvolutionClassification.COMPATIBLE



@dataclass(frozen=True)
class SkillComponent:
    """Evidence-only component inventory used before a new Skill is proposed."""

    name: str
    status: str
    path: str = ""
    gap: str = ""

    def __post_init__(self) -> None:
        if self.status not in {"FOUND", "PARTIAL", "MISSING"}:
            raise ValueError(f"invalid component status: {self.status}")
        if not self.name.strip():
            raise ValueError("component name is required")


@dataclass(frozen=True)
class SkillCreationAssessment:
    """Pre-intake result attached to the existing Symbiont Pattern Intake."""

    proposed_skill_id: str
    existing_owner: str | None
    components: tuple[SkillComponent, ...]
    readiness_score: float
    disposition: str
    rationale: str

    @property
    def ready_for_intake(self) -> bool:
        return self.disposition == "READY_FOR_INTAKE"

    @property
    def evidence(self) -> tuple[str, ...]:
        """Expose only evidence supplied by the component inventory."""
        return tuple(
            f"{component.name}: {component.path or component.status}"
            + (f" — {component.gap}" if component.gap else "")
            for component in self.components
        )


class SymbiontPatternIntake:
    """Attach external pattern discovery to the existing ELO cognitive spine."""

    def __init__(self, gate: EvolutionGate | None = None) -> None:
        self.gate = gate or EvolutionGate()


    def assess_skill_creation(
        self,
        *,
        proposed_skill_id: str,
        existing_owner: str | None,
        components: Iterable[SkillComponent],
        domain_family: str | None = None,
        skill_resolver: SpecialistSkillResolver | None = None,
    ) -> SkillCreationAssessment:
        """Reconcile a proposed Skill before intake using the existing Symbiont flow."""
        if not proposed_skill_id.strip():
            raise ValueError("proposed_skill_id is required")
        inventory = tuple(components)
        resolved_owner = existing_owner
        if resolved_owner is None and domain_family and skill_resolver is not None:
            resolution = skill_resolver.resolve(domain_family=domain_family)
            if resolution.resolved:
                resolved_owner = resolution.skill_id
        if not inventory:
            return SkillCreationAssessment(
                proposed_skill_id, resolved_owner, (), 0.0, "DEVELOP_FIRST",
                "required components were not supplied; develop the base before intake"
            )
        if resolved_owner:
            return SkillCreationAssessment(
                proposed_skill_id, resolved_owner, inventory, 0.0, "REUSE",
                "an existing owner is already identified; do not create a duplicate Skill"
            )
        found = sum(item.status == "FOUND" for item in inventory)
        readiness = round(found / len(inventory), 3)
        if found != len(inventory):
            return SkillCreationAssessment(
                proposed_skill_id, None, inventory, readiness, "DEVELOP_FIRST",
                "one or more required components are missing or partial"
            )
        return SkillCreationAssessment(
            proposed_skill_id, None, inventory, 1.0, "READY_FOR_INTAKE",
            "required components are evidenced and no existing owner was identified"
        )

    def classify(self, pattern: ExternalPatternInput) -> PatternIntakeDecision:
        self._validate(pattern)
        proposal = EvolutionProposal(
            proposal_id=pattern.pattern_id,
            tenant_id=pattern.tenant_id,
            source_id=pattern.source_ref,
            summary=f"{pattern.problem}: {pattern.mechanism}",
            purpose_alignment=True,
            identity_compatible=True,
            architecture_compatible=True,
            governance_compatible=True,
            evidence_ids=pattern.evidence_ids,
            maturity_score=0.0 if not pattern.evidence_ids else 0.5,
            existing_owner=pattern.existing_owner,
            provenance={
                "source_ref": pattern.source_ref,
                "source_commit": pattern.source_commit,
                "source_kind": pattern.source_kind,
                "scope": pattern.scope,
            },
        )
        decision = self.gate.evaluate(proposal)
        disposition = {
            EvolutionClassification.DUPLICATE_SUPERSEDED: "REUSE",
            EvolutionClassification.ADAPT_REQUIRED: "LAB_EXPERIMENT",
            EvolutionClassification.EVOLUTIONARY_CONFLICT: "BLOCK",
            EvolutionClassification.INCOMPATIBLE: "BLOCK",
            EvolutionClassification.COMPATIBLE: "LAB_CANDIDATE",
        }[decision.classification]
        return PatternIntakeDecision(
            pattern=pattern,
            classification=decision.classification,
            disposition=disposition,
            rationale=decision.rationale,
            proposal=proposal,
        )

    @staticmethod
    def to_lab_observation(
        pattern: ExternalPatternInput,
        *,
        expected_outcome: str,
        observed_outcome: str,
        decision_id: str,
        baseline: str,
        experiment: str,
        result: str,
        regression_status: str,
        generalization_status: str,
        hypothesis: str | None = None,
    ) -> SymbiontLabObservation:
        """Convert a classified external pattern into the existing LAB_ONLY schema."""
        return SymbiontLabObservation(
            observation_id=pattern.pattern_id,
            tenant_id=pattern.tenant_id,
            domain=pattern.domain,
            decision_id=decision_id,
            expected_outcome=expected_outcome,
            observed_outcome=observed_outcome,
            evidence_ids=pattern.evidence_ids,
            source_ref=pattern.source_ref,
            source_commit=pattern.source_commit,
            hypothesis=hypothesis or pattern.mechanism,
            baseline=baseline,
            experiment=experiment,
            result=result,
            regression_status=regression_status,
            generalization_status=generalization_status,
            risk=pattern.risk,
            existing_owner=pattern.existing_owner,
            scope=pattern.scope,
            tenant_scope=pattern.tenant_scope,
            source_kind=pattern.source_kind,
        )

    @staticmethod
    def _validate(pattern: ExternalPatternInput) -> None:
        if not all(
            (
                pattern.pattern_id,
                pattern.tenant_id,
                pattern.domain,
                pattern.source_ref,
                pattern.source_commit,
                pattern.problem,
                pattern.mechanism,
                pattern.scope,
            )
        ):
            raise ValueError("external pattern requires identity, provenance, problem and mechanism")
        if not pattern.evidence_ids:
            raise ValueError("external pattern requires evidence before architectural classification")
        if pattern.tenant_scope and pattern.tenant_scope != pattern.tenant_id:
            raise ValueError("tenant scope does not match tenant identity")
