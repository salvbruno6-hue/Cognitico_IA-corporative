from elo.cognitive.reasoning.critical_gap_reasoning import (
    CriticalEvidenceGap,
    GapCriticality,
    build_admin_decision_questionnaire,
    prioritize_evidence_gaps,
)
from elo.interface.contracts import CognitiveRequest
from elo.interface.response import ResponseBuilder


def test_response_builder_surfaces_admin_gap_as_governed_suggested_action():
    gap = CriticalEvidenceGap(
        gap_id="GAP-CAPACIDADE",
        parameter="capacidade_validada",
        decision="PLANO_PRODUCAO",
        missing_condition="capacidade real por etapa não confirmada",
        operational_impact="sem a capacidade real, o prazo não pode ser confirmado",
        collection_action="informar capacidade observada, período e condição operacional",
        owner="PCP",
        criticality=GapCriticality.CRITICAL,
        decision_sensitivity=5,
        collection_effort=2,
        blocks_decision=True,
        evidence_refs=("ev-cap-1",),
    )
    questions = build_admin_decision_questionnaire(
        prioritize_evidence_gaps((gap,))
    )
    request = CognitiveRequest(
        message="confirme o plano",
        tenant_id="tenant-a",
        correlation_id="corr-a",
    )

    response = ResponseBuilder().build(
        request,
        "session-a",
        {
            "response": {"type": "analysis", "content": "Plano parcialmente sustentado."},
            "confidence": 0.5,
            "admin_decision_questions": questions,
            "provenance": {"validation_status": "PARTIAL"},
        },
    )

    assert len(response.suggestions) == 1
    question = response.suggestions[0]
    assert question.action_id == "ADM-GAP-CAPACIDADE"
    assert question.action_type == "admin_decision_question"
    assert question.requires_approval is True
    assert question.payload["gap_id"] == "GAP-CAPACIDADE"
    assert question.payload["answer_contract"] == "HUMAN_EVIDENCE_CANDIDATE"
    assert question.payload["evidence_refs"] == ["ev-cap-1"]
    assert "capacidade real por etapa não confirmada" in question.label


def test_response_builder_ignores_invalid_empty_admin_question():
    request = CognitiveRequest(message="x", tenant_id="tenant-a")

    response = ResponseBuilder().build(
        request,
        "session-a",
        {
            "response": {"type": "analysis", "content": "x"},
            "admin_decision_questions": [{"question_id": "ADM-X", "prompt": ""}],
        },
    )

    assert response.suggestions == []
