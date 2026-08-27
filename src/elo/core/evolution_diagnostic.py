"""Purpose-aligned self-diagnostic for ELO evolution.

This module compares verified ELO states without treating every technical
change as learning or as a change to canonical identity. It provides the
analyst, systems-architect and corporate-intelligence perspectives while
keeping Soul invariants outside ordinary evolution.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Iterable


class EvolutionImpact(StrEnum):
    IMPROVEMENT = "IMPROVEMENT"
    REGRESSION = "REGRESSION"
    NEUTRAL = "NEUTRAL"
    UNVERIFIED = "UNVERIFIED"


class EvolutionState(StrEnum):
    NO_MATERIAL_CHANGE = "NO_MATERIAL_CHANGE"
    EVOLUTION_CONSOLIDATED = "EVOLUTION_CONSOLIDATED"
    EVOLUTION_PARTIAL = "EVOLUTION_PARTIAL"
    EVOLUTION_REJECTED = "EVOLUTION_REJECTED"
    CANONICAL_CONFLICT = "CANONICAL_CONFLICT"


@dataclass(frozen=True)
class EvolutionSnapshot:
    """Verified state used for before/after comparison."""

    snapshot_id: str
    purpose: str
    capabilities: frozenset[str] = frozenset()
    removed_capabilities: frozenset[str] = frozenset()
    replaced_capabilities: frozenset[str] = frozenset()
    consolidated_components: frozenset[str] = frozenset()
    regressions: frozenset[str] = frozenset()
    architecture_components: frozenset[str] = frozenset()
    evidence_ids: tuple[str, ...] = ()
    verified: bool = True

    def __post_init__(self) -> None:
        if not self.snapshot_id.strip():
            raise ValueError("snapshot_id is required")
        if not self.purpose.strip():
            raise ValueError("purpose is required")


@dataclass(frozen=True)
class AcceptedEvolution:
    """A proposed change explicitly accepted by the ELO governance path."""

    change_id: str
    summary: str
    affected_layer: str
    purpose_alignment: bool
    canonical_safe: bool
    evidence_ids: tuple[str, ...] = ()
    accepted: bool = False

    def __post_init__(self) -> None:
        if not self.change_id.strip() or not self.summary.strip():
            raise ValueError("change identity and summary are required")
        if self.accepted and (not self.canonical_safe or not self.purpose_alignment):
            raise ValueError("an accepted evolution must be purpose-aligned and canonical-safe")


@dataclass(frozen=True)
class EvolutionDiagnostic:
    state: EvolutionState
    impact: EvolutionImpact
    acquired: tuple[str, ...]
    lost: tuple[str, ...]
    replaced: tuple[str, ...]
    consolidated: tuple[str, ...]
    regressions: tuple[str, ...]
    accepted_changes: tuple[str, ...]
    canonical_conflicts: tuple[str, ...]
    analyst_view: str
    architect_view: str
    intelligence_view: str
    corporate_view: str
    direction: str
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)


class EvolutionDiagnosticEngine:
    """Compare verified states and diagnose whether evolution serves the purpose."""

    def diagnose(
        self,
        previous: EvolutionSnapshot,
        current: EvolutionSnapshot,
        accepted_changes: Iterable[AcceptedEvolution] = (),
        canonical_conflicts: Iterable[str] = (),
    ) -> EvolutionDiagnostic:
        conflicts = tuple(sorted(set(canonical_conflicts)))
        accepted = tuple(change for change in accepted_changes if change.accepted)
        unsafe_accepted = tuple(
            change.change_id
            for change in accepted
            if not change.canonical_safe or not change.purpose_alignment
        )
        conflicts = tuple(sorted(set(conflicts).union(unsafe_accepted)))

        acquired = tuple(sorted(current.capabilities - previous.capabilities))
        lost = tuple(sorted(current.removed_capabilities | (previous.capabilities - current.capabilities)))
        replaced = tuple(sorted(current.replaced_capabilities))
        consolidated = tuple(sorted(current.consolidated_components))
        regressions = tuple(sorted(current.regressions))

        evidence = tuple(
            dict.fromkeys(
                previous.evidence_ids
                + current.evidence_ids
                + tuple(evidence_id for change in accepted for evidence_id in change.evidence_ids)
            )
        )

        if conflicts:
            state = EvolutionState.CANONICAL_CONFLICT
            impact = EvolutionImpact.REGRESSION
            direction = "BLOCK canonical mutation; reformulate or escalate the conflicting evolution."
        elif previous.purpose != current.purpose:
            state = EvolutionState.CANONICAL_CONFLICT
            impact = EvolutionImpact.REGRESSION
            direction = "Preserve the established purpose and require explicit architectural governance for any purpose change."
        elif regressions:
            state = EvolutionState.EVOLUTION_PARTIAL
            impact = EvolutionImpact.REGRESSION
            direction = "Correct regressions before acquiring additional capabilities."
        elif acquired or replaced or consolidated:
            state = EvolutionState.EVOLUTION_CONSOLIDATED if current.verified and evidence else EvolutionState.EVOLUTION_PARTIAL
            impact = EvolutionImpact.IMPROVEMENT if state == EvolutionState.EVOLUTION_CONSOLIDATED else EvolutionImpact.UNVERIFIED
            direction = (
                "Consolidate the verified improvement and establish the new baseline."
                if state == EvolutionState.EVOLUTION_CONSOLIDATED
                else "Validate the observed change before declaring a new evolutionary state."
            )
        else:
            state = EvolutionState.NO_MATERIAL_CHANGE
            impact = EvolutionImpact.NEUTRAL
            direction = "Continue observation; do not manufacture an evolution event without material evidence."

        accepted_names = tuple(change.summary for change in accepted)
        analyst_view = self._analyst_view(acquired, lost, replaced, regressions)
        architect_view = self._architect_view(current, previous, consolidated, conflicts)
        intelligence_view = self._intelligence_view(acquired, regressions, current.purpose)
        corporate_view = self._corporate_view(state, current.purpose)

        return EvolutionDiagnostic(
            state=state,
            impact=impact,
            acquired=acquired,
            lost=lost,
            replaced=replaced,
            consolidated=consolidated,
            regressions=regressions,
            accepted_changes=accepted_names,
            canonical_conflicts=conflicts,
            analyst_view=analyst_view,
            architect_view=architect_view,
            intelligence_view=intelligence_view,
            corporate_view=corporate_view,
            direction=direction,
            evidence_ids=evidence,
        )

    @staticmethod
    def _analyst_view(acquired: tuple[str, ...], lost: tuple[str, ...], replaced: tuple[str, ...], regressions: tuple[str, ...]) -> str:
        return (
            f"Capabilities acquired: {len(acquired)}; lost/changed: {len(lost)}; "
            f"replaced: {len(replaced)}; regressions: {len(regressions)}."
        )

    @staticmethod
    def _architect_view(
        current: EvolutionSnapshot,
        previous: EvolutionSnapshot,
        consolidated: tuple[str, ...],
        conflicts: tuple[str, ...],
    ) -> str:
        added_components = current.architecture_components - previous.architecture_components
        removed_components = previous.architecture_components - current.architecture_components
        if conflicts:
            return "Canonical boundary conflict detected; architectural change must not be promoted."
        return (
            f"Architecture delta: +{len(added_components)} / -{len(removed_components)} components; "
            f"consolidated components: {len(consolidated)}."
        )

    @staticmethod
    def _intelligence_view(acquired: tuple[str, ...], regressions: tuple[str, ...], purpose: str) -> str:
        return (
            f"The observed capability change is evaluated against the purpose '{purpose}'. "
            f"Net acquired capabilities: {len(acquired)}; regressions requiring attention: {len(regressions)}."
        )

    @staticmethod
    def _corporate_view(state: EvolutionState, purpose: str) -> str:
        if state == EvolutionState.EVOLUTION_CONSOLIDATED:
            return f"Evolution is aligned with the stated corporate purpose: {purpose}."
        if state == EvolutionState.CANONICAL_CONFLICT:
            return "Evolution is not eligible for promotion because it conflicts with the canonical boundary or purpose."
        return f"Corporate value remains measured by improved fulfillment of the purpose: {purpose}."


def render_elo_here(diagnostic: EvolutionDiagnostic, *, category: str = "Consolidação sem novos aprendizados verificáveis") -> str:
    """Render a human-readable ELO self-report without promoting learning."""
    lines = [
        "ELO AQUI — DIAGNÓSTICO DE EVOLUÇÃO",
        "",
        f"Estado: {diagnostic.state}",
        f"Impacto: {diagnostic.impact}",
        f"Categoria de apresentação: {category}",
        "",
        f"Aquisições: {', '.join(diagnostic.acquired) or 'nenhuma'}",
        f"Perdas: {', '.join(diagnostic.lost) or 'nenhuma'}",
        f"Substituições: {', '.join(diagnostic.replaced) or 'nenhuma'}",
        f"Consolidações: {', '.join(diagnostic.consolidated) or 'nenhuma'}",
        f"Regressões: {', '.join(diagnostic.regressions) or 'nenhuma'}",
        "",
        f"Perspectiva de analista: {diagnostic.analyst_view}",
        f"Perspectiva de arquiteto: {diagnostic.architect_view}",
        f"Perspectiva de inteligência corporativa: {diagnostic.intelligence_view}",
        f"Perspectiva corporativa: {diagnostic.corporate_view}",
        "",
        f"Direcionamento: {diagnostic.direction}",
        f"Evidências: {', '.join(diagnostic.evidence_ids) or 'não informadas'}",
        "",
        "Este diagnóstico descreve evolução observada; não altera a Soul nem promove aprendizado por si só.",
    ]
    return "\n".join(lines)
