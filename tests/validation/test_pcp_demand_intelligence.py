from src.elo.cognitive.pcp_demand_intelligence import (
    governance_invariants,
    physical_gaps,
    resolve_indicator_plan,
)


def codes(intent: str, physical: bool = False) -> list[str]:
    return [step.code for step in resolve_indicator_plan(intent, physical_data_available=physical)]


def test_peak_analysis_queries_cause_after_variation():
    plan = codes("explique o pico de julho e por que houve subida")
    assert plan.index("DEM_YOY") < plan.index("DRV_NATUREZA")
    assert plan.index("DRV_NATUREZA") < plan.index("DRV_MODELO")
    assert plan.index("DRV_MODELO") < plan.index("DRV_CLIENTE")


def test_preparation_queries_return_stock_and_physical_gates():
    plan = resolve_indicator_plan("como devemos nos preparar para janeiro com estoque e cobertura")
    ids = [step.code for step in plan]
    assert ids.index("RET_PREV_MODELO") < ids.index("EST_SEGURANCA")
    assert ids.index("EST_SEGURANCA") < ids.index("DISP_PROJETADA")
    assert ids.index("DISP_PROJETADA") < ids.index("CAPACIDADE_ATENDIMENTO")
    gaps = physical_gaps(plan, physical_data_available=False)
    assert "QUA_ENTRADAS" in gaps
    assert "DISP_PROJETADA" in gaps
    assert "CAPACIDADE_ATENDIMENTO" in gaps


def test_direct_coverage_includes_protection_prerequisites():
    plan = codes("qual a cobertura de janeiro?")
    assert plan.index("EST_SPOT_P75") < plan.index("PROTECAO_COMERCIAL")
    assert plan.index("PROTECAO_COMERCIAL") < plan.index("DISP_PROJETADA")
    assert plan.index("DISP_PROJETADA") < plan.index("CAPACIDADE_ATENDIMENTO")


def test_availability_domain_noun_is_recognized():
    plan = resolve_indicator_plan("qual a disponibilidade em janeiro?")
    ids = [step.code for step in plan]
    assert "DISP_PATIO_ATUAL" in ids
    assert "DISP_PROJETADA" in ids
    assert "PROTECAO_COMERCIAL" in ids
    gaps = physical_gaps(plan, physical_data_available=False)
    assert "DISP_PROJETADA" in gaps


def test_return_question_keeps_spot_event_and_model_detail():
    plan = codes("mostre retornos previstos por modelo em novembro e dezembro")
    assert "RET_PREV_TOTAL" in plan
    assert "RET_PREV_SPOT" in plan
    assert "RET_PREV_EVENTO" in plan
    assert "RET_PREV_MODELO" in plan


def test_governance_invariants_are_fail_closed():
    invariants = governance_invariants()
    assert "MÓDULO_CONTÊINER_SEPARADOS" in invariants
    assert "SPOT_EVENTO_SEPARADOS" in invariants
    assert "RETORNO_PREVISTO_NAO_E_ESTOQUE_LIVRE" in invariants
    assert "GAP_NAO_E_ZERO" in invariants
