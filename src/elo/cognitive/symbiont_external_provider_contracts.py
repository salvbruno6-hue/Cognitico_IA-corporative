"""ELO-owned contracts for governed external capability providers.

The Symbiont is provider-neutral: OpenAI, Hermes, GitHub, Supabase, MCP servers
and future providers are capability implementations, not authorities. These
contracts describe discovery, authorization boundaries and evidence requirements
without storing credentials or mutating canonical ELO state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any, Mapping

CONTRACT_VERSION = "1.0"


class ProviderProtocol(StrEnum):
    API = "api"
    MCP = "mcp"
    SDK = "sdk"
    LOCAL_RUNTIME = "local_runtime"


class ProviderStatus(StrEnum):
    NOT_PROVISIONED = "NOT_PROVISIONED"
    AVAILABLE = "AVAILABLE"
    CONNECTED = "CONNECTED"
    BLOCKED = "BLOCKED"


class EvolutionDisposition(StrEnum):
    REUSE = "REUSE"
    ADAPT = "ADAPT"
    LAB_CANDIDATE = "LAB_CANDIDATE"
    BLOCK = "BLOCK"


_FORBIDDEN_KEYS = frozenset(
    {
        "api_key",
        "authorization",
        "client_secret",
        "database_url",
        "private_key",
        "service_role_key",
        "token",
    }
)


def _required(value: str, name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{name} is required")


def _reject_secrets(value: Any, path: str) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in _FORBIDDEN_KEYS:
                raise ValueError(f"credential/secret field is not allowed: {path}.{key}")
            _reject_secrets(child, f"{path}.{key}")
    elif isinstance(value, (tuple, list)):
        for index, child in enumerate(value):
            _reject_secrets(child, f"{path}[{index}]")


@dataclass(frozen=True)
class ExternalProviderContract:
    """ELO-owned identity and boundary contract for one external provider."""

    provider_id: str
    provider: str
    capability: str
    protocol: ProviderProtocol
    status: ProviderStatus
    purpose: str
    source_ref: str
    tenant_id: str
    domain: str
    read_allowed: bool = True
    write_allowed: bool = False
    execution_allowed: bool = False
    canonical_mutation_allowed: bool = False
    evidence_required: bool = True
    provenance_required: bool = True
    evolution_gate_required: bool = True
    cost_model: str = "unknown"
    rate_limit: str = "unknown"
    fallback_provider_id: str | None = None
    contract_version: str = CONTRACT_VERSION
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for value, name in (
            (self.provider_id, "provider_id"),
            (self.provider, "provider"),
            (self.capability, "capability"),
            (self.purpose, "purpose"),
            (self.source_ref, "source_ref"),
            (self.tenant_id, "tenant_id"),
            (self.domain, "domain"),
        ):
            _required(value, name)
        if self.contract_version != CONTRACT_VERSION:
            raise ValueError(f"unsupported contract_version: {self.contract_version}")
        if not self.evidence_required or not self.provenance_required or not self.evolution_gate_required:
            raise ValueError("external provider governance controls cannot be disabled")
        if self.canonical_mutation_allowed:
            raise ValueError("external providers cannot mutate canonical ELO state")
        _reject_secrets(self.metadata, "metadata")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExternalCapabilityProbe:
    """Bounded, evidence-bearing test of a provider capability."""

    probe_id: str
    provider_id: str
    capability: str
    request_id: str
    tenant_id: str
    objective: str
    input_payload: Mapping[str, Any]
    success_criteria: tuple[str, ...]
    evidence_requirements: tuple[str, ...]
    read_only: bool = True
    bounded: bool = True
    max_calls: int = 1
    contract_version: str = CONTRACT_VERSION

    def __post_init__(self) -> None:
        for value, name in (
            (self.probe_id, "probe_id"),
            (self.provider_id, "provider_id"),
            (self.capability, "capability"),
            (self.request_id, "request_id"),
            (self.tenant_id, "tenant_id"),
            (self.objective, "objective"),
        ):
            _required(value, name)
        if not self.success_criteria or not self.evidence_requirements:
            raise ValueError("probe requires success criteria and evidence requirements")
        if not self.read_only or not self.bounded:
            raise ValueError("default external provider probe must be read-only and bounded")
        if self.max_calls < 1:
            raise ValueError("max_calls must be positive")
        if self.contract_version != CONTRACT_VERSION:
            raise ValueError(f"unsupported contract_version: {self.contract_version}")
        _reject_secrets(self.input_payload, "input_payload")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExternalCapabilityOutcome:
    """Observed outcome; descriptive only and never a promotion command."""

    probe_id: str
    provider_id: str
    request_id: str
    tenant_id: str
    success: bool
    evidence_ids: tuple[str, ...]
    outcome: Mapping[str, Any]
    disposition: EvolutionDisposition = EvolutionDisposition.LAB_CANDIDATE
    candidate_only: bool = True
    contract_version: str = CONTRACT_VERSION

    def __post_init__(self) -> None:
        for value, name in (
            (self.probe_id, "probe_id"),
            (self.provider_id, "provider_id"),
            (self.request_id, "request_id"),
            (self.tenant_id, "tenant_id"),
        ):
            _required(value, name)
        if not self.evidence_ids:
            raise ValueError("external capability outcome requires evidence")
        if not self.outcome:
            raise ValueError("external capability outcome requires outcome")
        if not self.candidate_only:
            raise ValueError("external capability outcomes cannot be directly promoted")
        if self.contract_version != CONTRACT_VERSION:
            raise ValueError(f"unsupported contract_version: {self.contract_version}")
        _reject_secrets(self.outcome, "outcome")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
