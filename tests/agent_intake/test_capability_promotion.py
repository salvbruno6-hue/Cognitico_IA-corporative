from src.elo.agent_intake.hermes_capability_loops import CapabilityState
from src.elo.agent_intake.native_capabilities import CAPABILITY_IDS
from src.elo.agent_intake.capability_promotion import PromotionState, evaluate_all_candidates


def test_eight_candidates_have_native_operational_promotion_path():
    decisions = evaluate_all_candidates()
    assert tuple(d.capability_id for d in decisions) == CAPABILITY_IDS
    assert all(d.state is PromotionState.ACTIVE_OPERATIONAL for d in decisions)
    assert all(d.operationally_active for d in decisions)
    assert all(not d.canonical_eligible for d in decisions)


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
    assert decision.state is PromotionState.ACTIVE_OPERATIONAL
    assert not decision.canonical_eligible


def test_candidate_loop_state_model_still_starts_with_candidate():
    assert CapabilityState.CANDIDATE.value == "candidate"
