"""Governed meta-evolution engine for the ELO Symbiont.

The Symbiont may discover external architectural patterns, analyze them against
ELO's structural invariants, build isolated candidates, run deterministic gates,
and prepare an approval package. It never promotes a candidate to ELO authority.

The design borrows general patterns observed in self-evolving agent systems:
trace-first execution, reproducible manifests, baseline comparison, reflective
failure analysis, isolated candidate work, benchmark/regression gates and
human-controlled promotion. It does not copy an external runtime or grant an
external system authority over ELO.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
from typing import Iterable, Mapping, Sequence


class CandidateDisposition(str, Enum):
    REUSE = "REUSE"
    EXTEND = "EXTEND"
    CONSOLIDATE = "CONSOLIDATE"
    CANDIDATE = "CANDIDATE"
    BLOCK = "BLOCK"


class GateStatus(str, Enum):
    READY_FOR_APPROVAL = "READY_FOR_APPROVAL"
    BLOCKED = "BLOCKED"
    EXPERIMENTAL = "EXPERIMENTAL"


@dataclass(frozen=True)
class ArchitecturalInvariant:
    key: str
    description: str
    protected: bool = True


@dataclass(frozen=True)
class ELOStructuralModel:
    """Compact machine-readable representation of ELO's architectural spine."""

    version: str
    authorities: tuple[str, ...]
    components: tuple[str, ...]
    invariants: tuple[ArchitecturalInvariant, ...]
    capabilities: tuple[str, ...] = ()
    known_patterns: tuple[str, ...] = ()

    def invariant_keys(self) -> frozenset[str]:
        return frozenset(item.key for item in self.invariants if item.protected)


@dataclass(frozen=True)
class ExternalPattern:
    pattern_id: str
    name: str
    source: str
    source_ref: str
    source_commit: str
    problem: str
    mechanism: str
    evidence: tuple[str, ...]
    required_invariants: tuple[str, ...]
    risk: str = "MEDIUM"
    metadata: Mapping[str, str] = field(default_factory=dict)

    @property
    def fingerprint(self) -> str:
        payload = {
            "name": self.name,
            "source": self.source,
            "source_commit": self.source_commit,
            "mechanism": self.mechanism,
        }
        return sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class EvolutionTrace:
    event_type: str
    event_id: str
    candidate_id: str
    payload: Mapping[str, object]


@dataclass(frozen=True)
class CandidateVariant:
    candidate_id: str
    pattern_id: str
    baseline_version: str
    candidate_version: str
    disposition: CandidateDisposition
    hypothesis: str
    proposed_changes: tuple[str, ...]
    protected_invariants: tuple[str, ...]
    branch_ref: str
    source_fingerprint: str


@dataclass(frozen=True)
class EvaluationResult:
    candidate_id: str
    tests_passed: bool
    regressions_passed: bool
    benchmark_improved: bool
    isolation_passed: bool
    provenance_passed: bool
    authority_boundary_passed: bool
    evidence_ids: tuple[str, ...]
    metrics: Mapping[str, float]
    failure_reasons: tuple[str, ...] = ()

    @property
    def passed(self) -> bool:
        return all(
            (
                self.tests_passed,
                self.regressions_passed,
                self.isolation_passed,
                self.provenance_passed,
                self.authority_boundary_passed,
            )
        )


@dataclass(frozen=True)
class ApprovalPackage:
    candidate: CandidateVariant
    evaluation: EvaluationResult
    status: GateStatus
    summary: str
    required_approval: str
    traces: tuple[EvolutionTrace, ...]


