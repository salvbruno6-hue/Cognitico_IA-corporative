from elo.agentic.elo_provider import ELOKnowledgeProvider, ELORequestContext


class _ResolverSpy:
    def __init__(self):
        self.resolve_calls = 0

    def resolve(self, *_args, **_kwargs):
        self.resolve_calls += 1
        return None


def test_agentic_provider_defaults_to_read_only_temporal_path():
    provider = ELOKnowledgeProvider()
    assert provider.allow_temporal_trace is False


def test_agentic_request_context_requires_explicit_runtime_identity():
    assert ELORequestContext(
        tenant_id="tenant",
        principal_id="principal",
        session_id="session",
        request_id="request",
        correlation_id="corr",
        conversation_id="conv",
        authorization_scope="read",
    ).authorization_scope == "read"
