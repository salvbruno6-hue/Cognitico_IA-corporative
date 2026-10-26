"""Candidate-only external provider boundary derived from Hermes provider extraction.

This module does not load providers, execute tools, mutate routing, or transfer
authority. It classifies observed provider metadata against the existing ELO
External Capability Gateway so specialist providers can remain adapters rather
than becoming parallel Core owners.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any


@dataclass(frozen=True, slots=True)
class ProviderBoundaryDecision:
    provider_id: str
    owner: str
    classification: str
    admitted: bool
    reason: str
    canonical_mutation: bool = False


def classify_external_provider(metadata: Mapping[str, Any]) -> ProviderBoundaryDecision:
    """Classify a provider declaration without activating it.

    Fail closed when identity/owner/boundary metadata is incomplete. A provider
    explicitly declaring itself as Core or routing authority is rejected: an
    external provider may adapt the gateway, never become a parallel authority.
    """
    provider_id = str(metadata.get("provider_id") or "").strip()
    owner = str(metadata.get("owner") or "").strip()
    boundary = str(metadata.get("boundary") or "").strip().lower()
    authority = str(metadata.get("authority") or "").strip().lower()

    if not provider_id or not owner or not boundary:
        return ProviderBoundaryDecision(provider_id, owner, "candidate", False, "incomplete_provider_metadata")
    if authority in {"core", "router", "routing", "memory", "evolution_gate"}:
        return ProviderBoundaryDecision(provider_id, owner, "candidate", False, "parallel_authority_forbidden")
    if boundary not in {"adapter", "external_process", "plugin"}:
        return ProviderBoundaryDecision(provider_id, owner, "candidate", False, "unsupported_provider_boundary")
    if owner != "ELO External Capability Gateway":
        return ProviderBoundaryDecision(provider_id, owner, "candidate", False, "canonical_owner_mismatch")
    return ProviderBoundaryDecision(provider_id, owner, "adapter", True, "bounded_external_provider")


__all__ = ["ProviderBoundaryDecision", "classify_external_provider"]
