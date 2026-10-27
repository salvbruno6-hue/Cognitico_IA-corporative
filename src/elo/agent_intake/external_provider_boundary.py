"""Candidate-only external provider boundary derived from Hermes provider extraction.

This module does not load providers, execute tools, mutate routing, or transfer
authority. It classifies observed provider metadata against the existing ELO
External Capability Gateway so specialist providers can remain adapters rather
than becoming parallel Core owners.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ProviderBoundaryDecision:
    provider_id: str
    owner: str
    classification: str
    admitted: bool
    reason: str
    canonical_mutation: bool = False


def _nonempty_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None


def classify_external_provider(metadata: Mapping[str, Any]) -> ProviderBoundaryDecision:
    """Classify a provider declaration without activating it.

    Fail closed unless identity, owner, boundary and authority are explicit
    strings from the bounded adapter vocabulary. External providers may adapt
    the existing gateway; they never become parallel Core authorities.
    """
    provider_id = _nonempty_string(metadata.get("provider_id"))
    owner = _nonempty_string(metadata.get("owner"))
    boundary_raw = _nonempty_string(metadata.get("boundary"))
    authority_raw = _nonempty_string(metadata.get("authority"))

    display_provider_id = provider_id or ""
    display_owner = owner or ""
    if provider_id is None or owner is None or boundary_raw is None or authority_raw is None:
        return ProviderBoundaryDecision(
            display_provider_id,
            display_owner,
            "candidate",
            False,
            "incomplete_or_malformed_provider_metadata",
        )

    boundary = boundary_raw.lower()
    authority = authority_raw.lower()
    if authority in {"core", "router", "routing", "memory", "evolution_gate"}:
        return ProviderBoundaryDecision(provider_id, owner, "candidate", False, "parallel_authority_forbidden")
    if authority not in {"execution_adapter"}:
        return ProviderBoundaryDecision(provider_id, owner, "candidate", False, "unsupported_provider_authority")
    if boundary not in {"adapter", "external_process", "plugin"}:
        return ProviderBoundaryDecision(provider_id, owner, "candidate", False, "unsupported_provider_boundary")
    if owner != "ELO External Capability Gateway":
        return ProviderBoundaryDecision(provider_id, owner, "candidate", False, "canonical_owner_mismatch")
    return ProviderBoundaryDecision(provider_id, owner, "adapter", True, "bounded_external_provider")


__all__ = ["ProviderBoundaryDecision", "classify_external_provider"]
