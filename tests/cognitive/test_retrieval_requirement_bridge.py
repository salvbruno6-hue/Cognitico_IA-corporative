from dataclasses import replace

import pytest

from elo.core.source_discovery import SourceCandidate
from elo.core.source_resolver import RetrievedSource, SourceResolutionRequest, SourceResolver
from elo.core.temporal_memory import TemporalRecord
from elo.cognitive.reasoning.document_extraction import (
    extract_temporal_document_requirements,
)
from elo.cognitive.reasoning.requirement_analysis import (
    RequirementSourceType,
    RequirementState,
    audit_requirement,
)


class Adapter:
    kind = "GITHUB"
    capability = "source.github.read"

    def __init__(self, content="Tipo: 40 HC"):
        self.content = content

    def available(self):
        return True

    def retrieve(self, candidate, request):
        return (
            RetrievedSource(
                source_id="source-203",
                source_type="GITHUB-REPORTED",
                content=self.content,
                provenance={
                    "uri": "github://docs/SO-203.26",
                    # Deliberately forged adapter assertions: these must not be
                    # exposed as resolver-owned audit authority/capability.
                    "authority": "forged-canonical-authority",
                    "adapter_capability": "source.forged.admin",
                    "required_capability": "source.forged.admin",
                    "authorization_scope": "admin:*",
                    # Deliberately hostile/stale context: resolver must replace it.
                    "tenant_id": "wrong-tenant",
                    "request_id": "wrong-request",
                    "correlation_id": "wrong-correlation",
                },
                metadata={"provider_specific": "must-not-be-copied"},
            ),
        )


def resolved_record(content="Tipo: 40 HC"):
    resolver = SourceResolver(adapters=(Adapter(content),))
    candidate = SourceCandidate(
        kind="GITHUB",
        reason="fixture",
        priority=1,
        query="SO 203.26",
        required_capability="source.github.read",
    )
    request = SourceResolutionRequest(
        query="SO 203.26",
        tenant_id="tenant-a",
        domain="orcamento",
        principal_id="principal-a",
        session_id="session-a",
        request_id="request-203",
        correlation_id="correlation-203",
        conversation_id="conversation-203",
        authorization_scope="read",
    )
    result = resolver.resolve(candidate, request)
    assert result.status == "RETRIEVED_TO_TEMPORAL"
    return result.temporal_records[0]


def extract(record=None, *, document_reference="SO-203.26", evidence_ids=()):
    return extract_temporal_document_requirements(
        record=record or resolved_record(),
        document_reference=document_reference,
        requirement_prefix="SO-203.26",
        subject="container",
        evidence_ids=evidence_ids,
    )


def test_resolver_owned_context_overrides_adapter_context_before_extraction():
    record = resolved_record()
    assert record.provenance["tenant_id"] == "tenant-a"
    assert record.provenance["request_id"] == "request-203"
    assert record.provenance["correlation_id"] == "correlation-203"

    node = extract(record)[0]
    assert node.metadata["retrieval.tenant_id"] == "tenant-a"
    assert node.metadata["retrieval.request_id"] == "request-203"
    assert node.metadata["retrieval.correlation_id"] == "correlation-203"


def test_resolver_owned_capability_overrides_forged_adapter_assertions():
    record = resolved_record()
    # Raw temporal provenance may preserve adapter assertions for evidence, but
    # trusted resolver fields must overwrite the governed capability contract.
    assert record.provenance["required_capability"] == "source.github.read"
    assert record.provenance["authorization_scope"] == "read"
    assert record.provenance["source_kind"] == "GITHUB"

    node = extract(record)[0]
    assert node.metadata["retrieval.required_capability"] == "source.github.read"
    assert node.metadata["retrieval.authorization_scope"] == "read"
    assert node.metadata["retrieval.source_kind"] == "GITHUB"
    assert "retrieval.authority" not in node.metadata
    assert "retrieval.adapter_capability" not in node.metadata


