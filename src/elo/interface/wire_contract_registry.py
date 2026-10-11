"""Versioned wire-contract evidence over the canonical ELO interface contracts.

Observational only: this module does not create a transport, router, endpoint,
authorization path, execution authority, memory owner, or learning authority.
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
    canonical_owner: str = "elo.interface.contracts"
    execution_permitted: bool = False


_CANONICAL_CONTRACTS = (CognitiveRequest, CognitiveResponse, ErrorContract)


def _schema_digest(model: type) -> str:
    payload = json.dumps(
        model.model_json_schema(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
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
    if not registry:
        raise ValueError("wire contract registry cannot be empty")
    names = [item.name for item in registry]
    if len(names) != len(set(names)):
        raise ValueError("wire contract names must be unique")
    if any(item.transport != TRANSPORT for item in registry):
        raise ValueError("registry transport must match the existing interface")
    if any(item.execution_permitted for item in registry):
        raise ValueError("wire contract evidence cannot authorize execution")
    return registry


__all__ = [
    "REGISTRY_VERSION",
    "TRANSPORT",
    "WireContractDescriptor",
    "build_wire_contract_registry",
    "validate_wire_contract_registry",
]
