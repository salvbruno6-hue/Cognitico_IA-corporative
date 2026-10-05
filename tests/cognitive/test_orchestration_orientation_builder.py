from datetime import datetime, timezone

import pytest

_UNSET = object()

from elo.cognitive.orchestration_orientation import (
    OrchestrationOrientationBuilder,
    OrientationConfidence,
    OrientationRequest,
)
from elo.cognitive.routing.execution_routing import RoutingDecision
from elo.core.context_resolution import ContextEvidence
from elo.core.execution_boundary import ExecutionOutcome, ExecutionStatus
from elo.evidence import Evidence


def evidence(*, evidence_id: str = "ev-1", source_id: str = "src-1", provenance=_UNSET):
    return Evidence(
        evidence_id=evidence_id,
        tenant_id="tenant-1",
        domain="planning",
        source_type="test",
        source_id=source_id,
        claim="claim",
        content_ref="ref",
        observed_at=datetime.now(timezone.utc),
        quality="VERIFIED",
        relevance=1.0,
        provenance={"source": "test"} if provenance is _UNSET else provenance,
    )


def outcome(status=ExecutionStatus.EXECUTED, executed=True, reason="ok"):
    return ExecutionOutcome(
        request_id="req-1",
        status=status,
        executed=executed,
        reason=reason,
        provenance={"source": "test"},
        evidence_ids=("ev-1",),
        correlation_id="corr-1",
        authorization_id="auth-1",
        occurred_at=datetime.now(timezone.utc),
    )


def test_empty_request_is_insufficient():
    result = OrchestrationOrientationBuilder().build(
        OrientationRequest(capability="analysis")
    )
    assert result.confidence is OrientationConfidence.INSUFFICIENT
    assert result.evidence_refs == ()
    assert result.blocker is None


def test_provenance_without_execution_is_partial_not_aligned():
    result = OrchestrationOrientationBuilder().build(
        OrientationRequest(capability="analysis", source_facts=(evidence(),))
    )
    assert result.confidence is OrientationConfidence.PARTIAL
    assert result.evidence_refs == ("ev-1",)


def test_provenance_and_observed_execution_can_be_aligned():
    result = OrchestrationOrientationBuilder().build(
        OrientationRequest(
            capability="analysis",
            source_facts=(evidence(),),
            execution_outcome=outcome(),
        )
    )
    assert result.confidence is OrientationConfidence.ALIGNED
    assert "1 referência" in result.diagnosis
    assert "estado de confiança=aligned" in result.rationale


def test_missing_provenance_cannot_support_aligned():
    result = OrchestrationOrientationBuilder().build(
        OrientationRequest(
            capability="analysis",
            source_facts=(evidence(provenance={}),),
            execution_outcome=outcome(),
        )
    )
    assert result.confidence is OrientationConfidence.PARTIAL


def test_route_capability_mismatch_is_observable_inconsistency():
    result = OrchestrationOrientationBuilder().build(
        OrientationRequest(
            capability="analysis",
            source_facts=(evidence(),),
            routing_decision=RoutingDecision(
                capability="other",
                model_id="model-1",
                tool_id=None,
                rationale="selected",
            ),
            execution_outcome=outcome(),
        )
    )
    assert result.confidence is OrientationConfidence.PARTIAL
    assert result.blocker is not None
    assert "routing_decision capability" in result.blocker


def test_blocked_reason_is_preserved_without_inventing_generic_cause():
    result = OrchestrationOrientationBuilder().build(
        OrientationRequest(
            capability="analysis",
            execution_outcome=outcome(
                status=ExecutionStatus.BLOCKED,
                executed=False,
                reason="missing_execution_controls:authorization_id",
            ),
        )
    )
    assert result.confidence is OrientationConfidence.INSUFFICIENT
    assert result.blocker == "missing_execution_controls:authorization_id"
    assert "controle ausente no fluxo canônico" not in result.diagnosis


