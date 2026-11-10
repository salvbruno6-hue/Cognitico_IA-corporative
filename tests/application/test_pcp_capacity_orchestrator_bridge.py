from elo.application.use_cases.pcp_capacity_orchestrator_bridge import PCPCapacityOrchestratorBridge
from elo.cognitive.pcp_capacity_expansion import assess_capacity_expansion


def test_purchase_and_capacity_changes_require_external_authorization():
    assessment = assess_capacity_expansion(
        6,
        {"ESTRUTURA": 4, "MONTAGEM": 6},
        demand_by_model={"M01": 6},
        bom_by_model={"M01": {"PIR40": 14}},
        available_components={"PIR40": 70},
        worker_increment_capacity={"ESTRUTURA": 1},
        labor_constrained_resources=["ESTRUTURA"],
    )

    actions = PCPCapacityOrchestratorBridge().orient(assessment)
    by_action = {item.action: item for item in actions}

    assert by_action["EMITIR_NECESSIDADE_COMPRAS"].authorization_required is True
    assert by_action["AUMENTAR_CAPACIDADE_RECURSO"].authorization_required is True


def test_measurement_and_lookup_actions_are_consultative():
    assessment = assess_capacity_expansion(
        6,
        {"ESTRUTURA": 4, "FIBRA": None},
        required_constraints=["ESTRUTURA", "FIBRA"],
    )

    actions = PCPCapacityOrchestratorBridge().orient(assessment)
    assert any(item.action == "LOCALIZAR_CAPACIDADE" and not item.authorization_required for item in actions)


def test_unproven_labor_cause_remains_consultative_for_orchestrator():
    assessment = assess_capacity_expansion(
        6,
        {"ESTRUTURA": 4, "MONTAGEM": 6},
        worker_increment_capacity={"ESTRUTURA": 1},
    )
    actions = PCPCapacityOrchestratorBridge().orient(assessment)
    assert any(
        item.action == "VALIDAR_CAUSA_MAO_DE_OBRA"
        and not item.authorization_required
        and "causa_restricao_mao_de_obra" in item.evidence_required
        for item in actions
    )
