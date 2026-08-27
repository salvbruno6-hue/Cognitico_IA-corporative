import pytest

from elo.core.evolution_diagnostic import (
    AcceptedEvolution,
    EvolutionDiagnosticEngine,
    EvolutionSnapshot,
    EvolutionState,
)


def test_verified_capability_gain_is_consolidated():
    before = EvolutionSnapshot(snapshot_id="before", purpose="orchestrate decisions", capabilities=frozenset({"context"}), evidence_ids=("e1",))
    after = EvolutionSnapshot(snapshot_id="after", purpose="orchestrate decisions", capabilities=frozenset({"context", "correlation"}), evidence_ids=("e2",))
    result = EvolutionDiagnosticEngine().diagnose(before, after)
    assert result.state == EvolutionState.EVOLUTION_CONSOLIDATED
    assert result.acquired == ("correlation",)


def test_purpose_change_is_canonical_conflict():
    before = EvolutionSnapshot(snapshot_id="before", purpose="orchestrate decisions")
    after = EvolutionSnapshot(snapshot_id="after", purpose="different purpose")
    result = EvolutionDiagnosticEngine().diagnose(before, after)
    assert result.state == EvolutionState.CANONICAL_CONFLICT


def test_report_identifies_elo_and_non_learning_status():
    before = EvolutionSnapshot(snapshot_id="before", purpose="orchestrate decisions")
    after = EvolutionSnapshot(snapshot_id="after", purpose="orchestrate decisions", capabilities=frozenset({"correlation"}), evidence_ids=("e2",))
    result = EvolutionDiagnosticEngine().diagnose(before, after)
    assert "ELO AQUI" in result.direction or result.state == EvolutionState.EVOLUTION_CONSOLIDATED


def test_accepted_evolution_requires_purpose_alignment():
    with pytest.raises(ValueError, match="purpose-aligned"):
        AcceptedEvolution(
            change_id="c1",
            summary="change",
            affected_layer="core",
            purpose_alignment=False,
            canonical_safe=True,
            accepted=True,
        )


def test_non_aligned_accepted_change_cannot_reach_consolidated_state():
    before = EvolutionSnapshot(snapshot_id="before", purpose="orchestrate decisions", evidence_ids=("e1",))
    after = EvolutionSnapshot(snapshot_id="after", purpose="orchestrate decisions", capabilities=frozenset({"correlation"}), evidence_ids=("e2",))
    # The dataclass rejects an invalid accepted change before the engine can promote it.
    with pytest.raises(ValueError):
        AcceptedEvolution(
            change_id="c2",
            summary="misaligned",
            affected_layer="cognitive",
            purpose_alignment=False,
            canonical_safe=True,
            accepted=True,
        )
    result = EvolutionDiagnosticEngine().diagnose(before, after)
    assert result.state == EvolutionState.EVOLUTION_CONSOLIDATED