def test_different_claims_from_same_source_are_not_declared_conflict():
    first = evidence(evidence_id="ev-1", source_id="src-1")
    second = Evidence(
        evidence_id="ev-2",
        tenant_id="tenant-1",
        domain="planning",
        source_type="test",
        source_id="src-1",
        claim="another observable claim",
        content_ref="ref-2",
        observed_at=datetime.now(timezone.utc),
        provenance={"source": "test"},
    )
    result = OrchestrationOrientationBuilder().build(
        OrientationRequest(
            capability="analysis",
            source_facts=(first, second),
            execution_outcome=outcome(),
        )
    )
    assert result.confidence is OrientationConfidence.ALIGNED
    assert result.blocker is None


def test_invalid_request_raises_value_error():
    with pytest.raises(ValueError):
        OrchestrationOrientationBuilder().build("invalid")  # type: ignore[arg-type]


def test_builder_is_deterministic_for_same_input():
    request = OrientationRequest(
        capability="analysis",
        context={"domain": "planning"},
        source_facts=(evidence(),),
        execution_outcome=outcome(),
    )
    builder = OrchestrationOrientationBuilder()
    assert builder.build(request) == builder.build(request)


def test_context_evidence_uses_source_id_as_reference():
    fact = ContextEvidence(
        source_id="context-src-1",
        fact="observable fact",
        confidence=0.9,
        provenance={"source": "test"},
    )
    result = OrchestrationOrientationBuilder().build(
        OrientationRequest(
            capability="analysis",
            source_facts=(fact,),
            execution_outcome=outcome(),
        )
    )
    assert result.evidence_refs == ("context-src-1",)
    assert result.confidence is OrientationConfidence.ALIGNED


def test_executed_with_non_executed_status_is_partial():
    """Invariante 15 — ALIGNED exige consistência."""
    outcome_inconsistent = outcome(
        status=ExecutionStatus.BLOCKED,
        executed=True,
        reason="inconsistent: executed=True with non-EXECUTED status",
    )
    request = OrientationRequest(
        capability="test-capability",
        source_facts=(evidence(),),
        execution_outcome=outcome_inconsistent,
    )
    result = OrchestrationOrientationBuilder().build(request)
    assert result.confidence is OrientationConfidence.PARTIAL
    assert result.blocker is not None
    assert "executed=True" in result.blocker
    assert "non-EXECUTED status" in result.blocker


def test_next_step_derives_from_observable_blocker():
    """Invariante 12 — next_step deriva de fonte observável."""
    outcome_inconsistent = outcome(
        status=ExecutionStatus.BLOCKED,
        executed=True,
        reason="inconsistent: executed=True with non-EXECUTED status",
    )
    request = OrientationRequest(
        capability="test-capability",
        source_facts=(evidence(),),
        execution_outcome=outcome_inconsistent,
    )
    result = OrchestrationOrientationBuilder().build(request)
    assert isinstance(result.next_step, str)
    assert result.next_step.strip() != ""
    assert "Resolver os bloqueios ou conflitos observáveis" in result.next_step


def test_orientation_has_no_attributed_or_production_proven_fields():
    """Invariante 19 — Builder não declara ATTRIBUTED / PRODUCTION_PROVEN."""
    import dataclasses

    fields = {f.name for f in dataclasses.fields(result_type := type(
        OrchestrationOrientationBuilder().build(
            OrientationRequest(capability="test-capability")
        )
    ))}
    forbidden = {
        "attributed",
        "attribution",
        "attributed_state",
        "production_proven",
        "production_status",
        "production_state",
    }
    assert fields.isdisjoint(forbidden), (
        f"Orientation não pode expor campos de estado de produção/"
        f"atribuição: {fields & forbidden}"
    )
    result = OrchestrationOrientationBuilder().build(
        OrientationRequest(
            capability="test-capability",
            source_facts=(evidence(),),
        )
    )
    for name in forbidden:
        assert not hasattr(result, name), (
            f"Orientation não deve ter atributo '{name}'"
        )
