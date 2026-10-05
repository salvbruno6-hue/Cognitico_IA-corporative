from dataclasses import dataclass

from elo.application.use_cases.orchestrator import OrchestrationRequest
from elo.cognitive.response.intelligent_orchestration_response import (
    OrchestrationResponseComposer,
)


@dataclass
class Selection:
    capability_name: str = "EXT-TEST"


@dataclass
class Outcome:
    executed: bool = True
    provider: str = "fake"
    model: str = "test-model"
    request_id: str = "request-1"


def _request():
    return OrchestrationRequest(
        tenant_id="tenant-a",
        principal_id="principal-1",
        domain="cognitive",
        objective="test",
        evidence_ids=("evidence-1",),
        request_id="request-1",
        correlation_id="corr-1",
    )


def test_composer_returns_rich_response_without_creating_execution_authority():
    result = OrchestrationResponseComposer().compose(
        request=_request(),
        selection=Selection(),
        outcome=Outcome(),
    )

    assert result.status == "EXECUTED"
    assert result.stage == "EXECUTE"
    assert result.capability == "EXT-TEST"
    assert result.provider == "fake"
    assert result.model == "test-model"
    assert result.execution_id == "request-1"
    assert result.correlation_id == "corr-1"
    assert result.evidence_state == "OBSERVED"
    assert "O que funcionou" in result.response
    assert "Próximo passo" in result.response
    assert "execução" in result.response.lower()


def test_composer_is_fail_closed_when_no_outcome_exists():
    result = OrchestrationResponseComposer().compose(
        request=_request(),
        selection=Selection(),
        outcome=None,
    )

    assert result.status == "NOT_EXECUTED"
    assert result.stage == "HANDOFF"
    assert result.evidence_state == "INSUFFICIENT"
    assert result.execution_id is None
    assert "Próximo passo" in result.response
    assert "execução não autorizada" in result.response


def test_composer_does_not_claim_learning_or_production():
    result = OrchestrationResponseComposer().compose(
        request=_request(),
        selection=Selection(),
        outcome=Outcome(),
    )

    assert "aprendizado" in result.response.lower()
    assert "produção" not in result.response.lower()
