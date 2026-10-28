from datetime import date

import pytest

from elo.cognitive.pcp_control import (
    assess_data_readiness,
    assess_demand_capacity,
    assess_empirical_capacity_learning,
    assess_material_availability,
    assess_staffing_ramp,
    assess_systemic_capacity,
    build_pcp_evidence,
    calculate_mix_component_requirements,
    compare_date,
    compare_duration,
    compare_quantity,
    evaluate_pcp_evolution,
    project_el_balance,
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


def test_demand_is_always_confronted_with_period_capacity():
    result = assess_demand_capacity(
        68,
        capacity_per_day=2.5,
        productive_days=22,
    )
    assert result.period_capacity == 55
    assert result.deficit == 13
    assert result.spillover_quantity == 13
    assert result.utilization_pct == pytest.approx(123.6363, rel=1e-4)
    assert result.status == "CAPACIDADE_INSUFICIENTE"


def test_demand_capacity_preserves_missing_capacity_as_unknown():
    result = assess_demand_capacity(
        68,
        capacity_per_day=None,
        productive_days=22,
    )
    assert result.period_capacity is None
    assert result.deficit is None
    assert result.status == "CAPACIDADE_NAO_LOCALIZADA"


def test_mix_requirement_uses_model_mix_instead_of_total_modules():
    result = calculate_mix_component_requirements(
        {"M01": 15, "M02": 5},
        {
            "M01": {"PIR40": 14},
            "M02": {"PIR40": 17, "CUBA_P": 1},
        },
    )
    assert result.requirements["PIR40"] == 295
    assert result.requirements["CUBA_P"] == 5
    assert result.status == "CALCULADO"


def test_mix_requirement_blocks_missing_bom_instead_of_inventing():
    result = calculate_mix_component_requirements(
        {"M01": 10, "M02": 10},
        {"M01": {"PIR40": 14}},
    )
    assert result.requirements["PIR40"] == 140
    assert result.missing_bom_models == ("M02",)
    assert result.status == "RESPOSTA_PARCIAL"


def test_systemic_capacity_is_limited_by_fiber_when_all_units_require_it():
    result = assess_systemic_capacity(
        4,
        {
            "estrutura": 4,
            "el": 4,
            "montagem": 4,
            "fibra": 2,
            "qualidade": 4,
        },
    )
    assert result.executable_units == 2
    assert result.limiting_constraints == ("fibra",)
    assert result.status == "CAPACIDADE_SISTEMICA_INSUFICIENTE"


def test_systemic_capacity_preserves_unknown_required_constraint():
    result = assess_systemic_capacity(
        4,
        {"estrutura": 4, "fibra": 4, "qualidade": None},
        required_constraints=("estrutura", "fibra", "qualidade"),
    )
    assert result.executable_units == 4
    assert result.unknown_constraints == ("qualidade",)
    assert result.status == "RESPOSTA_PARCIAL"


def test_el_two_caps_assembly_plan_four_at_two():
    result = project_el_balance(
        2,
        daily_releases=[0],
        daily_assembly_plan=[4],
    )
    assert result.days[0].realizable_assembly == 2
    assert result.days[0].status == "MONTAGEM_LIMITADA_POR_EL"
    assert result.first_constraint_day == 1


def test_el_five_caps_recovery_plan_six_at_five_without_prior_release():
    result = project_el_balance(
        5,
        daily_releases=[0],
        daily_assembly_plan=[6],
    )
    assert result.days[0].realizable_assembly == 5
    assert result.first_constraint_day == 1


def test_el_projection_is_cumulative_across_days():
    result = project_el_balance(
        4,
        daily_releases=[4, 4, 0],
        daily_assembly_plan=[4, 4, 4],
    )
    assert [day.closing_el for day in result.days] == [4, 4, 0]
    assert result.first_constraint_day == 3


def test_staffing_ramp_uses_observed_team_productivity_but_does_not_authorize_hiring():
    result = assess_staffing_ramp(
        6,
        output_per_team_per_day=4,
        current_teams=1,
        workers_per_team=2,
    )
    assert result.required_teams == 2
    assert result.additional_teams == 1
    assert result.additional_workers == 2
    assert result.status == "CAPACITY_RAMP_CANDIDATE"


def test_staffing_ramp_does_not_invent_missing_team_productivity():
    result = assess_staffing_ramp(
        6,
        output_per_team_per_day=None,
        current_teams=1,
        workers_per_team=2,
    )
    assert result.required_teams is None
    assert result.additional_workers is None
    assert result.status == "PRODUTIVIDADE_EQUIPE_NAO_LOCALIZADA"


def test_material_availability_uses_warehouse_quantity_and_purchase_lead_time():
    result = assess_material_availability(
        680,
        300,
        lead_time_days=12,
        reference_date=date(2026, 10, 18),
    )
    assert result.shortage_quantity == 380
    assert result.available_on == date(2026, 10, 30)
    assert result.status == "REPOSICAO_NECESSARIA"


def test_material_availability_does_not_invent_missing_lead_time():
    result = assess_material_availability(
        680,
        300,
        lead_time_days=None,
        reference_date=date(2026, 10, 18),
    )
    assert result.available_on is None
    assert result.status == "LEAD_TIME_NAO_LOCALIZADO"


def test_recurrent_capacity_divergence_becomes_learning_candidate_only():
    result = assess_empirical_capacity_learning(
        4.0,
        [3.2, 3.1, 3.3, 3.2],
        min_samples=3,
        tolerance_pct=10,
    )
    assert result.observed_capacity == pytest.approx(3.2)
    assert result.deviation_pct == pytest.approx(-20.0)
    assert result.direction == "ABAIXO"
    assert result.confidence == 1.0
    assert result.status == "CANDIDATO_AJUSTE"


def test_capacity_learning_requires_repetition_before_candidate():
    result = assess_empirical_capacity_learning(
        4.0,
        [3.1, 3.2],
        min_samples=3,
        tolerance_pct=10,
    )
    assert result.status == "EVIDENCIA_INSUFICIENTE"
    assert result.confidence == pytest.approx(2 / 3)


def test_capacity_learning_keeps_empirical_baseline_when_observed_is_stable():
    result = assess_empirical_capacity_learning(
        4.0,
        [3.9, 4.0, 4.1],
        min_samples=3,
        tolerance_pct=10,
    )
    assert result.status == "ESTAVEL"


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
