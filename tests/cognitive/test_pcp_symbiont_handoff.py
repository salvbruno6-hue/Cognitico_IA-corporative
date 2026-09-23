from elo.cognitive.pcp_confrontation import confront
from elo.cognitive.pcp_operational_evidence import build_operational_evidence_package
from elo.cognitive.pcp_symbiont_handoff import prepare_pcp_symbiont_handoff


def test_handoff_translates_without_executing_symbiont():
    package = build_operational_evidence_package((
        confront(
            dimension="CAPACIDADE", key="C1",
            planned=100, actual=90, variance=-10,
            evidence_ids=("E1",),
        ),
    ), source_kind="SUPABASE", source_ref="pcp")
    handoff = prepare_pcp_symbiont_handoff(
        package,
        tenant_id="T1",
        decision_id="D1",
        observation_id="O1",
        source_commit="abc123",
    )
    observation = handoff.observation
    assert observation["domain"] == "PCP"
    assert observation["decision_id"] == "D1"
    assert observation["evidence_ids"] == ["E1"]
    assert observation["existing_owner"] == "SKILL_PLANEJAMENTO_MULTITEINER"
    assert observation["source_commit"] == "abc123"


def test_handoff_does_not_invent_learning_state():
    package = build_operational_evidence_package((
        confront(
            dimension="PRAZO", key="P1",
            planned="2026-09-10", actual="2026-09-12",
        ),
    ), source_kind="SUPABASE")
    observation = prepare_pcp_symbiont_handoff(
        package,
        tenant_id="T1",
        decision_id="D1",
        observation_id="O1",
    ).observation
    assert observation["hypothesis"] is None
    assert observation["experiment"] is None
    assert observation["regression_status"] is None
    assert observation["generalization_status"] is None
