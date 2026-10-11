"""Versioned evidence over the canonical ELO interface contracts.

This module inventories existing interface contracts. It does not create a new
transport, router, endpoint, authorization authority, or execution path.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .contracts import CognitiveRequest, CognitiveResponse, ErrorContract


REGISTRY_VERSION = "1.0.0"
TRANSPORT = "HTTP/JSON"


@dataclass(frozen=True, slots=True)
class WireContractDescriptor:
    name: str
    version: str
    transport: str
    schema_digest: str


_CANONICAL_CONTRACTS = (CognitiveRequest, CognitiveResponse, ErrorContract)


def _schema_digest(model: type) -> str:
    payload = json.dumps(
        model.model_json_schema(), sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_wire_contract_registry() -> tuple[WireContractDescriptor, ...]:
    return tuple(
        WireContractDescriptor(
            name=model.__name__,
            version=REGISTRY_VERSION,
            transport=TRANSPORT,
            schema_digest=_schema_digest(model),
        )
        for model in _CANONICAL_CONTRACTS
    )


def validate_wire_contract_registry() -> tuple[WireContractDescriptor, ...]:
    registry = build_wire_contract_registry()
    names = tuple(item.name for item in registry)
    if not registry:
        raise ValueError("wire contract registry cannot be empty")
    if len(names) != len(set(names)):
        raise ValueError("wire contract names must be unique")
    if any(item.transport != TRANSPORT for item in registry):
        raise ValueError("wire contract transport must remain canonical")
    if any(len(item.schema_digest) != 64 for item in registry):
        raise ValueError("wire contract schema digest must be sha256")
    return registry


def compatibility_fingerprint() -> str:
    """Return one deterministic fingerprint for the complete public contract set."""
    payload = json.dumps(
        [item.__dict__ if hasattr(item, "__dict__") else {
            "name": item.name,
            "version": item.version,
            "transport": item.transport,
            "schema_digest": item.schema_digest,
        } for item in validate_wire_contract_registry()],
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


__all__ = [
    "REGISTRY_VERSION",
    "TRANSPORT",
    "WireContractDescriptor",
    "build_wire_contract_registry",
    "compatibility_fingerprint",
    "validate_wire_contract_registry",
]
