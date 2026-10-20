from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.reasoning.requirement_analysis import (
    ClaimProvenance,
    RequirementClaim,
    RequirementNode,
    RequirementSourceType,
    RequirementState,
    ResolutionAttemptKind,
)
from elo.cognitive.reasoning.requirement_resolution import (
    RequirementResolutionFlow,
    ResolutionStepResult,
    audit_requirement_resolution,
)


@dataclass
class Provider:
    kind: ResolutionAttemptKind
    result: ResolutionStepResult

    def resolve(self, node, parameter, claims):
        return self.result


def test_structured_cross_entity_reuse_is_explainable_in_bounded_audit():
    original = RequirementClaim(
        claim_id="RULE-PRODUCT-B",
        requirement_id="SO-203.26:R1",
        subject="PRODUCT-B",
        predicate="mdf.thickness",
        value="15 mm",
        state=RequirementState.KNOWN,
        provenance=ClaimProvenance(
            source_type=RequirementSourceType.RULE,
            source_reference="rule:mdf:v1",
            reasoning_method="rule-evaluation:v1",
            evidence_ids=("EV-RULE-SOURCE",),
            validation_status="VALIDATED",
        ),
    )
    node = RequirementNode(
        requirement_id="SO-203.26:R1",
        text="Definir espessura do MDF",
        entity="MLT-C08",
    )
    provider = Provider(
        kind=ResolutionAttemptKind.RULE,
        result=ResolutionStepResult(
            source_reference="rule-engine:v1",
            claims=(original,),
        ),
    )

    result = RequirementResolutionFlow(
        providers={ResolutionAttemptKind.RULE: provider},
        structured_entity_applicability_evidence={
            original.claim_id: ("EV-ENTITY-APPLIES",),
        },
    ).resolve(node=node, parameter="mdf.thickness")
    audit = audit_requirement_resolution(result)

    reuse = audit["attempts"][0]["structured_reuse"][0]
    rebound = result.claims[-1]

    assert reuse == {
        "original_claim_id": "RULE-PRODUCT-B",
        "original_requirement_id": "SO-203.26:R1",
        "original_subject": "PRODUCT-B",
        "recovered_value": "15 mm",
        "target_subject": "MLT-C08",
        "source_reference": "rule:mdf:v1",
        "evidence_ids": ("EV-RULE-SOURCE",),
        "applicability_evidence_ids": ("EV-ENTITY-APPLIES",),
        "bound_claim_id": rebound.claim_id,
    }
    assert rebound.subject == "MLT-C08"
    assert "EV-ENTITY-APPLIES" in rebound.provenance.evidence_ids


def test_resolution_audit_preserves_only_allowlisted_authorized_scope_context():
    node = RequirementNode(
        requirement_id="SO-203.26:R1",
        text="Definir espessura do MDF",
        entity="MLT-C08",
        metadata={
            "retrieval.tenant_id": "tenant-elo",
            "retrieval.domain": "budgeting",
            "retrieval.principal_id": "principal-7",
            "retrieval.session_id": "session-9",
            "retrieval.request_id": "request-11",
            "retrieval.correlation_id": "corr-13",
            "retrieval.source_id": "source-17",
            "retrieval.source_kind": "knowledge",
            "retrieval.required_capability": "knowledge.read",
            "retrieval.authorization_scope": "tenant:tenant-elo:budgeting",
            "private_reasoning": "do not expose",
            "credential": "secret-value",
            "random": "untrusted metadata",
            "retrieval.uri": "should-not-be-carried-by-resolution-scope",
            "retrieval.conversation_id": "also-not-scope",
            "retrieval.classification": "internal",
            "retrieval.record_id": "record-19",
            "retrieval.reported_source_type": "provider-supplied",
        },
    )

    result = RequirementResolutionFlow(providers={}).resolve(
        node=node,
        parameter="mdf.thickness",
    )
    audit = audit_requirement_resolution(result)

    assert audit["scope"] == {
        "retrieval.tenant_id": "tenant-elo",
        "retrieval.domain": "budgeting",
        "retrieval.principal_id": "principal-7",
        "retrieval.session_id": "session-9",
        "retrieval.request_id": "request-11",
        "retrieval.correlation_id": "corr-13",
        "retrieval.source_id": "source-17",
        "retrieval.source_kind": "knowledge",
        "retrieval.required_capability": "knowledge.read",
        "retrieval.authorization_scope": "tenant:tenant-elo:budgeting",
    }
    serialized = repr(audit)
    assert "do not expose" not in serialized
    assert "secret-value" not in serialized
    assert "untrusted metadata" not in serialized
    assert "should-not-be-carried-by-resolution-scope" not in serialized
    assert "also-not-scope" not in serialized
    assert "record-19" not in serialized
    assert "provider-supplied" not in serialized


def test_blank_allowlisted_scope_values_are_omitted():
    node = RequirementNode(
        requirement_id="SO-203.26:R1",
        text="Definir espessura do MDF",
        entity="MLT-C08",
        metadata={
            "retrieval.tenant_id": "tenant-elo",
            "retrieval.request_id": "   ",
        },
    )

    result = RequirementResolutionFlow(providers={}).resolve(
        node=node,
        parameter="mdf.thickness",
    )
    audit = audit_requirement_resolution(result)

    assert audit["scope"] == {"retrieval.tenant_id": "tenant-elo"}
    assert "retrieval.request_id" not in audit["scope"]
