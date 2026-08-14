"""Governed multi-scenario diagnostics for the ELO Core Loop.

This module preserves the existing deterministic diagnostic modes while adding
an explicit multi-lens decision gate. The same evidence can be read through
operational, causal, temporal, capacity, risk and evidence-quality lenses
without silently changing facts or exposing private chain-of-thought.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class DiagnosticMode(StrEnum):
    BASELINE = "BASELINE"
    BOTTLENECK = "BOTTLENECK"
    CAUSAL = "CAUSAL"
    RISK = "RISK"
    COUNTERFACTUAL = "COUNTERFACTUAL"
    ADVERSARIAL = "ADVERSARIAL"


class DiagnosticLens(StrEnum):
    OPERATIONAL = "OPERATIONAL"
    CAUSAL = "CAUSAL"
    TEMPORAL = "TEMPORAL"
    CAPACITY = "CAPACITY"
    RISK = "RISK"
    EVIDENCE = "EVIDENCE"


class DiagnosticStatus(StrEnum):
    SUPPORTED = "SUPPORTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    CONFLICTING = "CONFLICTING"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class DiagnosticObservation:
    evidence_id: str
    dimension: str
    value: float
    statement: str
    confidence: float = 1.0
    metadata: Mapping[str, str] = ()
    lens: DiagnosticLens | None = None
    status: DiagnosticStatus = DiagnosticStatus.SUPPORTED
    impact: str | None = None
    recommendation: str | None = None

    @property
    def evidence_ids(self) -> tuple[str, ...]:
        return (self.evidence_id,)

    @property
    def finding(self) -> str:
        return self.statement


@dataclass(frozen=True)
class DiagnosticFinding:
    mode: DiagnosticMode
    severity: str
    statement: str
    evidence_ids: tuple[str, ...]
    confidence: float


@dataclass(frozen=True)
class DiagnosticReport:
    scenario_id: str
    findings: tuple[DiagnosticFinding, ...]
    uncertainties: tuple[str, ...] = ()

    def by_mode(self, mode: DiagnosticMode) -> tuple[DiagnosticFinding, ...]:
        return tuple(item for item in self.findings if item.mode == mode)

    def modes_with_findings(self) -> tuple[DiagnosticMode, ...]:
        return tuple(dict.fromkeys(item.mode for item in self.findings))


@dataclass(frozen=True)
class DiagnosticScenario:
    scenario_id: str
    question: str
    entity: str | None = None
    scope: str | None = None
    observations: tuple[DiagnosticObservation, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def by_lens(self, lens: DiagnosticLens) -> tuple[DiagnosticObservation, ...]:
        return tuple(item for item in self.observations if item.lens == lens)

    def has_conflict(self) -> bool:
        return any(item.status == DiagnosticStatus.CONFLICTING for item in self.observations)

    def is_blocked(self) -> bool:
        return any(item.status == DiagnosticStatus.BLOCKED for item in self.observations)

    def evidence_quality(self) -> float:
        evidence = self.by_lens(DiagnosticLens.EVIDENCE)
        if not evidence:
            return 0.0
        return sum(item.confidence for item in evidence) / len(evidence)

    def decision_ready(self, minimum_confidence: float = 0.7) -> bool:
        if self.is_blocked() or self.has_conflict():
            return False
        required = {DiagnosticLens.OPERATIONAL, DiagnosticLens.CAUSAL, DiagnosticLens.EVIDENCE}
        present = {item.lens for item in self.observations}
        return required.issubset(present) and self.evidence_quality() >= minimum_confidence

    def human_summary(self) -> str:
        if self.is_blocked():
            return "Eu não considero este cenário pronto para decisão porque há um bloqueio de evidência ou governança."
        if self.has_conflict():
            return "Eu encontrei leituras conflitantes entre as evidências e não considero seguro consolidar uma decisão ainda."
        if self.decision_ready():
            return "Eu considero o cenário suficientemente sustentado para uma decisão, com base nas evidências operacionais, causais e de qualidade disponíveis."
        return "Eu encontrei sinais relevantes, mas ainda não tenho evidência suficiente para tratar a conclusão como decisão madura."


class DiagnosticScenarioEngine:
    """Run bounded diagnostic modes and governed multi-lens scenarios."""

    LENSES = tuple(DiagnosticLens)

    def diagnose(
        self,
        scenario_id: str,
        observations: tuple[DiagnosticObservation, ...],
        *,
        modes: tuple[DiagnosticMode, ...] = tuple(DiagnosticMode),
    ) -> DiagnosticReport:
        if not scenario_id.strip():
            raise ValueError("scenario_id is required")
        if not observations:
            return DiagnosticReport(scenario_id, (), ("no evidence supplied",))

        findings: list[DiagnosticFinding] = []
        for mode in modes:
            findings.extend(self._run_mode(mode, observations))
        return DiagnosticReport(
            scenario_id=scenario_id,
            findings=tuple(findings),
            uncertainties=self._uncertainties(observations),
        )

    def create(
        self,
        scenario_id: str,
        question: str,
        *,
        entity: str | None = None,
        scope: str | None = None,
    ) -> DiagnosticScenario:
        if not scenario_id.strip():
            raise ValueError("scenario_id is required")
        if not question.strip():
            raise ValueError("question is required")
        return DiagnosticScenario(
            scenario_id=scenario_id,
            question=question,
            entity=entity,
            scope=scope,
        )

    @classmethod
    def required_lenses(cls) -> tuple[DiagnosticLens, ...]:
        return cls.LENSES

    def _run_mode(
        self,
        mode: DiagnosticMode,
        observations: tuple[DiagnosticObservation, ...],
    ) -> tuple[DiagnosticFinding, ...]:
        if mode == DiagnosticMode.BASELINE:
            return tuple(
                DiagnosticFinding(mode, "INFO", item.statement, (item.evidence_id,), item.confidence)
                for item in observations
            )

        if mode == DiagnosticMode.BOTTLENECK:
            return self._threshold_findings(mode, observations, 0.8, "possível gargalo")

        if mode == DiagnosticMode.RISK:
            return self._threshold_findings(mode, observations, 0.7, "risco operacional relevante")

        if mode == DiagnosticMode.CAUSAL:
            return self._causal_findings(observations)

        if mode == DiagnosticMode.COUNTERFACTUAL:
            return self._threshold_findings(mode, observations, 0.5, "cenário sensível: alteração da condição pode mudar o resultado")

        return self._threshold_findings(mode, observations, 0.9, "hipótese que exige contestação")

    @staticmethod
    def _threshold_findings(
        mode: DiagnosticMode,
        observations: tuple[DiagnosticObservation, ...],
        threshold: float,
        prefix: str,
    ) -> tuple[DiagnosticFinding, ...]:
        return tuple(
            DiagnosticFinding(
                mode,
                "HIGH" if item.value >= 0.9 else "MEDIUM",
                f"{prefix}: {item.statement}",
                (item.evidence_id,),
                item.confidence,
            )
            for item in observations
            if item.value >= threshold
        )

    @staticmethod
    def _causal_findings(
        observations: tuple[DiagnosticObservation, ...],
    ) -> tuple[DiagnosticFinding, ...]:
        by_dimension: dict[str, list[DiagnosticObservation]] = {}
        for item in observations:
            by_dimension.setdefault(item.dimension, []).append(item)
        findings: list[DiagnosticFinding] = []
        for dimension, items in by_dimension.items():
            if len(items) >= 2 and any(item.value >= 0.8 for item in items):
                findings.append(
                    DiagnosticFinding(
                        DiagnosticMode.CAUSAL,
                        "INVESTIGATE",
                        f"múltiplas evidências no domínio {dimension} justificam investigação causal; não tratar correlação como causa comprovada",
                        tuple(item.evidence_id for item in items),
                        min(item.confidence for item in items),
                    )
                )
        return tuple(findings)

    @staticmethod
    def _uncertainties(observations: tuple[DiagnosticObservation, ...]) -> tuple[str, ...]:
        return tuple(
            f"{item.evidence_id}: confiança abaixo de 0.6"
            for item in observations
            if item.confidence < 0.6
        )
