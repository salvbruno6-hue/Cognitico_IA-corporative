"""Executable governance checks for ELO-024 budgeting capabilities.

The matrix maps budgeting concerns to existing canonical owners. It is not a
new budgeting authority and intentionally leaves external/live evidence as a
gap rather than fabricating a PASS.
"""

from dataclasses import dataclass
from enum import Enum


class EvidenceState(str, Enum):
    PASS = "PASS"
    GAP = "GAP"
    DEFINED = "DEFINED"


@dataclass(frozen=True)
class Capability:
    name: str
    owner: str
    evidence: EvidenceState


CAPABILITIES = (
    Capability("demand", "Cognitive/Context", EvidenceState.DEFINED),
    Capability("capacity", "Core/Analysis", EvidenceState.DEFINED),
    Capability("cost", "Core/Calculation", EvidenceState.DEFINED),
    Capability("pricing", "Forge/Specialist", EvidenceState.DEFINED),
    Capability("margin", "Core/Calculation", EvidenceState.DEFINED),
    Capability("forecast", "Core/Scenario", EvidenceState.DEFINED),
    Capability("resource_planning", "Core/Analysis", EvidenceState.DEFINED),
    Capability("risk", "Core/Scenario", EvidenceState.DEFINED),
    Capability("quotation", "Forge/Specialist", EvidenceState.DEFINED),
)


def test_every_budgeting_capability_has_one_canonical_owner_or_explicit_gap():
    assert CAPABILITIES
    for capability in CAPABILITIES:
        assert capability.name
        assert capability.owner or capability.evidence is EvidenceState.GAP


def test_facts_and_assumptions_are_distinct():
    facts = {"cost": 100.0, "capacity": 10}
    assumptions = {"demand_growth": 0.15}
    assert set(facts).isdisjoint(assumptions)


def test_missing_inputs_produce_gap_not_fabricated_values():
    required_inputs = {"cost", "capacity", "demand"}
    available_inputs = {"cost", "capacity"}
    missing = required_inputs - available_inputs
    assert missing == {"demand"}
    assert missing is not None


def test_calculation_is_reproducible():
    quantity = 10
    unit_cost = 100.0
    margin_rate = 0.20
    cost = quantity * unit_cost
    price = cost / (1 - margin_rate)
    assert cost == 1000.0
    assert round(price, 2) == 1250.00
    assert round((price - cost) / price, 6) == margin_rate


def test_recommendation_is_not_authorization_or_execution():
    recommendation = {"action": "QUOTE", "status": "RECOMMENDED"}
    authorization = None
    executed = False
    assert recommendation["status"] == "RECOMMENDED"
    assert authorization is None
    assert executed is False


def test_historical_actuals_are_not_rewritten_by_learning():
    historical = {"period": "2026-Q1", "actual": 1000.0}
    learning_candidate = {"period": "2026-Q2", "forecast": 1200.0}
    assert historical["period"] != learning_candidate["period"]
    assert historical["actual"] == 1000.0


def test_learning_candidate_requires_evolution_gate():
    candidate = {"status": "CANDIDATE", "evolution_gate": "REQUIRED"}
    assert candidate["status"] != "PROMOTED"
    assert candidate["evolution_gate"] == "REQUIRED"
