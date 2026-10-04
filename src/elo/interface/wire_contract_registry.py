"""Versioned wire-contract evidence over the canonical ELO interface contracts.

This module does not create a transport, router, JSON-RPC endpoint, or authority.
It inventories the existing Pydantic interface models and produces deterministic
schema evidence for validation and downstream consumers.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .contracts import CognitiveRequest, CognitiveResponse, ErrorContract


REGISTRY_VERSION = "1.0.0"


@dataclass(frozen=True, slots=True)
class WireContractDescriptor:
    name: str
    version: str
    transport: str
    schema_digest: str


_CANONICAL_CONTRACTS = (
    CognitiveRequest,
    CognitiveResponse,
    ErrorContract,
)


def _schema_digest(model: type) -> str:
    schema = model.model_json_schema()
    payload = json.dumps(schema, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_wire_contract_registry() -> tuple[WireContractDescriptor, ...]:
    """Return deterministic descriptors for existing interface contracts."""
    return tuple(
        WireContractDescriptor(
            name=model.__name__,
            version=REGISTRY_VERSION,
            transport="HTTP/JSON",
            schema_digest=_schema_digest(model),
        )
        for model in _CANONICAL_CONTRACTS
    )


def validate_wire_contract_registry() -> tuple[WireContractDescriptor, ...]:
    """Validate uniqueness and deterministic schema evidence."""
    registry = build_wire_contract_registry()
    names = [item.name for item in registry]
    if len(names) != len(set(names)):
        raise ValueError("wire contract names must be unique")
    if not registry:
        raise ValueError("wire contract registry cannot be empty")
    if any(item.transport != "HTTP/JSON" for item in registry):
        raise ValueError("registry transport must match the existing interface")
    return registry


__all__ = [
    "REGISTRY_VERSION",
    "WireContractDescriptor",
    "build_wire_contract_registry",
    "validate_wire_contract_registry",
]
