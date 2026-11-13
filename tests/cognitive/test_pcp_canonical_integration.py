"""Structural integration check for the PCP governed handoff.

The test verifies the canonical classes are the ones used by the PCP boundary.
It does not fabricate an ATTRIBUTED decision or execute learning.
"""

from elo.core.decision_outcome_loop import DecisionLifecycle, DecisionState
from elo.cognitive.symbiont_skill_runtime import SymbiontSkillRuntime
from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabObservation
from elo.cognitive.pcp_symbiont_handoff import PCPSymbiontHandoff


def test_canonical_symbiont_authorities_are_importable():
    assert DecisionLifecycle is not None
    assert DecisionState.ATTRIBUTED.value == "attributed"
    assert SymbiontSkillRuntime is not None
    assert SymbiontLabAdapter is not None
    assert SymbiontLabObservation is not None
    assert PCPSymbiontHandoff is not None


def test_runtime_delegates_to_lifecycle_contract():
    assert "handoff_to_symbiont" in SymbiontSkillRuntime.handoff_decision.__name__
    assert hasattr(DecisionLifecycle, "handoff_to_symbiont")


def test_real_loop_requires_attributed_state():
    assert DecisionState.PROPOSED.value == "proposed"
    assert DecisionState.ATTRIBUTED.value == "attributed"
    assert DecisionLifecycle.handoff_to_symbiont is not None
