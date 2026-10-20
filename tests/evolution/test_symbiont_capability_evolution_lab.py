from elo.cognitive.symbiont_capability_evolution import Curvature, review_capabilities
from scripts.run_symbiont_capability_evolution_lab import run_lab


def test_capability_evolution_can_use_laboratory_downstream_experience():
    result = run_lab()

    assert result["mode"] == "LAB_ONLY"
    assert result["evidence_mode"] == "INDIRECT_EXPERIENCE"
    assert result["observer_capability"] == "ExecutionRouter"
    assert str(result["experience_ref"]).strip()
    assert result["status"] == "ANALYSIS_READY"
    assert result["curvature"] == "POSITIVE"
    assert result["canonical_mutation"] is False
    assert result["production_evidence"] is False
    assert result["promotion_authorized"] is False
