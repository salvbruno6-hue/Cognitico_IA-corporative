from elo.cognitive.routing.model_selection import ModelCandidate, ModelSelector
from elo.cognitive.routing.tool_selection import ToolCandidate, ToolSelector


def test_model_selector_prefers_evidence_and_quality():
    candidates = [
        ModelCandidate("fast", frozenset({"reasoning"}), quality=0.6, evidence=0.4, latency_ms=50),
        ModelCandidate("trusted", frozenset({"reasoning"}), quality=0.9, evidence=0.95, latency_ms=500),
    ]
    assert ModelSelector().select("reasoning", candidates).model_id == "trusted"


def test_tool_selector_rejects_unsupported_capability():
    try:
        ToolSelector().select("calculation", [ToolCandidate("search", frozenset({"retrieval"}))])
    except LookupError as exc:
        assert "calculation" in str(exc)
    else:
        raise AssertionError("unsupported capability must fail")
