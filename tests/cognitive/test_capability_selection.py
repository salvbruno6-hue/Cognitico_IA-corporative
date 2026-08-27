from elo.core.capability_registry import CapabilityProbe, CapabilityRegistry
from elo.cognitive.reasoning.capability_selection import CapabilityRequirement, CapabilitySelector


def test_selector_chooses_capability_matching_required_function():
    registry = CapabilityRegistry((
        CapabilityProbe("LOCAL_AI", "model-a", health_check=lambda: True,
                         metadata={"capabilities": "reasoning,retrieval"}),
        CapabilityProbe("LOCAL_TOOL", "python", health_check=lambda: True,
                         metadata={"capabilities": "calculation"}),
    ))
    decision = CapabilitySelector(registry).select(
        CapabilityRequirement("calculation", preferred_kinds=("LOCAL_TOOL",))
    )
    assert decision.status == "SELECTED"
    assert decision.capability_name == "python"


def test_selector_does_not_use_unavailable_capability():
    registry = CapabilityRegistry((
        CapabilityProbe("REMOTE_AI", "model-a", health_check=lambda: False,
                         metadata={"capabilities": "reasoning"}),
    ))
    decision = CapabilitySelector(registry).select(CapabilityRequirement("reasoning"))
    assert decision.status == "NO_MATCH"


def test_selector_respects_minimum_score():
    registry = CapabilityRegistry((
        CapabilityProbe("LOCAL_AI", "model-a", health_check=lambda: True,
                         metadata={"capabilities": "reasoning"}),
    ))
    decision = CapabilitySelector(registry).select(
        CapabilityRequirement("reasoning", preferred_kinds=("REMOTE_AI",), min_score=0.9)
    )
    assert decision.status == "INSUFFICIENT"
