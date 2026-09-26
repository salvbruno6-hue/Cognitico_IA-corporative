"""Bounded provider-routing plan adapter.

Materializes a policy-validated routing plan without selecting a live provider,
accessing credentials, executing a request, or changing routing authority.
"""
from __future__ import annotations

from dataclasses import dataclass

from .hermes_routing_boundary import RoutingDisposition, RoutingSignal, assess_routing


@dataclass(frozen=True, slots=True)
class RoutingPlanContract:
    route_id: str
    tenant_scope: str
    primary_provider: str
    fallback_providers: tuple[str, ...]
    credential_pool_strategy: str
    source_refs: tuple[str, ...]
    disposition: RoutingDisposition
    execution_permitted: bool = False
    canonical_authority: bool = False
    governance_bypass_permitted: bool = False


class RoutingAdapter:
    def adapt(self, signal: RoutingSignal) -> RoutingPlanContract | None:
        assessment = assess_routing(signal)
        if assessment.disposition is not RoutingDisposition.CANDIDATE:
            return None
        return RoutingPlanContract(
            route_id=signal.route_id,
            tenant_scope=signal.tenant_scope,
            primary_provider=signal.primary_provider,
            fallback_providers=signal.fallback_providers,
            credential_pool_strategy=signal.credential_pool_strategy,
            source_refs=assessment.evidence_refs,
            disposition=assessment.disposition,
        )


def adapt_routing(signal: RoutingSignal) -> RoutingPlanContract | None:
    return RoutingAdapter().adapt(signal)


__all__ = ["RoutingAdapter", "RoutingPlanContract", "adapt_routing"]
