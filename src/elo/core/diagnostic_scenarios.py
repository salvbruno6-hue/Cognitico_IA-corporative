"""Deterministic multi-scenario diagnostics for ELO.

This module does not replace reasoning or GPT. It creates controlled diagnostic
views over the same evidence so ELO can compare operational, causal,
risk, bottleneck and counterfactual perspectives without silently changing
facts between analyses.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class DiagnosticMode(StrEnum):
    BASELINE = "BASELINE"
    BOTTLENECK = "BOTTLENECK"
    CAUSAL = "CAUSAL"
    RISK = "RISK"
    COUNTERFACTUAL = "COUNTERFACTUAL"
    ADVERSARIAL = "ADVERSARIAL"


@dataclass(frozen=True)
class DiagnosticObservation:
    evidence_id: str
    dimension: str
    value: float
    statement: str
    confidence: float = 1.0
    metadata: Mapping[str, str] = ()


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


class DiagnosticScenarioEngine:
    """Run several bounded readings against identical evidence."""

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
