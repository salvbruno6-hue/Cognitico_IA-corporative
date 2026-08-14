"""Scenario-based diagnostic engine for ELO.

The engine compares the same operational situation through different diagnostic
lenses. It deliberately separates observed evidence from hypotheses and avoids
claiming causality when the available evidence is insufficient.
"""

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping

from .production_flow import ProductionEvent, ProductionFlow, ProductionStage


class DiagnosticLens(StrEnum):
    FLOW = "FLOW"
    MATERIAL = "MATERIAL"
    CAPACITY = "CAPACITY"
    QUALITY = "QUALITY"
    DEADLINE = "DEADLINE"
    SYSTEMIC = "SYSTEMIC"


class DiagnosticStatus(StrEnum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    INSUFFICIENT = "INSUFFICIENT"


@dataclass(frozen=True)
class DiagnosticFinding:
    lens: DiagnosticLens
    status: DiagnosticStatus
    observations: tuple[str, ...] = ()
    hypotheses: tuple[str, ...] = ()
    impacts: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
    confidence: float = 0.0


@dataclass(frozen=True)
class DiagnosticScenario:
    scenario_id: str
    question: str
    flow: ProductionFlow
    context: Mapping[str, str] = None


class DiagnosticEngine:
    """Evaluate a production scenario through independent and systemic lenses."""

    def diagnose(self, scenario: DiagnosticScenario) -> tuple[DiagnosticFinding, ...]:
        return tuple(self._evaluate(lens, scenario) for lens in DiagnosticLens)

    def _evaluate(self, lens: DiagnosticLens, scenario: DiagnosticScenario) -> DiagnosticFinding:
        events = scenario.flow.events
        deviations = scenario.flow.deviations()

        if lens == DiagnosticLens.FLOW:
            if not scenario.flow.lifecycle_complete():
                return DiagnosticFinding(
                    lens, DiagnosticStatus.PARTIAL,
                    observations=("O ciclo produtivo não possui todas as etapas mínimas observáveis.",),
                    missing_evidence=("demanda, planejamento, execução ou resultado",),
                    confidence=0.8,
                )
            return DiagnosticFinding(
                lens, DiagnosticStatus.SUPPORTED,
                observations=("O ciclo possui demanda, planejamento, execução e resultado observáveis.",),
                confidence=0.9,
            )

        if lens == DiagnosticLens.MATERIAL:
            material_events = tuple(e for e in events if e.stage == ProductionStage.MATERIAL)
            shortages = tuple(e for e in material_events if (e.status or "").upper() in {"SHORTAGE", "BLOCKED", "UNAVAILABLE"})
            if shortages:
                return DiagnosticFinding(
                    lens, DiagnosticStatus.SUPPORTED,
                    observations=(f"Há {len(shortages)} evento(s) de material com indisponibilidade ou bloqueio.",),
                    hypotheses=("A indisponibilidade pode contribuir para atraso ou parada.",),
                    impacts=("risco de atraso da ordem", "pressão sobre compras/estoque"),
                    confidence=0.85,
                )
            if not material_events:
                return DiagnosticFinding(lens, DiagnosticStatus.INSUFFICIENT, missing_evidence=("eventos de materiais",), confidence=0.35)
            return DiagnosticFinding(lens, DiagnosticStatus.PARTIAL, observations=("Há eventos de materiais, mas não há evidência de indisponibilidade.",), confidence=0.65)

        if lens == DiagnosticLens.CAPACITY:
            capacity_events = tuple(e for e in events if e.stage == ProductionStage.CAPACITY)
            blocked = tuple(e for e in capacity_events if (e.status or "").upper() in {"BLOCKED", "OVERLOAD", "UNAVAILABLE"})
            if blocked:
                return DiagnosticFinding(
                    lens, DiagnosticStatus.SUPPORTED,
                    observations=(f"Há {len(blocked)} evento(s) de restrição de capacidade.",),
                    hypotheses=("A restrição pode deslocar a programação e aumentar o lead time.",),
                    impacts=("risco de fila", "risco de reprogramação"),
                    confidence=0.85,
                )
            if not capacity_events:
                return DiagnosticFinding(lens, DiagnosticStatus.INSUFFICIENT, missing_evidence=("capacidade disponível e carga planejada",), confidence=0.3)
            return DiagnosticFinding(lens, DiagnosticStatus.PARTIAL, observations=("Há registro de capacidade, sem restrição explícita.",), confidence=0.65)

        if lens == DiagnosticLens.QUALITY:
            quality_events = tuple(e for e in events if e.stage == ProductionStage.QUALITY)
            failures = tuple(e for e in quality_events if (e.status or "").upper() in {"FAIL", "REWORK", "QUARANTINE"} or e.deviation)
            if failures:
                return DiagnosticFinding(
                    lens, DiagnosticStatus.SUPPORTED,
                    observations=(f"Há {len(failures)} evento(s) de qualidade, retrabalho ou quarentena.",),
                    hypotheses=("O desvio de qualidade pode gerar retrabalho e alterar a disponibilidade para expedição.",),
                    impacts=("retrabalho", "atraso potencial", "redução de disponibilidade"),
                    confidence=0.85,
                )
            if not quality_events:
                return DiagnosticFinding(lens, DiagnosticStatus.INSUFFICIENT, missing_evidence=("inspeções e resultado de qualidade",), confidence=0.3)
            return DiagnosticFinding(lens, DiagnosticStatus.PARTIAL, observations=("Há controle de qualidade sem falha explícita.",), confidence=0.65)

        if lens == DiagnosticLens.DEADLINE:
            deadline_events = tuple(e for e in events if (e.metadata.get("deadline_status", "").upper() in {"LATE", "AT_RISK"}))
            if deadline_events:
                return DiagnosticFinding(
                    lens, DiagnosticStatus.SUPPORTED,
                    observations=(f"Há {len(deadline_events)} evento(s) com risco ou atraso de prazo.",),
                    impacts=("risco de atraso ao cliente",),
                    confidence=0.9,
                )
            return DiagnosticFinding(lens, DiagnosticStatus.INSUFFICIENT, missing_evidence=("prazo prometido versus prazo realizado",), confidence=0.35)

        # SYSTEMIC
        evidence_count = sum(1 for finding in self._evaluate_independent(scenario) if finding.status == DiagnosticStatus.SUPPORTED)
        if not deviations and evidence_count < 2:
            return DiagnosticFinding(
                lens, DiagnosticStatus.INSUFFICIENT,
                observations=("Não há evidência suficiente para atribuir uma causa sistêmica.",),
                hypotheses=("É necessário cruzar mais de uma dimensão operacional.",),
                missing_evidence=("relações temporais entre materiais, capacidade, qualidade e prazo",),
                confidence=0.25,
            )
        hypotheses = []
        impacts = []
        if deviations:
            hypotheses.append("Os desvios registrados devem ser correlacionados antes de definir uma causa raiz.")
            impacts.append("potencial efeito cascata sobre prazo e capacidade")
        if evidence_count >= 2:
            hypotheses.append("Há sinais em mais de uma dimensão e o cenário merece análise sistêmica.")
            impacts.append("risco de decisão local mascarar impacto em outros processos")
        return DiagnosticFinding(
            lens, DiagnosticStatus.PARTIAL,
            observations=(f"Foram encontradas evidências suportadas em {evidence_count} dimensão(ões).",),
            hypotheses=tuple(hypotheses), impacts=tuple(impacts),
            missing_evidence=("causalidade confirmada",), confidence=0.7,
        )

    def _evaluate_independent(self, scenario: DiagnosticScenario) -> tuple[DiagnosticFinding, ...]:
        return tuple(self._evaluate(lens, scenario) for lens in DiagnosticLens if lens != DiagnosticLens.SYSTEMIC)
