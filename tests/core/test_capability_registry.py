import pytest

from elo.core.capability_registry import CapabilityProbe, CapabilityRegistry, CapabilityStatus


def test_capability_discovery_reports_available_and_unavailable_without_making_them_dependencies():
    registry = CapabilityRegistry(
        (
            CapabilityProbe("local_ai", "ollama", "0.1", lambda: True),
            CapabilityProbe("cli", "codex", "1.0", lambda: False),
        )
    )
    snapshot = {item.name: item for item in registry.snapshot()}
    assert snapshot["ollama"].status == CapabilityStatus.AVAILABLE
    assert snapshot["codex"].status == CapabilityStatus.UNAVAILABLE
    assert tuple(item.name for item in registry.get_available()) == ("ollama",)


def test_unknown_capability_is_not_claimed_available_without_health_evidence():
    registry = CapabilityRegistry((CapabilityProbe("local_ai", "ollama"),))
    assert registry.snapshot()[0].status == CapabilityStatus.UNKNOWN
    assert registry.get_available() == ()


def test_failed_probe_degrades_to_unavailable():
    def broken():
        raise RuntimeError("provider failure")

    registry = CapabilityRegistry((CapabilityProbe("provider", "remote-ai", health_check=broken),))
    assert registry.snapshot()[0].status == CapabilityStatus.UNAVAILABLE


def test_secret_metadata_is_rejected_and_non_secret_metadata_is_preserved():
    assert CapabilityRegistry.safe_metadata({"location": "local", "transport": "cli"})["location"] == "local"
    with pytest.raises(ValueError):
        CapabilityRegistry.safe_metadata({"api_key": "never-store-this"})
    with pytest.raises(ValueError):
        CapabilityRegistry.safe_metadata({"OPENAI_API_KEY": "never-store-this"})
    with pytest.raises(ValueError):
        CapabilityProbe("provider", "remote-ai", metadata={"access_token": "never-store-this"})
