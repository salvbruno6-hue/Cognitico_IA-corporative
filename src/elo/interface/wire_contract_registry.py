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

# Governed baseline captured from the canonical contracts on main at the point
# this refinement is introduced. A future contract change must deliberately
# update this baseline after compatibility review; otherwise CI surfaces drift.
GOVERNED_SCHEMA_BASELINE: dict[str, str] = {
    "CognitiveRequest": "732711824e722bc713e6cedb353a1c3b0097765df8fb75bb339703a201908ad4",
    "CognitiveResponse": "7a5a9b7d849964af33196de4e402aafd78a4105e9ef5f672c0f43a9bca0e8b5b",
    "ErrorContract": "b1f205c88623b32e992b5d7c0687233faf4af0b591fa88010f79221e4135435e",
}


@dataclass(frozen=True, slots=True)
class WireContractDescriptor:
    name: str
    version: str
    transport: str
    schema_digest: str


@dataclass(frozen=True, slots=True)
class WireContractCompatibility:
    compatible: bool
    changed_contracts: tuple[str, ...]
    missing_contracts: tuple[str, ...]
    unexpected_contracts: tuple[str, ...]


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


def compare_to_governed_baseline() -> WireContractCompatibility:
    """Compare current public schemas with the reviewed canonical baseline."""
    current = {item.name: item.schema_digest for item in validate_wire_contract_registry()}
    expected_names = set(GOVERNED_SCHEMA_BASELINE)
    current_names = set(current)
    changed = tuple(sorted(
        name for name in expected_names & current_names
        if current[name] != GOVERNED_SCHEMA_BASELINE[name]
    ))
    missing = tuple(sorted(expected_names - current_names))
    unexpected = tuple(sorted(current_names - expected_names))
    return WireContractCompatibility(
        compatible=not changed and not missing and not unexpected,
        changed_contracts=changed,
        missing_contracts=missing,
        unexpected_contracts=unexpected,
    )


def compatibility_fingerprint() -> str:
    """Return one deterministic fingerprint for the complete public contract set."""
    payload = json.dumps(
        [
            {
                "name": item.name,
                "version": item.version,
                "transport": item.transport,
                "schema_digest": item.schema_digest,
            }
            for item in validate_wire_contract_registry()
        ],
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


__all__ = [
    "GOVERNED_SCHEMA_BASELINE",
    "REGISTRY_VERSION",
    "TRANSPORT",
    "WireContractCompatibility",
    "WireContractDescriptor",
    "build_wire_contract_registry",
    "compare_to_governed_baseline",
    "compatibility_fingerprint",
    "validate_wire_contract_registry",
]
