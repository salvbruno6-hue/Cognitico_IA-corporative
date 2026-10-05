"""Read-only consultive builder for structured orchestration orientation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping

from elo.cognitive.routing.execution_routing import RoutingDecision
from elo.core.context_resolution import ContextEvidence
from elo.core.execution_boundary import ExecutionOutcome
from elo.evidence import Evidence


OrientationFact = Evidence | ContextEvidence


class OrientationConfidence(StrEnum):
    """Semantic orientation confidence; not a numeric probability."""

    ALIGNED = "aligned"
    PARTIAL = "partial"
    INSUFFICIENT = "insufficient"


@dataclass(frozen=True, slots=True)
class OrientationRequest:
    capability: str
    context: dict[str, object] = field(default_factory=dict)
    execution_outcome: ExecutionOutcome | None = None
    source_facts: tuple[OrientationFact, ...] = ()
    routing_decision: RoutingDecision | None = None
    capability_snapshot: Mapping[str, object] | None = None


@dataclass(frozen=True, slots=True)
class Orientation:
    diagnosis: str
    rationale: str
    evidence_refs: tuple[str, ...]
    next_step: str
    blocker: str | None
    source_facts: tuple[OrientationFact, ...]
    confidence: OrientationConfidence


class OrchestrationOrientationBuilder:
    """Compose orientation from already-produced canonical states.

    The builder performs no I/O and never calls Registry, Router, Forge,
    authorization, execution, learning, promotion, or Evolution Gate.
    """

    def build(self, request: OrientationRequest) -> Orientation:
        self._validate_request(request)
        facts = tuple(request.source_facts)
        evidence_refs = self._collect_evidence_refs(facts)
        consistency = self._assess_consistency(request, facts)
        confidence = self._determine_confidence(
            request, facts, evidence_refs, consistency
        )
        diagnosis = self._build_diagnosis(
            request, facts, evidence_refs, consistency, confidence
        )
        rationale = self._build_rationale(
            request, facts, evidence_refs, consistency, confidence
        )
        blocker = self._build_blocker(request, consistency)
        next_step = self._build_next_step(confidence, blocker, consistency)
        return Orientation(
            diagnosis=diagnosis,
            rationale=rationale,
            evidence_refs=evidence_refs,
            next_step=next_step,
            blocker=blocker,
            source_facts=facts,
            confidence=confidence,
        )

    @staticmethod
    def _validate_request(request: OrientationRequest) -> None:
        if not isinstance(request, OrientationRequest):
            raise ValueError(
                "OrientationRequest required; got "
                f"{type(request).__name__}"
            )
        if not isinstance(request.capability, str) or not request.capability.strip():
            raise ValueError("capability must be a non-empty str")
        if not isinstance(request.context, dict):
            raise ValueError("context must be a dict")
        if not isinstance(request.source_facts, tuple):
            raise ValueError("source_facts must be a tuple")
        for fact in request.source_facts:
            if not isinstance(fact, (Evidence, ContextEvidence)):
                raise ValueError(
                    "source_facts may only contain Evidence or ContextEvidence"
                )
        if request.routing_decision is not None and not isinstance(
            request.routing_decision, RoutingDecision
        ):
            raise ValueError("routing_decision must be RoutingDecision or None")
        if request.execution_outcome is not None and not isinstance(
            request.execution_outcome, ExecutionOutcome
        ):
            raise ValueError("execution_outcome must be ExecutionOutcome or None")
        if request.capability_snapshot is not None and not isinstance(
            request.capability_snapshot, Mapping
        ):
            raise ValueError("capability_snapshot must be Mapping or None")

    @staticmethod
    def _collect_evidence_refs(
        facts: tuple[OrientationFact, ...],
    ) -> tuple[str, ...]:
        refs: list[str] = []
        for fact in facts:
            if isinstance(fact, Evidence):
                ref = fact.evidence_id
            else:
                ref = fact.source_id
            if isinstance(ref, str) and ref:
                refs.append(ref)
        return tuple(dict.fromkeys(refs))

    @classmethod
    def _assess_consistency(
        cls,
        request: OrientationRequest,
        facts: tuple[OrientationFact, ...],
    ) -> tuple[str, ...]:
        """Return only contradictions observable from supplied states.

        Fact-level semantic contradiction is deliberately not inferred:
        the canonical Evidence/ContextEvidence contracts do not define a
        contradiction relation. Only explicit control-state mismatches are
        treated as conflicts.
        """
        conflicts: list[str] = []

        claims_by_source: dict[str, set[str]] = {}
        for fact in facts:
            source_id, claim = cls._fact_identity(fact)
            claims_by_source.setdefault(source_id, set()).add(claim)

        for source_id, claims in claims_by_source.items():
            if len(claims) > 1:
                conflicts.append(
                    f"conflicting factual claims for source_id={source_id}"
                )

        route = request.routing_decision
        if route is not None and route.capability != request.capability:
            conflicts.append(
                "routing_decision capability does not match requested capability"
            )

        outcome = request.execution_outcome
        if outcome is not None and outcome.executed and outcome.status.value != "EXECUTED":
            conflicts.append(
                "execution_outcome marks executed=True with non-EXECUTED status"
            )

        return tuple(conflicts)

    @staticmethod
    def _all_have_provenance(facts: tuple[OrientationFact, ...]) -> bool:
        return bool(facts) and all(bool(getattr(fact, "provenance", None)) for fact in facts)

    @classmethod
    def _determine_confidence(
        cls,
        request: OrientationRequest,
        facts: tuple[OrientationFact, ...],
        evidence_refs: tuple[str, ...],
        conflicts: tuple[str, ...],
    ) -> OrientationConfidence:
        if not facts and request.execution_outcome is None:
            return OrientationConfidence.INSUFFICIENT
        if conflicts:
            return OrientationConfidence.PARTIAL
        if not evidence_refs:
            return OrientationConfidence.INSUFFICIENT
        if not cls._all_have_provenance(facts):
            return OrientationConfidence.PARTIAL
        if request.execution_outcome is None:
            return OrientationConfidence.PARTIAL
        return OrientationConfidence.ALIGNED

    @staticmethod
    def _build_diagnosis(
        request: OrientationRequest,
        facts: tuple[OrientationFact, ...],
        evidence_refs: tuple[str, ...],
        conflicts: tuple[str, ...],
        confidence: OrientationConfidence,
    ) -> str:
        if conflicts:
            return (
                f"Orientação de '{request.capability}' está parcialmente sustentada; "
                f"foram observadas {len(conflicts)} inconsistência(s) nos estados recebidos "
                f"({', '.join(evidence_refs) if evidence_refs else 'sem refs'})."
            )
        outcome = request.execution_outcome
        if outcome is not None and outcome.status.value == "BLOCKED":
            return (
                f"Execução de '{request.capability}' está bloqueada; "
                f"razão observada: {outcome.reason}."
            )
        if outcome is not None and outcome.executed:
            return (
                f"Execução de '{request.capability}' foi observada como concluída; "
                f"a orientação usa {len(evidence_refs)} referência(s) factual(is) "
                "rastreável(is)."
            )
        if facts:
            return (
                f"Orientação de '{request.capability}' possui {len(evidence_refs)} "
                f"referência(s) rastreável(is), mas o estado é {confidence.value.upper()}."
            )
        return (
            f"Orientação de '{request.capability}' é insuficiente porque "
            "não há fatos rastreáveis nem resultado de execução."
        )

    @staticmethod
    def _build_rationale(
        request: OrientationRequest,
        facts: tuple[OrientationFact, ...],
        evidence_refs: tuple[str, ...],
        conflicts: tuple[str, ...],
        confidence: OrientationConfidence,
    ) -> str:
        basis: list[str] = []
        if evidence_refs:
            basis.append(f"fatos rastreados por {len(evidence_refs)} referência(s)")
        if request.routing_decision is not None:
            basis.append(
                f"rota já produzida para capability={request.routing_decision.capability}"
            )
        if request.capability_snapshot is not None:
            basis.append("snapshot de capability previamente produzido")
        if request.execution_outcome is not None:
            basis.append(
                f"resultado de execução com status={request.execution_outcome.status.value}"
            )
        if not basis:
            basis.append("nenhuma fonte factual ou execução disponível")
        if conflicts:
            basis.append(f"{len(conflicts)} inconsistência(s) observável(is)")
        if not facts:
            basis.append("sem source_facts")
        basis.append(f"estado de confiança={confidence.value}")
        return "Orientação derivada de " + "; ".join(basis) + "."

    @staticmethod
    def _build_blocker(
        request: OrientationRequest,
        conflicts: tuple[str, ...],
    ) -> str | None:
        if conflicts:
            return "; ".join(conflicts)
        outcome = request.execution_outcome
        if outcome is not None and outcome.status.value == "BLOCKED":
            return outcome.reason or "execução bloqueada"
        if outcome is not None and not outcome.executed and outcome.reason:
            return outcome.reason
        return None

    @staticmethod
    def _build_next_step(
        confidence: OrientationConfidence,
        blocker: str | None,
        conflicts: tuple[str, ...],
    ) -> str:
        if blocker or conflicts:
            return (
                "Resolver os bloqueios ou conflitos observáveis e reavaliar "
                "a orientação pelo fluxo canônico responsável."
            )
        if confidence is OrientationConfidence.INSUFFICIENT:
            return (
                "Fornecer os dados essenciais ainda ausentes para permitir "
                "orientação rastreável."
            )
        if confidence is OrientationConfidence.PARTIAL:
            return (
                "Completar os dados essenciais e reavaliar; ALIGNED somente "
                "é permitido quando não houver inconsistência observável e "
                "as evidências necessárias forem rastreáveis e suficientes."
            )
        return (
            "Prosseguir pelo fluxo canônico que possui a autoridade "
            "correspondente ao próximo passo."
        )
