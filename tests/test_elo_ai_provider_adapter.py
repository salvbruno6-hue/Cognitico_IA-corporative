import pytest

from src.elo.integrations.ai_provider import AIRequest, OpenAIProvider


def test_openai_adapter_requires_environment_secret(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        OpenAIProvider()


def test_openai_adapter_accepts_environment_secret(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    provider = OpenAIProvider()
    assert provider.provider_id == "openai"


def test_request_keeps_governed_specialist_context():
    request = AIRequest(
        request_id="req-1",
        tenant_id="tenant-1",
        specialist_id="budgeting",
        provider="openai",
        model="gpt-5.4-mini",
        instructions="Construir orçamento conforme critérios do ELO.",
        context="Lista-Mãe e evidências versionadas.",
    )
    assert request.tenant_id == "tenant-1"
    assert request.specialist_id == "budgeting"
    assert "evidências" in request.context


def test_adapter_does_not_accept_another_provider():
    provider = OpenAIProvider(api_key="test-key")
    request = AIRequest(
        request_id="req-2",
        tenant_id="tenant-1",
        specialist_id="budgeting",
        provider="other-provider",
        model="model-x",
        instructions="x",
    )
    with pytest.raises(ValueError):
        provider.generate(request)
