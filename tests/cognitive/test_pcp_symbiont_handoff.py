from elo.cognitive.pcp_confrontation import confront
from elo.cognitive.pcp_operational_evidence import build_operational_evidence_package
from elo.cognitive.pcp_symbiont_handoff import prepare_pcp_symbiont_handoff


def make_handoff():
    package = build_operational_evidence_package((
        confront(
            dimension="CAPACIDADE", key="C1",
            planned=100, actual=90, variance=-10,
            evidence_ids=("E1",),
        ),
    ), source_kind="SUPABASE", source_ref="pcp")
    return prepare_pcp_symbiont_handoff(
        package,
        tenant_id="T1",
        decision_id="D1",
        observation_id="O1",
        source_ref="pcp",
        source_commit="abc123",
        hypothesis="verificar desvio de capacidade",
        baseline="capacidade planejada registrada",
        experiment="confrontação controlada",
        result="desvio observado",
        regression_status="OK",
        generalization_status="PARTIAL",
        risk="LOW",
    )


def test_handoff_returns_canonical_observation():
    observation = make_handoff().observation
    assert observation.domain == "PCP"
    assert observation.decision_id == "D1"
    assert observation.evidence_ids == ("E1",)
    assert observation.existing_owner == "SKILL_PLANEJAMENTO_MULTITEINER"


def test_handoff_requires_explicit_laboratory_fields():
    package = build_operational_evidence_package((
        confront(
            dimension="PRAZO", key="P1",
            planned="2026-09-10", actual="2026-09-12",
            evidence_ids=("E1",),
        ),
    ), source_kind="SUPABASE", source_ref="pcp")
    try:
        prepare_pcp_symbiont_handoff(
            package,
            tenant_id="T1",
            decision_id="D1",
            observation_id="O1",
            source_ref="pcp",
            source_commit="abc123",
            hypothesis="h",
            baseline="b",
            experiment="e",
            result="r",
            regression_status="OK",
            generalization_status="PARTIAL",
            risk="LOW",
        )
    except TypeError:
        raise AssertionError("all canonical fields are explicitly supplied")
