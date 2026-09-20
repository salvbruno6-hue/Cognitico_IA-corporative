"""Candidate-only boundary for Hermes provider routing."""
from dataclasses import dataclass
from enum import Enum
from typing import Tuple
CAPABILITY_ID="EXT-ROUTE-HERMES"
class RoutingDisposition(str,Enum): OBSERVATION="OBSERVATION"; CANDIDATE="CANDIDATE"; REJECTED="REJECTED"
@dataclass(frozen=True)
class RoutingSignal:
    route_id:str; tenant_scope:str; source_refs:Tuple[str,...]; primary_provider:str; fallback_providers:Tuple[str,...]; credential_pool_strategy:str
    provenance_verified:bool=False; explicit_policy:bool=False; canonical_routing_authority:bool=False; governance_bypass:bool=False
@dataclass(frozen=True)
class RoutingAssessment:
    route_id:str; disposition:RoutingDisposition; evidence_refs:Tuple[str,...]; canonical_authority:bool=False; execution_permitted:bool=False; governance_bypass_permitted:bool=False
def assess_routing(s:RoutingSignal)->RoutingAssessment:
    if not s.route_id or not s.tenant_scope or not s.primary_provider or not s.source_refs or not s.provenance_verified: return RoutingAssessment(s.route_id,RoutingDisposition.REJECTED,tuple(s.source_refs))
    if s.canonical_routing_authority or s.governance_bypass: return RoutingAssessment(s.route_id,RoutingDisposition.REJECTED,tuple(s.source_refs))
    if not s.explicit_policy or not s.credential_pool_strategy: return RoutingAssessment(s.route_id,RoutingDisposition.OBSERVATION,tuple(s.source_refs))
    return RoutingAssessment(s.route_id,RoutingDisposition.CANDIDATE,tuple(s.source_refs))
