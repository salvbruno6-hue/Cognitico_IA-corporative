from elo.application.use_cases.orchestrator import (
    GovernedOrchestrator,
    OrchestrationRequest,
    OrchestrationStage,
)


ORCHESTRATOR = GovernedOrchestrator()


def request(**overrides: object) -> OrchestrationRequest:
    values: dict[str, object] = {
        "tenant_id": "tenant-a",
        "principal_id": "principal-a",
        "domain": "orcamento",
        "objective": "avaliar viabilidade",
        "evidence_ids": ("ev-1",),
        "execution_authorized": False,
    }
    values.update(overrides)
    return OrchestrationRequest(**values)  # type: ignore[arg-type]


def test_missing_context_is_blocked() -> None:
    result = ORCHESTRATOR.decide_execution(request(tenant_id=""))
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "BLOCKED"


def test_missing_evidence_is_inconclusive() -> None:
    result = ORCHESTRATOR.decide_execution(request(evidence_ids=()))
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "INCONCLUSIVE"


def test_without_authority_never_executes() -> None:
    result = ORCHESTRATOR.decide_execution(request(execution_authorized=False))
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "RECOMMENDATION"


def test_explicit_authority_and_evidence_permit_execution() -> None:
    result = ORCHESTRATOR.decide_execution(request(execution_authorized=True))
    assert result.stage is OrchestrationStage.EXECUTE
    assert result.status == "AUTHORIZED"
