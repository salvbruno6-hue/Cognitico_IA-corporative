from elo.cognitive.pcp_data_questions import analysis_status, evaluate_goal, project_questions


def test_quantity_gap_can_be_answered_without_full_operational_database():
    result = evaluate_goal("atraso_op", {"quantidade_planejada": 100, "quantidade_produzida": 70})
    assert result.status == "RESPOSTA_PARCIAL"
    assert result.level == "S1"
    assert result.next_evidence == ("fim_planejado", "fim_real")


def test_capacity_can_be_calculated_without_stock():
    result = evaluate_goal("capacidade_atendimento", {"demanda": 100, "capacidade_disponivel": 120})
    assert result.status == "DADOS_SUFICIENTES"
    assert result.level == "S2"
    assert "estoque_disponivel" in result.complementary


def test_missing_data_is_not_inference_permission_and_does_not_fake_result():
    result = evaluate_goal("capacidade_atendimento", {"demanda": 100})
    assert result.status == "ANALISE_BLOQUEADA"
    assert result.blocking == ("capacidade_disponivel",)


def test_no_data_is_distinguished_from_blocking_after_partial_evidence():
    empty = evaluate_goal("material_op", {})
    partial = evaluate_goal("material_op", {"quantidade_bruta": 8})
    assert empty.status == "DADOS_NAO_LOCALIZADOS"
    assert partial.status == "RESPOSTA_PARCIAL"


def test_questions_mark_only_goal_relevant_blockers():
    gaps = project_questions("capacidade_atendimento", {"demanda": 100})
    by_key = {gap.key: gap for gap in gaps}
    assert by_key["capacidade_disponivel"].blocking is True
    assert by_key["estoque_disponivel"].blocking is False


def test_analysis_status_no_longer_requires_every_source():
    assert analysis_status("capacidade_atendimento", {"demanda": 100, "capacidade_disponivel": 120}) == "DADOS_SUFICIENTES"
