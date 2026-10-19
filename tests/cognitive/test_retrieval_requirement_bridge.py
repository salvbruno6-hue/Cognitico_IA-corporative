import pytest

from elo.core.source_resolver import RetrievedSource
from elo.cognitive.reasoning.document_extraction import (
    extract_retrieved_document_requirements,
)
from elo.cognitive.reasoning.requirement_analysis import (
    RequirementSourceType,
    RequirementState,
    audit_requirement,
)


def retrieved(*, content="Tipo: 40 HC", provenance=None):
    return RetrievedSource(
        source_id="source-203",
        source_type="GITHUB",
        content=content,
        provenance=provenance
        or {
            "uri": "github://docs/SO-203.26",
            "authority": "external_source_evidence",
            "adapter_capability": "source.github.read",
            "tenant_id": "tenant-a",
            "domain": "orcamento",
            "principal_id": "principal-a",
            "session_id": "session-a",
            "request_id": "request-203",
            "correlation_id": "correlation-203",
        },
        metadata={"provider_specific": "must-not-be-copied"},
    )


def test_retrieved_explicit_document_fact_stays_documented_not_inferred():
    nodes = extract_retrieved_document_requirements(
        retrieved=retrieved(),
        document_reference="SO-203.26",
        requirement_prefix="SO-203.26",
        subject="container",
        evidence_ids=("ev-doc-203",),
    )

    claim = nodes[0].claims[0]
    assert claim.state is RequirementState.DOCUMENTED
    assert claim.state is not RequirementState.INFERRED
    assert claim.provenance.source_type is RequirementSourceType.DOCUMENT
    assert claim.provenance.source_reference == "SO-203.26#line:1"
    assert claim.provenance.evidence_ids == ("ev-doc-203",)


def test_bridge_preserves_selected_retrieval_provenance_in_metadata():
    node = extract_retrieved_document_requirements(
        retrieved=retrieved(),
        document_reference="SO-203.26",
        requirement_prefix="SO-203.26",
        subject="container",
    )[0]

    assert node.metadata["retrieval.source_id"] == "source-203"
    assert node.metadata["retrieval.source_type"] == "GITHUB"
    assert node.metadata["retrieval.uri"] == "github://docs/SO-203.26"
    assert node.metadata["retrieval.authority"] == "external_source_evidence"
    assert node.metadata["retrieval.adapter_capability"] == "source.github.read"
    assert node.metadata["retrieval.request_id"] == "request-203"
    assert node.metadata["retrieval.correlation_id"] == "correlation-203"
    assert "provider_specific" not in node.metadata
    assert "retrieval.provider_specific" not in node.metadata


def test_bridge_does_not_treat_source_type_as_document_authority():
    node = extract_retrieved_document_requirements(
        retrieved=retrieved(),
        document_reference="approved-document-ref",
        requirement_prefix="REQ",
        subject="container",
    )[0]

    assert node.claims[0].provenance.source_reference == "approved-document-ref#line:1"
    assert node.metadata["retrieval.source_type"] == "GITHUB"


def test_ambiguous_retrieved_prose_does_not_create_fact():
    nodes = extract_retrieved_document_requirements(
        retrieved=retrieved(content="O projeto deve considerar condições adequadas de uso."),
        document_reference="SO-203.26",
        requirement_prefix="SO-203.26",
        subject="container",
    )
    assert nodes == ()


def test_bridge_fails_closed_for_blank_content():
    with pytest.raises(ValueError, match="content"):
        extract_retrieved_document_requirements(
            retrieved=retrieved(content="   "),
            document_reference="SO-203.26",
            requirement_prefix="SO-203.26",
            subject="container",
        )


def test_bridge_fails_closed_for_missing_provenance():
    source = RetrievedSource(
        source_id="source-203",
        source_type="GITHUB",
        content="Tipo: 40 HC",
        provenance={},
    )
    with pytest.raises(ValueError, match="provenance"):
        extract_retrieved_document_requirements(
            retrieved=source,
            document_reference="SO-203.26",
            requirement_prefix="SO-203.26",
            subject="container",
        )


def test_bridge_requires_explicit_document_qualification():
    with pytest.raises(ValueError, match="document_reference"):
        extract_retrieved_document_requirements(
            retrieved=retrieved(),
            document_reference="",
            requirement_prefix="SO-203.26",
            subject="container",
        )


def test_same_retrieval_produces_stable_output():
    kwargs = dict(
        retrieved=retrieved(content="Tipo: 40 HC\nPiso: vinílico"),
        document_reference="SO-203.26",
        requirement_prefix="SO-203.26",
        subject="container",
    )
    assert extract_retrieved_document_requirements(**kwargs) == extract_retrieved_document_requirements(**kwargs)


def test_existing_audit_contract_remains_compatible():
    node = extract_retrieved_document_requirements(
        retrieved=retrieved(content="Piso: vinílico"),
        document_reference="SO-203.26",
        requirement_prefix="SO-203.26",
        subject="container",
        evidence_ids=("ev-floor",),
    )[0]

    trace = audit_requirement(node)
    assert trace["source_claims"][0]["state"] == "DOCUMENTED"
    assert trace["evidence_ids"] == ("ev-floor",)
