import pytest

from elo.cognitive.reasoning.critical_gap_reasoning import (
    CriticalEvidenceGap,
    GapCriticality,
    GapPlanState,
    ObservationUse,
    prioritize_evidence_gaps,
    qualify_observation,
    build_admin_decision_questionnaire,
)


def _gap(
    gap_id: str,
    parameter: str,
    *,
    criticality: GapCriticality,
    sensitivity: int,
    effort: int,
    blocks: bool = True,
) -> CriticalEvidenceGap:
    return CriticalEvidenceGap(
        gap_id=gap_id,
        parameter=parameter,
        decision="CONTRATACAO_MONTAGEM",
        missing_condition=f"evidência ausente: {parameter}",
        operational_impact=f"sem {parameter}, a causa da restrição não é comprovada",
        collection_action=f"coletar {parameter} por período e setor",
        owner="PRODUCAO_RH",
        criticality=criticality,
        decision_sensitivity=sensitivity,
        collection_effort=effort,
        blocks_decision=blocks,
    )


def test_orchestrator_prioritizes_the_gap_with_highest_decision_power():
    plan = prioritize_evidence_gaps(
        [
            _gap(
                "GAP-ABSENTEISMO",
                "absenteismo",
                criticality=GapCriticality.HIGH,
                sensitivity=3,
                effort=2,
            ),
            _gap(
                "GAP-EQUIPE",
                "quantidade_colaboradores_por_setor_funcao_turno",
                criticality=GapCriticality.CRITICAL,
                sensitivity=5,
                effort=2,
            ),
            _gap(
                "GAP-RETRABALHO",
                "retrabalho",
                criticality=GapCriticality.HIGH,
                sensitivity=4,
                effort=3,
            ),
        ]
    )

    assert plan.state is GapPlanState.DECISION_BLOCKED
    assert plan.next_gap is not None
    assert plan.next_gap.gap_id == "GAP-EQUIPE"
    assert plan.blocked_decisions == ("CONTRATACAO_MONTAGEM",)
    assert plan.canonical_mutation is False


def test_missing_field_is_explained_by_impact_and_collection_action():
    gap = _gap(
        "GAP-MIX",
        "mix_modelos_m01_m02",
        criticality=GapCriticality.CRITICAL,
        sensitivity=5,
        effort=1,
    )

    assert "causa da restrição" in gap.operational_impact
    assert gap.collection_action.startswith("coletar")
    assert gap.priority_score > 0


def test_six_per_day_can_be_historical_without_becoming_canonical_capacity():
    observation = qualify_observation(
        observation_id="MONTAGEM-6-DIA",
        statement="oficina de montagem observada em média de 6 módulos/dia",
        source_ref="informação operacional do usuário",
        missing_context=(
            "periodo_observado",
            "quantidade_colaboradores_por_funcao",
            "turnos_e_jornada",
            "horas_extras",
            "mix_modelos",
            "el_disponivel",
            "esperas_por_material",
            "retrabalho",
        ),
    )

    assert ObservationUse.HISTORICAL_EVIDENCE in observation.allowed_uses
    assert ObservationUse.SCENARIO_INPUT in observation.allowed_uses
    assert ObservationUse.CANONICAL_RULE not in observation.allowed_uses
    assert observation.canonicalizable is False


def test_canonical_capacity_is_fail_closed_while_context_is_missing():
    with pytest.raises(ValueError, match="contextual evidence is missing"):
        qualify_observation(
            observation_id="MONTAGEM-6-DIA",
            statement="6 módulos/dia",
            source_ref="historical observation",
            missing_context=("mix_modelos",),
            authorize_canonical_rule=True,
        )


def test_no_gaps_never_authorizes_a_business_action():
    plan = prioritize_evidence_gaps([])

    assert plan.state is GapPlanState.NO_GAPS
    assert plan.next_gap is None
    assert plan.canonical_mutation is False



def test_admin_questionnaire_uses_existing_gap_priority_and_never_invents_answer():
    plan = prioritize_evidence_gaps(
        [
            _gap(
                "GAP-LOW",
                "espera_material",
                criticality=GapCriticality.MEDIUM,
                sensitivity=2,
                effort=3,
            ),
            _gap(
                "GAP-HIGH",
                "quantidade_colaboradores",
                criticality=GapCriticality.CRITICAL,
                sensitivity=5,
                effort=1,
            ),
        ]
    )

    questions = build_admin_decision_questionnaire(plan)

    assert [item.gap_id for item in questions] == ["GAP-HIGH", "GAP-LOW"]
    assert questions[0].parameter == "quantidade_colaboradores"
    assert "evidência ausente: quantidade_colaboradores" in questions[0].prompt
    assert questions[0].response_guidance == "coletar quantidade_colaboradores por período e setor"
    assert questions[0].answer_contract == "HUMAN_EVIDENCE_CANDIDATE"
    assert questions[0].blocks_decision is True
    assert questions[0].to_payload()["decision"] == "CONTRATACAO_MONTAGEM"


def test_admin_questionnaire_excludes_non_blocking_gaps_by_default():
    plan = prioritize_evidence_gaps(
        [
            _gap(
                "GAP-INFO",
                "referencia_auxiliar",
                criticality=GapCriticality.LOW,
                sensitivity=1,
                effort=1,
                blocks=False,
            )
        ]
    )

    assert build_admin_decision_questionnaire(plan) == ()
    assert len(build_admin_decision_questionnaire(plan, include_non_blocking=True)) == 1


def test_admin_questionnaire_has_bounded_question_count():
    plan = prioritize_evidence_gaps(
        [
            _gap(
                f"GAP-{index}",
                f"parametro_{index}",
                criticality=GapCriticality.HIGH,
                sensitivity=3,
                effort=2,
            )
            for index in range(8)
        ]
    )

    questions = build_admin_decision_questionnaire(plan, max_questions=3)
    assert len(questions) == 3
    with pytest.raises(ValueError, match="between 1 and 20"):
        build_admin_decision_questionnaire(plan, max_questions=0)


def test_no_gap_produces_no_admin_question():
    assert build_admin_decision_questionnaire(prioritize_evidence_gaps([])) == ()
