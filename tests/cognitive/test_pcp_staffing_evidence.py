from elo.cognitive.pcp_staffing_evidence import (
    StaffingEvidenceState,
    assess_staffing_evidence,
)


def _complete_evidence():
    return {
        "periodo_observado": "2026-10",
        "equipe_por_setor_funcao": {"MONTAGEM": {"MONTADOR": 6}},
        "turnos_jornada": {"turno": "1", "horas": 8},
        "horas_extras": 0,
        "absenteismo": 0,
        "mix_modelos": {"M01": 10, "M02": 4},
        "el_disponivel": 5,
        "esperas_material": 0,
        "retrabalho_reprovacao": 0,
        "wip": 3,
        "equipamentos_indisponibilidades": [],
        "producao_realizada": {"media_modulos_dia": 6},
    }


def test_historical_six_per_day_remains_noncanonical_with_missing_context():
    result = assess_staffing_evidence({}, observed_modules_per_day=6)
    assert result.state == StaffingEvidenceState.EVIDENCE_COLLECTION_REQUIRED
    assert result.observation is not None
    assert result.observation.canonicalizable is False
    assert "equipe_por_setor_funcao" in result.observation.missing_context
    assert result.can_calculate_headcount is False


def test_next_gap_prioritizes_decision_critical_collection():
    result = assess_staffing_evidence({}, observed_modules_per_day=6)
    assert result.gap_plan.next_gap is not None
    assert result.gap_plan.next_gap.parameter in {
        "periodo_observado",
        "equipe_por_setor_funcao",
        "mix_modelos",
        "el_disponivel",
        "producao_realizada",
    }


def test_complete_context_still_does_not_imply_labor_cause():
    result = assess_staffing_evidence(_complete_evidence(), observed_modules_per_day=6)
    assert result.state == StaffingEvidenceState.CAUSE_NOT_ESTABLISHED
    assert result.can_calculate_headcount is False


def test_non_labor_constraint_blocks_hiring_calculation():
    result = assess_staffing_evidence(
        _complete_evidence(),
        observed_modules_per_day=6,
        causal_constraint="EL",
    )
    assert result.state == StaffingEvidenceState.NON_LABOR_CONSTRAINT
    assert result.can_calculate_headcount is False


def test_labor_constraint_requires_marginal_productivity():
    result = assess_staffing_evidence(
        _complete_evidence(),
        observed_modules_per_day=6,
        causal_constraint="MAO_DE_OBRA",
    )
    assert result.state == StaffingEvidenceState.MARGINAL_PRODUCTIVITY_REQUIRED
    assert result.can_calculate_headcount is False


def test_headcount_becomes_calculable_only_with_causal_and_marginal_evidence():
    result = assess_staffing_evidence(
        _complete_evidence(),
        observed_modules_per_day=6,
        causal_constraint="MAO_DE_OBRA",
        marginal_productivity_per_worker=0.5,
    )
    assert result.state == StaffingEvidenceState.STAFFING_EVIDENCE_READY
    assert result.can_calculate_headcount is True
