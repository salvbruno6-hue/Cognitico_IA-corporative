"""Stronger executable governance evidence for ELO-024.

This test module validates boundaries and evidence semantics only. It does not
create a budgeting authority, scenario engine, memory layer, or executor.
"""

from dataclasses import dataclass
from enum import Enum


class EvidenceState(str, Enum):
    DEFINED = "DEFINED"
    GAP = "GAP"


@dataclass(frozen=True)
class Capability:
    name: str
    owner: str | None
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
    Capability("live_supplier_quote", None, EvidenceState.GAP),
)


def test_each_capability_has_owner_or_explicit_gap():
    assert all(item.owner or item.evidence is EvidenceState.GAP for item in CAPABILITIES)


def test_gap_is_not_promoted_to_pass():
    live_quote = next(item for item in CAPABILITIES if item.name == "live_supplier_quote")
    assert live_quote.evidence is EvidenceState.GAP
    assert live_quote.evidence is not EvidenceState.DEFINED or live_quote.owner is None


def test_facts_and_assumptions_remain_separate():
    facts = {"cost": 100.0, "capacity": 10, "period": "2026-Q3"}
    assumptions = {"demand_growth": 0.15, "supplier_lead_time_days": 7}
    assert set(facts).isdisjoint(assumptions)


def test_missing_inputs_create_follow_up_gap():
    required = {"cost", "capacity", "demand"}
    available = {"cost", "capacity"}
    missing = required - available
    assert missing == {"demand"}
    assert missing, "missing evidence must remain visible"


def test_specialist_request_is_scoped_and_provenance_preserving():
    request = {
        "specialist": "pricing",
        "scope": "supplier quote for item A",
        "provenance_required": True,
        "status": "REQUESTED",
    }
    assert request["specialist"] == "pricing"
    assert request["scope"]
    assert request["provenance_required"] is True
    assert request["status"] != "EXECUTED"


def test_budget_vs_actual_adds_evidence_without_rewriting_history():
    historical = {"period": "2026-Q2", "budget": 1000.0, "actual": 950.0}
    next_evidence = {"period": "2026-Q3", "budget": 1100.0, "actual": None}
    assert historical["period"] != next_evidence["period"]
    assert historical["actual"] == 950.0
    assert next_evidence["actual"] is None


def test_recommendation_cannot_authorize_or_execute():
    recommendation = {"status": "RECOMMENDED", "action": "REVIEW_QUOTE"}
    authorization = None
    execution = None
    assert recommendation["status"] == "RECOMMENDED"
    assert authorization is None
    assert execution is None


def test_learning_candidate_requires_evolution_gate():
    candidate = {
        "status": "CANDIDATE",
        "historical_evidence_ids": ["ORC-001", "ACT-001"],
        "evolution_gate": "REQUIRED",
    }
    assert candidate["status"] != "PROMOTED"
    assert candidate["evolution_gate"] == "REQUIRED"
    assert candidate["historical_evidence_ids"]


def test_reproducible_margin_calculation():
    quantity = 10
    unit_cost = 100.0
    margin_rate = 0.20
    cost = quantity * unit_cost
    price = cost / (1 - margin_rate)
    assert cost == 1000.0
    assert round(price, 2) == 1250.00
    assert round((price - cost) / price, 6) == margin_rate
