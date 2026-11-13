from src.elo.agent_intake.hermes_capability_loops import CapabilityState
from src.elo.agent_intake.native_capabilities import CAPABILITY_IDS
from src.elo.agent_intake.capability_promotion import (
    PromotionState,
    activate_operational_capabilities,
    evaluate_all_candidates,
)
from src.elo.core.capability_registry import CapabilityRegistry, CapabilityStatus


def test_eight_candidates_promote_to_success():
    decisions = evaluate_all_candidates()
    assert tuple(d.capability_id for d in decisions) == CAPABILITY_IDS
    assert all(d.state is PromotionState.SUCCESS for d in decisions)
    assert all(d.operationally_active for d in decisions)
    assert all(not d.canonical_eligible for d in decisions)


def test_success_is_the_active_operational_state():
    assert PromotionState.ACTIVE_OPERATIONAL is PromotionState.SUCCESS
    assert PromotionState.SUCCESS.value == "success"


def test_eight_mechanisms_are_effectively_active_in_existing_elo_registry():
    registry = activate_operational_capabilities(CapabilityRegistry())
    snapshots = registry.snapshot()
    assert tuple(item.name for item in snapshots) == CAPABILITY_IDS
    assert all(item.kind == "elo-native" for item in snapshots)
    assert all(item.status is CapabilityStatus.AVAILABLE for item in snapshots)
    assert all(item.metadata["promotion_state"] == "success" for item in snapshots)
    assert all(item.metadata["canonical_mutation"] == "false" for item in snapshots)


def test_core_canonization_requires_core_relevance_and_evolution_gate():
    from src.elo.agent_intake.native_capabilities import execute_candidate
    from src.elo.agent_intake.capability_promotion import evaluate_promotion

    evidence = execute_candidate("HERMES-SKILLS", request_id="CANON-TEST", tenant_scope="elo-lab")
    decision = evaluate_promotion(
        evidence,
        provenance_passed=True,
        governance_complete=True,
        core_pillar_relevance=True,
        evolution_gate_approved=True,
    )
    assert decision.state is PromotionState.CANONICAL
    assert decision.canonical_eligible


def test_core_canonization_stays_blocked_without_evolution_gate():
    from src.elo.agent_intake.native_capabilities import execute_candidate
    from src.elo.agent_intake.capability_promotion import evaluate_promotion

    evidence = execute_candidate("HERMES-SKILLS", request_id="CANON-BLOCK", tenant_scope="elo-lab")
    decision = evaluate_promotion(
        evidence,
        provenance_passed=True,
        governance_complete=True,
        core_pillar_relevance=True,
        evolution_gate_approved=False,
    )
    assert decision.state is PromotionState.SUCCESS
    assert not decision.canonical_eligible


def test_candidate_loop_state_model_still_starts_with_candidate():
    assert CapabilityState.CANDIDATE.value == "candidate"