def test_temporal_explicit_document_fact_stays_documented_not_inferred():
    nodes = extract(evidence_ids=("ev-doc-203",))
    claim = nodes[0].claims[0]
    assert claim.state is RequirementState.DOCUMENTED
    assert claim.state is not RequirementState.INFERRED
    assert claim.provenance.source_type is RequirementSourceType.DOCUMENT
    assert claim.provenance.source_reference == "SO-203.26#line:1"
    assert claim.provenance.evidence_ids == ("ev-doc-203",)


def test_bridge_preserves_selected_resolver_provenance_in_metadata():
    node = extract()[0]
    assert node.metadata["retrieval.record_id"] == "source-203"
    assert node.metadata["retrieval.source_id"] == "source-203"
    assert node.metadata["retrieval.reported_source_type"] == "GITHUB-REPORTED"
    assert node.metadata["retrieval.uri"] == "github://docs/SO-203.26"
    assert node.metadata["retrieval.required_capability"] == "source.github.read"
    assert node.metadata["retrieval.authorization_scope"] == "read"
    assert node.metadata["retrieval.conversation_id"] == "conversation-203"
    assert "provider_specific" not in node.metadata
    assert "retrieval.provider_specific" not in node.metadata


def test_bridge_does_not_treat_reported_source_type_as_document_authority():
    node = extract(document_reference="approved-document-ref")[0]
    assert node.claims[0].provenance.source_reference == "approved-document-ref#line:1"
    assert node.metadata["retrieval.reported_source_type"] == "GITHUB-REPORTED"
    assert node.metadata["retrieval.source_kind"] == "GITHUB"


def test_ambiguous_retrieved_prose_does_not_create_fact():
    record = resolved_record("O projeto deve considerar condições adequadas de uso.")
    assert extract(record) == ()


def test_bridge_fails_closed_for_blank_content():
    record = TemporalRecord(
        record_id="source-203",
        conversation_id="conversation-203",
        source_type="GITHUB",
        content="   ",
        provenance={"tenant_id": "tenant-a"},
        created_at="2026-10-19T00:00:00+00:00",
    )
    with pytest.raises(ValueError, match="content"):
        extract(record)


def test_bridge_fails_closed_for_missing_resolver_owned_context():
    record = TemporalRecord(
        record_id="source-203",
        conversation_id="conversation-203",
        source_type="GITHUB",
        content="Tipo: 40 HC",
        provenance={"uri": "github://docs/SO-203.26"},
        created_at="2026-10-19T00:00:00+00:00",
    )
    with pytest.raises(ValueError, match="resolver-owned temporal provenance missing"):
        extract(record)


def test_bridge_fails_closed_for_whitespace_only_resolver_context():
    record = resolved_record()
    provenance = dict(record.provenance)
    provenance["tenant_id"] = "   "
    poisoned = replace(record, provenance=provenance)
    with pytest.raises(ValueError, match="tenant_id"):
        extract(poisoned)


def test_bridge_requires_explicit_document_qualification():
    with pytest.raises(ValueError, match="document_reference"):
        extract(document_reference="")


def test_same_temporal_record_produces_stable_output():
    record = resolved_record("Tipo: 40 HC\nPiso: vinílico")
    assert extract(record) == extract(record)


def test_audit_contract_exposes_only_allowlisted_retrieval_provenance():
    node = extract(resolved_record("Piso: vinílico"), evidence_ids=("ev-floor",))[0]
    node = replace(
        node,
        metadata={
            **node.metadata,
            "private_reasoning": "must-not-leak",
            "credential": "must-not-leak",
        },
    )
    trace = audit_requirement(node)
    assert trace["source_claims"][0]["state"] == "DOCUMENTED"
    assert trace["evidence_ids"] == ("ev-floor",)
    assert trace["metadata"]["retrieval.source_id"] == "source-203"
    assert trace["metadata"]["retrieval.tenant_id"] == "tenant-a"
    assert trace["metadata"]["retrieval.request_id"] == "request-203"
    assert trace["metadata"]["retrieval.correlation_id"] == "correlation-203"
    assert trace["metadata"]["retrieval.required_capability"] == "source.github.read"
    assert "private_reasoning" not in trace["metadata"]
    assert "credential" not in trace["metadata"]