class SymbiontMetaEvolutionEngine:
    """Identify, adapt, test and prepare external capabilities for ELO review."""

    def __init__(self, structural_model: ELOStructuralModel) -> None:
        self.model = structural_model
        self._traces: list[EvolutionTrace] = []

    def classify(self, pattern: ExternalPattern) -> CandidateDisposition:
        """Apply reuse-before-create against the ELO structural model."""
        known = {value.casefold() for value in self.model.known_patterns}
        capabilities = {value.casefold() for value in self.model.capabilities}
        name = pattern.name.casefold()
        mechanism = pattern.mechanism.casefold()

        if name in known or mechanism in capabilities:
            return CandidateDisposition.REUSE

        required = set(pattern.required_invariants)
        if required and not required.issubset(self.model.invariant_keys()):
            return CandidateDisposition.BLOCK

        for component in self.model.components:
            if component.casefold() in name or component.casefold() in mechanism:
                return CandidateDisposition.EXTEND

        return CandidateDisposition.CANDIDATE

    def prepare_candidate(
        self,
        pattern: ExternalPattern,
        *,
        candidate_id: str,
        branch_ref: str,
        proposed_changes: Sequence[str],
    ) -> CandidateVariant:
        disposition = self.classify(pattern)
        if disposition in {CandidateDisposition.REUSE, CandidateDisposition.BLOCK}:
            proposed_changes = ()

        candidate = CandidateVariant(
            candidate_id=candidate_id,
            pattern_id=pattern.pattern_id,
            baseline_version=self.model.version,
            candidate_version=f"{self.model.version}+symbiont.{candidate_id}",
            disposition=disposition,
            hypothesis=(
                f"Adapt '{pattern.name}' to strengthen ELO without changing canonical authority."
            ),
            proposed_changes=tuple(proposed_changes),
            protected_invariants=tuple(sorted(pattern.required_invariants)),
            branch_ref=branch_ref,
            source_fingerprint=pattern.fingerprint,
        )
        self._trace(candidate_id, "candidate_prepared", {"disposition": disposition.value})
        return candidate

    def evaluate(
        self,
        candidate: CandidateVariant,
        *,
        tests_passed: bool,
        regressions_passed: bool,
        benchmark_improved: bool,
        isolation_passed: bool = True,
        provenance_passed: bool = True,
        authority_boundary_passed: bool = True,
        evidence_ids: Iterable[str] = (),
        metrics: Mapping[str, float] | None = None,
        failure_reasons: Iterable[str] = (),
    ) -> EvaluationResult:
        result = EvaluationResult(
            candidate_id=candidate.candidate_id,
            tests_passed=tests_passed,
            regressions_passed=regressions_passed,
            benchmark_improved=benchmark_improved,
            isolation_passed=isolation_passed,
            provenance_passed=provenance_passed,
            authority_boundary_passed=authority_boundary_passed,
            evidence_ids=tuple(evidence_ids),
            metrics=dict(metrics or {}),
            failure_reasons=tuple(failure_reasons),
        )
        self._trace(
            candidate.candidate_id,
            "evaluation_completed",
            {"passed": result.passed, "benchmark_improved": benchmark_improved},
        )
        return result

    def approval_package(
        self, candidate: CandidateVariant, evaluation: EvaluationResult
    ) -> ApprovalPackage:
        if candidate.disposition in {CandidateDisposition.REUSE, CandidateDisposition.BLOCK}:
            status = GateStatus.BLOCKED if candidate.disposition is CandidateDisposition.BLOCK else GateStatus.EXPERIMENTAL
        elif not evaluation.passed:
            status = GateStatus.BLOCKED
        elif not evaluation.benchmark_improved:
            status = GateStatus.EXPERIMENTAL
        else:
            status = GateStatus.READY_FOR_APPROVAL

        self._trace(candidate.candidate_id, "approval_package_prepared", {"status": status.value})
        return ApprovalPackage(
            candidate=candidate,
            evaluation=evaluation,
            status=status,
            summary=self._summary(candidate, evaluation, status),
            required_approval="HUMAN_EVOLUTION_GATE",
            traces=tuple(self._traces_for(candidate.candidate_id)),
        )

    def _trace(self, candidate_id: str, event_type: str, payload: Mapping[str, object]) -> None:
        event_id = sha256(
            f"{candidate_id}:{len(self._traces)}:{event_type}".encode()
        ).hexdigest()[:16]
        self._traces.append(EvolutionTrace(event_type, event_id, candidate_id, dict(payload)))

    def _traces_for(self, candidate_id: str) -> list[EvolutionTrace]:
        return [trace for trace in self._traces if trace.candidate_id == candidate_id]

    @staticmethod
    def _summary(
        candidate: CandidateVariant, evaluation: EvaluationResult, status: GateStatus
    ) -> str:
        if status is GateStatus.READY_FOR_APPROVAL:
            return "Candidate passed execution, regression, isolation, provenance and authority gates and is ready for human approval."
        if status is GateStatus.EXPERIMENTAL:
            return "Candidate remains experimental because evidence is insufficient for governed promotion."
        return "Candidate is blocked and must not be promoted to ELO authority."
