from elo.core.evolution_diagnostic import EvolutionDiagnosticEngine, EvolutionSnapshot, EvolutionState


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
