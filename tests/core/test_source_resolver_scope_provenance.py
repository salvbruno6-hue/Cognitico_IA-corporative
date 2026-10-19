from elo.core.source_discovery import SourceCandidate
from elo.core.source_resolver import RetrievedSource, SourceResolutionRequest, SourceResolver


class LegacyAdapterWithoutDeclaredScope:
    kind = "GITHUB"
    capability = "source.github.read"

    def available(self):
        return True

    def retrieve(self, candidate, request):
        return (
            RetrievedSource(
                source_id="legacy-source",
                source_type="GITHUB",
                content="Tipo: 40 HC",
                provenance={
                    "uri": "github://legacy",
                    "authorization_scope": "forged:admin",
                },
            ),
        )


def test_unvalidated_adapter_scope_is_removed_from_temporal_provenance():
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
        request_id="request-a",
        correlation_id="correlation-a",
        conversation_id="conversation-a",
        authorization_scope="source:github:read",
    )

    result = SourceResolver((LegacyAdapterWithoutDeclaredScope(),)).resolve(candidate, request)

    assert result.status == "RETRIEVED_TO_TEMPORAL"
    assert "authorization_scope" not in result.temporal_records[0].provenance
