from elo.adapters.source_adapters import (
    AIProviderSourceAdapter,
    ChatGPTProjectSourceAdapter,
    DocumentSourceAdapter,
    GitHubSourceAdapter,
    WebSourceAdapter,
)
from elo.core.source_discovery import SourceCandidate
from elo.core.source_resolver import RetrievedSource, SourceResolutionRequest, SourceResolver


def request(scope: str) -> SourceResolutionRequest:
    return SourceResolutionRequest(
        query="budget quotation",
        tenant_id="tenant-a",
        domain="BUDGET",
        principal_id="analyst-1",
        session_id="session-1",
        request_id="request-1",
        correlation_id="corr-1",
        conversation_id="conversation-1",
        authorization_scope=scope,
    )


def source() -> RetrievedSource:
    return RetrievedSource(
        source_id="source-1",
        source_type="external",
        content="verified source material",
        provenance={"provider": "test"},
    )


def candidate(kind: str, capability: str) -> SourceCandidate:
    return SourceCandidate(
        kind=kind,
        reason="authorized retrieval",
        priority=1,
        query="budget quotation",
        required_capability=capability,
    )


def test_github_adapter_is_concrete_and_preserves_external_authority_boundary():
    adapter = GitHubSourceAdapter(lambda _candidate, _request: (source(),))
    result = SourceResolver((adapter,)).resolve(
        candidate("GITHUB", "source.github.read"),
        request("source:github:read"),
    )
    assert result.status == "RETRIEVED_TO_TEMPORAL"
    assert result.retrieved[0].provenance["adapter_kind"] == "GITHUB"
    assert result.retrieved[0].provenance["authority"] == "external_source_evidence"


def test_all_supported_provider_boundaries_are_explicit_and_pluggable():
    adapters = (
        ChatGPTProjectSourceAdapter(lambda _c, _r: (source(),)),
        DocumentSourceAdapter(lambda _c, _r: (source(),)),
        WebSourceAdapter(lambda _c, _r: (source(),)),
        AIProviderSourceAdapter(lambda _c, _r: (source(),)),
    )
    expected = (
        ("CHATGPT_PROJECTS", "source.chatgpt_projects.read", "source:chatgpt_projects:read"),
        ("DOCUMENTS", "source.documents.read", "source:documents:read"),
        ("WEB", "source.web.read", "source:web:read"),
        ("AI_PROVIDER", "source.ai_provider.read", "source:ai_provider:read"),
    )
    for adapter, (kind, capability, scope) in zip(adapters, expected):
        result = SourceResolver((adapter,)).resolve(candidate(kind, capability), request(scope))
        assert result.status == "RETRIEVED_TO_TEMPORAL"
        assert result.temporal_records[0].provenance["tenant_id"] == "tenant-a"


def test_adapter_rejects_wrong_authorization_scope_before_fetch():
    called = False

    def fetch(_candidate, _request):
        nonlocal called
        called = True
        return (source(),)

    adapter = GitHubSourceAdapter(fetch)
    try:
        adapter.retrieve(candidate("GITHUB", "source.github.read"), request("source:web:read"))
    except PermissionError:
        pass
    else:
        raise AssertionError("wrong authorization scope must be rejected")
    assert called is False


def test_unavailable_adapter_is_explicit_and_does_not_invent_evidence():
    adapter = WebSourceAdapter(lambda _c, _r: (source(),), available_state=False)
    result = SourceResolver((adapter,)).resolve(
        candidate("WEB", "source.web.read"),
        request("source:web:read"),
    )
    assert result.status == "UNAVAILABLE"
    assert result.retrieved == ()
    assert result.temporal_records == ()


def test_provider_result_is_not_canonical_truth():
    adapter = AIProviderSourceAdapter(lambda _c, _r: (source(),))
    result = SourceResolver((adapter,)).resolve(
        candidate("AI_PROVIDER", "source.ai_provider.read"),
        request("source:ai_provider:read"),
    )
    assert result.retrieved[0].provenance["authority"] == "external_source_evidence"
    assert result.temporal_records[0].provenance["authority"] == "external_source_evidence"


def test_temporal_admission_preserves_request_and_correlation_context():
    adapter = DocumentSourceAdapter(lambda _c, _r: (source(),))
    result = SourceResolver((adapter,)).resolve(
        candidate("DOCUMENTS", "source.documents.read"),
        request("source:documents:read"),
    )
    record = result.temporal_records[0]
    assert record.provenance["request_id"] == "request-1"
    assert record.provenance["correlation_id"] == "corr-1"
    assert record.provenance["principal_id"] == "analyst-1"
