from elo.core import ConsultingResponse


def test_consulting_response_keeps_analysis_separate_from_decision():
    response = ConsultingResponse(
        objective="Escolher a estrutura contratual mais adequada.",
        context=("Cliente X", "Contrato Y"),
        facts=("Há duas alternativas possíveis.",),
        analysis=("A alternativa A reduz a complexidade operacional.",),
        alternatives=("A", "B"),
        risks=("Validar requisitos jurídicos antes da execução.",),
        recommendation="Avançar com A, condicionada à validação jurídica.",
        decision_required="Responsável deve aprovar a estrutura final.",
        next_actions=("Validar requisitos", "Registrar decisão"),
        status="DECISION_REQUIRED",
    )

    assert response.is_actionable()
    assert response.recommendation is not None
    assert response.decision_required is not None
    assert response.summary_sections()["objective"] == "Escolher a estrutura contratual mais adequada."


def test_consulting_response_can_report_insufficient_evidence():
    response = ConsultingResponse(
        objective="Avaliar uma hipótese.",
        status="INSUFFICIENT_EVIDENCE",
        uncertainty=("A fonte disponível não é suficiente para concluir.",),
    )

    assert not response.is_actionable()
    assert response.status == "INSUFFICIENT_EVIDENCE"
