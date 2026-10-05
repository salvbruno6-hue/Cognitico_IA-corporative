from dataclasses import dataclass
from datetime import datetime, timezone

from elo.application.use_cases.orchestrator import (
    AuthorizationDecision,
    GovernedOrchestrator,
    OrchestrationRequest,
    OrchestrationStage,
)
from elo.core.execution_boundary import ExecutionOutcome, ExecutionStatus
from elo.evidence import Evidence, EvidenceRepository
from elo.cognitive.symbiont_capability_governance import (
    CapabilityVisibilityRecord,
    CapabilityVisibilityState,
    GlobalCapabilityVisibility,
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
        "evidence_ref": "authz-req-001",
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


def test_missing_authorization_evidence_never_executes() -> None:
    result = ORCHESTRATOR.decide_execution(
        request(authorization=canonical_authorization(evidence_ref=""))
    )
    assert result.stage is OrchestrationStage.HANDOFF
    assert result.status == "RECOMMENDATION"


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


def _visibility(capability_id: str, state: CapabilityVisibilityState) -> GlobalCapabilityVisibility:
    return GlobalCapabilityVisibility(
        records=(
            CapabilityVisibilityRecord(
                capability_id=capability_id,
                registry_visible=state in {
                    CapabilityVisibilityState.REGISTERED_VISIBLE,
                    CapabilityVisibilityState.REGISTERED_WITHOUT_IMPLEMENTATION_VIEW,
                    CapabilityVisibilityState.UNRESOLVED_OWNER,
                },
                available=True,
                implementation_visible=state in {
                    CapabilityVisibilityState.REGISTERED_VISIBLE,
                    CapabilityVisibilityState.IMPLEMENTED_NOT_REGISTERED,
                    CapabilityVisibilityState.UNRESOLVED_OWNER,
                },
                owner="owner-a" if state is not CapabilityVisibilityState.UNRESOLVED_OWNER else None,
                runtime_status="INTEGRATED",
                evolution_status="REQUIRED",
                evidence_refs=("ev-visibility",),
                state=state,
            ),
        ),
    )


def test_orchestrator_advises_use_of_existing_canonical_capability() -> None:
    result = ORCHESTRATOR.advise_capability(
        _visibility("cap-a", CapabilityVisibilityState.REGISTERED_VISIBLE),
        "cap-a",
        authorized_actions=frozenset({"USE_CANONICAL"}),
    )
    assert result.action == "USE_CANONICAL"
    assert result.authorized is True
    assert result.owner == "owner-a"


def test_orchestrator_surfaces_connection_gap_without_authorizing_it() -> None:
    result = ORCHESTRATOR.advise_capability(
        _visibility("cap-b", CapabilityVisibilityState.EXISTING_BUT_UNWIRED),
        "cap-b",
    )
    assert result.action == "CONNECT_CANONICAL"
    assert result.authorized is False


def test_orchestrator_does_not_infer_unknown_capability() -> None:
    result = ORCHESTRATOR.advise_capability(
        GlobalCapabilityVisibility(records=()),
        "missing-capability",
        authorized_actions=frozenset({"INVESTIGATE"}),
    )
    assert result.action == "INVESTIGATE"
    assert result.authorized is True
    assert result.state == "UNKNOWN"


@dataclass(frozen=True)
class ResponseSelection:
    capability_name: str = "EXT-TEST"


def test_compose_response_reuses_orchestrator_evidence_repository() -> None:
    repository = EvidenceRepository()
    repository.save(
        Evidence(
            evidence_id="ev-1",
            tenant_id="tenant-a",
            domain="cognitive",
            source_type="test",
            source_id="source-1",
            claim="execution evidence is traceable",
            content_ref="test://ev-1",
            observed_at=datetime.now(timezone.utc),
            provenance={"source": "orchestrator-test"},
        )
    )
    outcome = ExecutionOutcome(
        request_id="request-1",
        status=ExecutionStatus.EXECUTED,
        executed=True,
        reason="authorized_execution_completed",
        provenance={"execution": "executed"},
        evidence_ids=("ev-1",),
        correlation_id="corr-1",
    )

    result = GovernedOrchestrator(
        evidence_repository=repository,
    ).compose_response(
        request(),
        ResponseSelection(),
        outcome,
    )

    assert result.orientation is not None
    assert result.orientation.evidence_refs == ("ev-1",)
    assert result.orientation.confidence.value == "aligned"
