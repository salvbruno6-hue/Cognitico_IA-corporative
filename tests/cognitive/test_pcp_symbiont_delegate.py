from elo.cognitive.pcp_confrontation import confront
from elo.cognitive.pcp_operational_evidence import build_operational_evidence_package
from elo.cognitive.pcp_symbiont_delegate import delegate_pcp_observation
from elo.cognitive.pcp_symbiont_handoff import prepare_pcp_symbiont_handoff


def test_delegate_uses_injected_canonical_authority():
    package = build_operational_evidence_package((
        confront(
            dimension="CAPACIDADE", key="C1",
            planned=100, actual=90, variance=-10,
            evidence_ids=("E1",),
        ),
    ), source_kind="SUPABASE")
    handoff = prepare_pcp_symbiont_handoff(
        package, tenant_id="T1", decision_id="D1", observation_id="O1",
    )
    calls = []

    def canonical(observation):
        calls.append(observation)
        return {"canonical": True}

    result = delegate_pcp_observation(handoff, canonical_handoff=canonical)
    assert result.status == "DELEGATED"
    assert result.delegated is True
    assert result.response == {"canonical": True}
    assert len(calls) == 1


def test_delegate_does_not_create_learning_result():
    package = build_operational_evidence_package((
        confront(
            dimension="PRAZO", key="P1",
            planned="2026-09-10", actual="2026-09-12",
        ),
    ), source_kind="SUPABASE")
    handoff = prepare_pcp_symbiont_handoff(
        package, tenant_id="T1", decision_id="D1", observation_id="O1",
    )
    result = delegate_pcp_observation(
        handoff, canonical_handoff=lambda _: {"accepted": True},
    )
    assert result.response == {"accepted": True}
