from elo.application.use_cases.orchestrator import (
    AuthorizationDecision,
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
        "authorization": None,
    }
    values.update(overrides)
    return OrchestrationRequest(**values)  # type: ignore[arg-type]


def canonical_authorization(**overrides: object) -> AuthorizationDecision:
    values: dict[str, object] = {
        "authorized": True,
        "authority": "elo-authz",
        "identity_id": "identity-a",
        "role": "ELO_ADMIN",
    }
    values.update(overrides)
    return AuthorizationDecision(**values)  # type: ignore[arg-type]


def test_missing_context_is_blocked() -> None:
    result = ORCHESTRATOR.decide_execution(request(tenant_id=""))
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "BLOCKED"


def test_missing_evidence_is_inconclusive() -> None:
    result = ORCHESTRATOR.decide_execution(request(evidence_ids=()))
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "INCONCLUSIVE"


def test_without_canonical_authorization_never_executes() -> None:
    result = ORCHESTRATOR.decide_execution(request())
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "RECOMMENDATION"
    assert "absent" in result.reason


def test_denied_canonical_authorization_never_executes() -> None:
    result = ORCHESTRATOR.decide_execution(
        request(authorization=canonical_authorization(authorized=False))
    )
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "RECOMMENDATION"


def test_non_canonical_authority_never_executes() -> None:
    result = ORCHESTRATOR.decide_execution(
        request(authorization=canonical_authorization(authority="local-orchestrator"))
    )
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "RECOMMENDATION"
    assert "provenance" in result.reason


def test_partial_provenance_never_executes() -> None:
    result = ORCHESTRATOR.decide_execution(
        request(authorization=canonical_authorization(identity_id=""))
    )
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "RECOMMENDATION"


def test_canonical_authorization_and_evidence_permit_execution() -> None:
    result = ORCHESTRATOR.decide_execution(
        request(authorization=canonical_authorization())
    )
    assert result.stage is OrchestrationStage.EXECUTE
    assert result.status == "AUTHORIZED"
