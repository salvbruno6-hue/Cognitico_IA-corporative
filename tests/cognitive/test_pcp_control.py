from datetime import date

import pytest

from elo.cognitive.pcp_control import (
    assess_data_readiness,
    build_pcp_evidence,
    compare_date,
    compare_duration,
    compare_quantity,
    evaluate_pcp_evolution,
)


def test_planned_vs_actual_quantity_and_time():
    qtd = compare_quantity(10, 8, unit="UN")
    assert qtd.variance == -2
    assert qtd.status == "CALCULADO"

    tempo = compare_duration(20, 23)
    assert tempo.variance == 3
    assert tempo.unit == "horas"


def test_planned_vs_actual_date():
    result = compare_date(date(2026, 9, 10), date(2026, 9, 13))
    assert result.variance == 3
    assert result.unit == "dias"


def test_planned_vs_actual_does_not_invent_missing_realized_data():
    result = compare_quantity(10, None)
    assert result.status == "NAO_LOCALIZADO"
    assert result.variance is None


def test_data_readiness_accepts_future_operational_feeding():
    result = assess_data_readiness(
        [
            "mt_planos_pcp",
            "mt_linhas_plano_pcp",
            "mt_ordens_producao",
            "mt_operacoes_ordem_producao",
            "mt_capacidade_diaria",
            "mt_necessidades_materiais",
            "mt_lotes_estoque",
            "mt_eventos_fluxo_modular",
        ]
    )
    assert result.status == "PRONTO"
    assert result.missing == ()


def test_data_readiness_identifies_only_missing_sources():
    result = assess_data_readiness(["mt_planos_pcp"])
    assert result.status == "PENDENTE_DADOS"
    assert "mt_ordens_producao" in result.missing


def test_evidence_requires_provenance_and_evidence_ids():
    with pytest.raises(ValueError):
        build_pcp_evidence(
            observation_id="PCP-1",
            source_ref="",
            source_commit="abc",
            evidence_ids=["E1"],
            baseline="b",
            experiment="e",
            expected_outcome="x",
            observed_outcome="x",
            result="ok",
            regression_status="PASS",
            generalization_status="PARTIAL",
            risk="LOW",
            existing_owner=None,
            scope="controlled",
        )

    with pytest.raises(ValueError):
        build_pcp_evidence(
            observation_id="PCP-1",
            source_ref="github:skill",
            source_commit="abc",
            evidence_ids=[],
            baseline="b",
            experiment="e",
            expected_outcome="x",
            observed_outcome="x",
            result="ok",
            regression_status="PASS",
            generalization_status="PARTIAL",
            risk="LOW",
            existing_owner=None,
            scope="controlled",
        )


def test_evolution_reuses_existing_owner_through_canonical_gate():
    decision = evaluate_pcp_evolution(
        proposal_id="PCP-EVO-1",
        tenant_id="pcp",
        source_id="pcp-test",
        summary="test existing owner",
        purpose_alignment=True,
        identity_compatible=True,
        architecture_compatible=True,
        governance_compatible=True,
        evidence_ids=["E1"],
        maturity_score=0.9,
        existing_owner="SKILL_PLANEJAMENTO_MULTITEINER",
        provenance={"source": "test", "version": "1"},
    )
    assert decision.classification.value == "DUPLICATE/SUPERSEDED"
    assert decision.canonical_mutation_allowed is False
