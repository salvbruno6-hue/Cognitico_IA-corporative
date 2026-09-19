"""Governed loops for turning Hermes capability evidence into native ELO capabilities.

The loops are deliberately separated:
1. Discovery/test loop: find evidence, map invariants, and test a capability safely.
2. Transformation loop: convert validated evidence into an ELO-native function,
   structure, or skill candidate without importing Hermes as a runtime dependency.
3. Approval-readiness loop: verify that the transformed candidate is complete for
   Evolution Gate review. This loop never approves or promotes by itself.

No business operation is executed and Hermes is never mutated.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Callable, Iterable, Mapping


class CapabilityKind(str, Enum):
    FUNCTION = "function"
    STRUCTURE = "structure"
    SKILL = "skill"


class CapabilityState(str, Enum):
    DISCOVERED = "discovered"
    TESTING = "testing"
    INCONSISTENT = "inconsistent"
    TRANSFORMING = "transforming"
    TRANSFORMED = "transformed"
    READY_FOR_APPROVAL = "ready_for_approval"
    CANDIDATE = "candidate"


@dataclass(frozen=True)
class CapabilityEvidence:
    mechanism_id: str
    source: str
    revision: str
    interface: str
    invariants: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    relations: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class DiscoveryTestResult:
    mechanism_id: str
    iteration: int
    consistent: bool
    test_passed: bool
    issues: tuple[str, ...] = ()


@dataclass(frozen=True)
class TransformationCandidate:
    mechanism_id: str
    candidate_id: str
    kind: CapabilityKind
    state: CapabilityState
    native_name: str
    contract: tuple[str, ...]
    source: str
    revision: str
    evidence_refs: tuple[str, ...]
    invariants: tuple[str, ...]
    dependencies: tuple[str, ...]
    relations: tuple[str, ...]
    transformation_notes: tuple[str, ...] = ()
    variant: int = 0


@dataclass(frozen=True)
class ApprovalReadiness:
    candidate_id: str
    ready: bool
    missing: tuple[str, ...]
    checks: Mapping[str, bool] = field(default_factory=dict)


DiscoveryEvaluator = Callable[[CapabilityEvidence], tuple[bool, tuple[str, ...]]]
DiscoveryTester = Callable[[CapabilityEvidence], bool]
EvidenceAdjuster = Callable[[CapabilityEvidence, tuple[str, ...], int], CapabilityEvidence]
TransformationBuilder = Callable[[CapabilityEvidence, CapabilityKind, int], TransformationCandidate]
TransformationTester = Callable[[TransformationCandidate], tuple[bool, tuple[str, ...]]]


class HermesCapabilityLoops:
    """Three bounded loops: discovery/test, transformation, approval-readiness."""

    @staticmethod
    def discover_and_test(
        evidence: CapabilityEvidence,
        *,
        evaluate: DiscoveryEvaluator,
        test: DiscoveryTester,
        adjust: EvidenceAdjuster,
        max_iterations: int = 5,
    ) -> tuple[CapabilityEvidence, tuple[DiscoveryTestResult, ...]]:
        """Iterate evidence checks until consistent+tested or bounded out."""
        if max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
        current = evidence
        history: list[DiscoveryTestResult] = []
        for iteration in range(1, max_iterations + 1):
            consistent, issues = evaluate(current)
            passed = test(current) if consistent else False
            history.append(
                DiscoveryTestResult(
                    mechanism_id=current.mechanism_id,
                    iteration=iteration,
                    consistent=consistent,
                    test_passed=passed,
                    issues=tuple(issues),
                )
            )
            if consistent and passed:
                return current, tuple(history)
            reasons = tuple(issues) or ("controlled test failed",)
            adjusted = adjust(current, reasons, iteration)
            if adjusted.mechanism_id != evidence.mechanism_id:
                raise ValueError("discovery adjustment cannot change mechanism identity")
            if adjusted.source != evidence.source or adjusted.revision != evidence.revision:
                raise ValueError("discovery adjustment cannot change evidence provenance")
            current = adjusted
        return current, tuple(history)

    @staticmethod
    def transform_until_valid(
        evidence: CapabilityEvidence,
        *,
        kind: CapabilityKind,
        build: TransformationBuilder,
        test: TransformationTester,
        max_iterations: int = 5,
    ) -> tuple[TransformationCandidate, tuple[str, ...]]:
        """Create native ELO variants until the transformed contract passes."""
        if max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
        notes: list[str] = []
        for variant in range(max_iterations):
            candidate = build(evidence, kind, variant)
            if candidate.mechanism_id != evidence.mechanism_id:
                raise ValueError("transformation cannot change mechanism identity")
            if candidate.source != evidence.source or candidate.revision != evidence.revision:
                raise ValueError("transformation cannot change provenance")
            passed, issues = test(candidate)
            if passed:
                return replace(candidate, state=CapabilityState.TRANSFORMED, variant=variant), tuple(notes)
            notes.extend(issues or ("native transformation test failed",))
        return replace(candidate, state=CapabilityState.CANDIDATE, transformation_notes=tuple(notes)), tuple(notes)

    @staticmethod
    def approval_readiness(
        candidate: TransformationCandidate,
        *,
        implementation_passed: bool,
        provenance_passed: bool,
        consistency_passed: bool,
        governance_metadata_complete: bool,
        evolution_gate_approved: bool = False,
    ) -> ApprovalReadiness:
        """Check readiness for Evolution Gate; never grant approval itself."""
        checks = {
            "implementation_test": implementation_passed,
            "provenance": provenance_passed,
            "consistency": consistency_passed,
            "governance_metadata": governance_metadata_complete,
            "evolution_gate": evolution_gate_approved,
            "native_contract": bool(candidate.contract),
            "evidence": bool(candidate.evidence_refs),
            "invariants": bool(candidate.invariants),
        }
        missing = tuple(name for name, passed in checks.items() if not passed)
        return ApprovalReadiness(
            candidate_id=candidate.candidate_id,
            ready=not missing,
            missing=missing,
            checks=checks,
        )

    @staticmethod
    def run_pipeline(
        evidence: CapabilityEvidence,
        *,
        kind: CapabilityKind,
        evaluate: DiscoveryEvaluator,
        discovery_test: DiscoveryTester,
        adjust: EvidenceAdjuster,
        build: TransformationBuilder,
        transformation_test: TransformationTester,
        approval: Mapping[str, bool],
        max_iterations: int = 5,
    ) -> tuple[CapabilityEvidence, tuple[DiscoveryTestResult, ...], TransformationCandidate, ApprovalReadiness]:
        """Run all three loops without performing approval or promotion."""
        stable, discovery_history = HermesCapabilityLoops.discover_and_test(
            evidence,
            evaluate=evaluate,
            test=discovery_test,
            adjust=adjust,
            max_iterations=max_iterations,
        )
        candidate, _ = HermesCapabilityLoops.transform_until_valid(
            stable,
            kind=kind,
            build=build,
            test=transformation_test,
            max_iterations=max_iterations,
        )
        readiness = HermesCapabilityLoops.approval_readiness(
            candidate,
            implementation_passed=approval.get("implementation_test", False),
            provenance_passed=approval.get("provenance", False),
            consistency_passed=approval.get("consistency", False),
            governance_metadata_complete=approval.get("governance_metadata", False),
            evolution_gate_approved=approval.get("evolution_gate", False),
        )
        return stable, discovery_history, candidate, readiness

@dataclass(frozen=True)
class ImplementationDecision:
    """Explicit ELO decision authorizing implementation of an already-approved candidate."""

    decision_id: str
    candidate_id: str
    approved: bool
    scope: str
    evidence_refs: tuple[str, ...] = ()
    authority: str = "elo_cognitive"


@dataclass(frozen=True)
class ImplementationActivation:
    """Auditable result of the approval -> implementation handoff."""

    decision_id: str
    candidate_id: str
    state: str
    activated: bool
    scope: str
    reason: str = ""


class ApprovedCandidateImplementationLoop:
    """Fail-closed loop from approved candidate to controlled implementation.

    Approval and implementation are separate decisions. This loop never grants
    Evolution Gate approval and never promotes a candidate by itself. It only
    activates a candidate after all prior approval gates are already satisfied
    and an explicit implementation decision authorizes that candidate.
    """

    @staticmethod
    def activate(
        candidate: TransformationCandidate,
        *,
        readiness: ApprovalReadiness,
        decision: ImplementationDecision,
    ) -> ImplementationActivation:
        if decision.candidate_id != candidate.candidate_id:
            raise ValueError("implementation decision does not match candidate")
        if not decision.decision_id:
            raise ValueError("implementation decision requires decision_id")
        if not decision.scope:
            raise ValueError("implementation decision requires scope")
        if not decision.evidence_refs:
            raise ValueError("implementation decision requires evidence_refs")
        if not decision.approved:
            return ImplementationActivation(
                decision_id=decision.decision_id,
                candidate_id=candidate.candidate_id,
                state="BLOCKED",
                activated=False,
                scope=decision.scope,
                reason="implementation decision not approved",
            )
        if not readiness.ready:
            return ImplementationActivation(
                decision_id=decision.decision_id,
                candidate_id=candidate.candidate_id,
                state="BLOCKED",
                activated=False,
                scope=decision.scope,
                reason="candidate is not fully approved",
            )
        return ImplementationActivation(
            decision_id=decision.decision_id,
            candidate_id=candidate.candidate_id,
            state="IMPLEMENTATION_AUTHORIZED",
            activated=True,
            scope=decision.scope,
        )
