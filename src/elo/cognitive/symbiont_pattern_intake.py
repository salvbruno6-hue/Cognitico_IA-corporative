"""Controlled intake of external architectural patterns into the ELO Symbiont Lab.

This is deliberately an integration layer, not a second evolution engine. External
patterns enter through the existing laboratory/evidence boundary and are classified
by the canonical Evolution Gate before any learning candidate can be created.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

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




class CanonicalAuthorizationEvidence(Protocol):
    """Transport contract for an already-evaluated elo-authz decision."""

    authorized: bool
    authority: str
    evidence_ref: str


@dataclass(frozen=True)
class SkillComponent:
    """Evidence inventory for a required Skill component before intake."""

    name: str
    status: str
    path: str = ""
    gap: str = ""
    documentation_status: str = "MISSING"
    test_status: str = "UNTESTED"
    authorization_status: str = "UNKNOWN"
    authorization_authority: str = ""
    authorization_evidence_ref: str = ""
    compatibility_status: str = "UNKNOWN"
    baseline_status: str = "MISSING"
    measurement_status: str = "MISSING"
    regression_status: str = "UNKNOWN"

    def __post_init__(self) -> None:
        if self.status not in {"FOUND", "PARTIAL", "MISSING"}:
            raise ValueError(f"invalid component status: {self.status}")
        if self.documentation_status not in {"FOUND", "PARTIAL", "MISSING"}:
            raise ValueError("invalid documentation status")
        if self.test_status not in {"TESTED", "PARTIAL", "UNTESTED", "FAILED"}:
            raise ValueError("invalid test status")
        if self.authorization_status not in {"COMPATIBLE", "BLOCKED", "UNKNOWN"}:
            raise ValueError("invalid authorization status")
        if self.authorization_status == "COMPATIBLE" and self.authorization_authority != "elo-authz":
            raise ValueError("compatible authorization requires canonical elo-authz authority")
        if self.authorization_status == "COMPATIBLE" and not self.authorization_evidence_ref.strip():
            raise ValueError("compatible authorization requires evidence reference")
        if self.compatibility_status not in {"COMPATIBLE", "CONFLICT", "UNKNOWN"}:
            raise ValueError("invalid compatibility status")
        if self.baseline_status not in {"PRESENT", "MISSING"}:
            raise ValueError("invalid baseline status")
        if self.measurement_status not in {"PRESENT", "MISSING"}:
            raise ValueError("invalid measurement status")
        if self.regression_status not in {"PASS", "FAIL", "UNKNOWN"}:
            raise ValueError("invalid regression status")
        if not self.name.strip():
            raise ValueError("component name is required")


@dataclass(frozen=True)
class SkillCreationAssessment:
    """Evidence-based pre-intake result attached to the existing Pattern Intake."""

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

    @property
    def evidence_completeness(self) -> float:
        """Coverage of all required evidence dimensions, not a quality score."""
        if not self.components:
            return 0.0
        checks = []
        for component in self.components:
            checks.extend((
                component.status == "FOUND",
                component.documentation_status == "FOUND",
                component.test_status == "TESTED",
                component.authorization_status == "COMPATIBLE",
                component.compatibility_status == "COMPATIBLE",
                component.baseline_status == "PRESENT",
                component.measurement_status == "PRESENT",
                component.regression_status == "PASS",
            ))
        return round(sum(checks) / len(checks), 3)

    @property
    def blocking_gaps(self) -> tuple[str, ...]:
        gaps: list[str] = []
        for component in self.components:
            if component.status != "FOUND":
                gaps.append(f"{component.name}: component={component.status}")
            if component.documentation_status != "FOUND":
                gaps.append(f"{component.name}: documentation={component.documentation_status}")
            if component.test_status != "TESTED":
                gaps.append(f"{component.name}: test={component.test_status}")
            if component.authorization_status != "COMPATIBLE":
                gaps.append(f"{component.name}: authorization={component.authorization_status}")
            if component.authorization_status == "COMPATIBLE" and component.authorization_authority != "elo-authz":
                gaps.append(f"{component.name}: authorization_authority={component.authorization_authority or 'MISSING'}")
            if component.authorization_status == "COMPATIBLE" and not component.authorization_evidence_ref.strip():
                gaps.append(f"{component.name}: authorization_evidence_ref=MISSING")
            if component.compatibility_status != "COMPATIBLE":
                gaps.append(f"{component.name}: compatibility={component.compatibility_status}")
            if component.baseline_status != "PRESENT":
                gaps.append(f"{component.name}: baseline={component.baseline_status}")
            if component.measurement_status != "PRESENT":
                gaps.append(f"{component.name}: measurement={component.measurement_status}")
            if component.regression_status != "PASS":
                gaps.append(f"{component.name}: regression={component.regression_status}")
        return tuple(gaps)


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
        authorization_decision: CanonicalAuthorizationEvidence | None = None,
    ) -> SkillCreationAssessment:
        """Reconcile a proposed Skill before intake using the existing Symbiont flow."""
        if not proposed_skill_id.strip():
            raise ValueError("proposed_skill_id is required")

        inventory = tuple(components)
        resolved_owner = None
        if skill_resolver is not None and domain_family:
            resolution = skill_resolver.resolve(domain_family=domain_family)
            if resolution.resolved:
                resolved_owner = resolution.skill_id
            elif existing_owner:
                return SkillCreationAssessment(
                    proposed_skill_id, None, inventory, 0.0, "DEVELOP_FIRST",
                    "caller-supplied owner was not independently resolved by the canonical SpecialistSkillResolver"
                )
        elif existing_owner:
            return SkillCreationAssessment(
                proposed_skill_id, None, inventory, 0.0, "DEVELOP_FIRST",
                "existing_owner requires independent verification through the canonical SpecialistSkillResolver"
            )
        if not inventory:
            return SkillCreationAssessment(
                proposed_skill_id, resolved_owner, (), 0.0, "DEVELOP_FIRST",
                "required components were not supplied; develop the base before intake"
            )
        if resolved_owner:
            return SkillCreationAssessment(
                proposed_skill_id, resolved_owner, inventory, 0.0, "REUSE",
                "canonical SpecialistSkillResolver identified an existing owner; do not create a duplicate Skill"
            )
        requires_authorization_decision = any(
            component.authorization_status == "COMPATIBLE" for component in inventory
        )
        if requires_authorization_decision:
            if authorization_decision is None:
                return SkillCreationAssessment(
                    proposed_skill_id, None, inventory, 0.0, "DEVELOP_FIRST",
                    "canonical authorization decision is required for pre-intake evaluation"
                )
            if authorization_decision.authority != "elo-authz":
                return SkillCreationAssessment(
                    proposed_skill_id, None, inventory, 0.0, "DEVELOP_FIRST",
                    "authorization decision provenance is not canonical"
                )
            if not authorization_decision.authorized:
                return SkillCreationAssessment(
                    proposed_skill_id, None, inventory, 0.0, "DEVELOP_FIRST",
                    "canonical authorization decision was not granted"
                )
            if not authorization_decision.evidence_ref.strip():
                return SkillCreationAssessment(
                    proposed_skill_id, None, inventory, 0.0, "DEVELOP_FIRST",
                    "canonical authorization decision has no evidence reference"
                )
            for component in inventory:
                if component.authorization_status == "COMPATIBLE" and (
                    component.authorization_authority != authorization_decision.authority
                    or component.authorization_evidence_ref != authorization_decision.evidence_ref
                ):
                    return SkillCreationAssessment(
                        proposed_skill_id, None, inventory, 0.0, "DEVELOP_FIRST",
                        f"authorization evidence for {component.name} does not match the canonical decision"
                    )

        complete = all(
            item.status == "FOUND"
            and item.documentation_status == "FOUND"
            and item.test_status == "TESTED"
            and item.authorization_status == "COMPATIBLE"
            and item.compatibility_status == "COMPATIBLE"
            and item.baseline_status == "PRESENT"
            and item.measurement_status == "PRESENT"
            and item.regression_status == "PASS"
            for item in inventory
        )
        if not complete:
            return SkillCreationAssessment(
                proposed_skill_id, None, inventory,
                SkillCreationAssessment(
                    proposed_skill_id, None, inventory, 0.0, "DEVELOP_FIRST", ""
                ).evidence_completeness,
                "DEVELOP_FIRST",
                "required component, documentation, test, authorization, compatibility, baseline, measurement or regression evidence is incomplete"
            )
        return SkillCreationAssessment(
            proposed_skill_id, None, inventory, 1.0, "READY_FOR_INTAKE",
            "required components and pre-intake evidence are complete; no existing owner was independently identified"
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
