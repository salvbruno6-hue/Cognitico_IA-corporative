"""Candidate-only boundary for Hermes provider routing and fallback."""
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

CAPABILITY_ID = "EXT-ROUTE-HERMES"

class RoutingDisposition(str, Enum):
    OBSERVATION = "OBSERVATION"
    CANDIDATE = "CANDIDATE"
    REJECTED = "REJECTED"

@dataclass(frozen=True)
class RoutingSignal:
    route_id: str
    tenant_scope: str
    source_refs: Tuple[str, ...]
    primary_provider: str
    fallback_providers: Tuple[str, ...]
    credential_pool_strategy: str
    provenance_verified: bool = False
    explicit_policy: bool = False
    canonical_routing_authority: bool = False
    governance_bypass: bool = False

@dataclass(frozen=True)
class RoutingAssessment:
    route_id: str
    disposition: RoutingDisposition
    evidence_refs: Tuple[str, ...]
    canonical_authority: bool = False
    execution_permitted: bool = False
    governance_bypass_permitted: bool = False

def assess_routing(signal: RoutingSignal) -> RoutingAssessment:
    if not signal.route_id or not signal.tenant_scope or not signal.primary_provider:
        return RoutingAssessment(signal.route_id, RoutingDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.source_refs or not signal.provenance_verified:
        return RoutingAssessment(signal.route_id, RoutingDisposition.REJECTED, tuple(signal.source_refs))
    if signal.canonical_routing_authority or signal.governance_bypass:
        return RoutingAssessment(signal.route_id, RoutingDisposition.REJECTED, tuple(signal.source_refs))
    if not signal.explicit_policy or not signal.credential_pool_strategy:
        return RoutingAssessment(signal.route_id, RoutingDisposition.OBSERVATION, tuple(signal.source_refs))
    return RoutingAssessment(signal.route_id, RoutingDisposition.CANDIDATE, tuple(signal.source_refs))