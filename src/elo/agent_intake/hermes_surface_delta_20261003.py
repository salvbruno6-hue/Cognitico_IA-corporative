"""Candidate-only registry for the current Hermes surface delta.

This module records externally observed Hermes mechanisms and maps each one to an
existing ELO owner. It does not connect to Hermes, execute tools, mutate state,
authorize promotion, or create a new authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

@dataclass(frozen=True, slots=True)
class HermesSurfaceDelta:
    mechanism_id: str
    observed_capability: str
    elo_owner: str
    candidate_introduction: str
    dependencies: tuple[str, ...]
    relations: tuple[str, ...]
    validation_boundary: str
    candidate_only: bool = True
    canonical_mutation: bool = False
    business_operation: bool = False

SURFACE_DELTAS: tuple[HermesSurfaceDelta, ...] = (
    HermesSurfaceDelta(
        "HERMES-WEBHOOK-GUARD",
        "HMAC-authenticated event routes, filters, idempotency, rate limits and constrained per-route toolsets",
        "ELO Workflow/Automation",
        "introduce authenticated event intake as a bounded trigger contract; authentication never makes payload business content trusted",
        ("webhook adapter", "existing workflow runtime"),
        ("EXT-HOOK-HERMES", "EXT-CRON-HERMES", "ExecutionBoundary"),
        "controlled contract validation only",
    ),
    HermesSurfaceDelta(
        "HERMES-TOOL-LOOP-GUARD",
        "warnings and hard stops for repeated failed or non-progressing tool calls, stricter for unattended execution",
        "ELO Model/Tool Routing",
        "introduce non-progress detection as an execution-safety signal without changing the canonical decision authority",
        ("tool middleware", "session mode"),
        ("EXT-TOOL-SEARCH-HERMES", "ExecutionBoundary"),
        "deterministic policy evaluation",
    ),
    HermesSurfaceDelta(
        "HERMES-CODE-KERNEL",
        "session-scoped execute_code kernels with idle/LRU limits and per-cell RPC authority rebinding",
        "ELO Model/Tool Routing",
        "introduce bounded stateful programmatic execution as an observable runtime contract",
        ("execute_code", "sandbox RPC"),
        ("EXT-CODE-EXEC-HERMES", "ExecutionBoundary"),
        "controlled metadata and invariant validation",
    ),
    HermesSurfaceDelta(
        "HERMES-MCP-DYNAMIC",
        "runtime tools/list_changed re-registration with lock protection",
        "ELO External Capability Gateway",
        "introduce capability-catalog change detection without treating newly exposed tools as authorized",
        ("MCP registry", "tool registry"),
        ("EXT-MCP-HERMES", "EXT-TOOL-SEARCH-HERMES"),
        "controlled discovery-state validation",
    ),
    HermesSurfaceDelta(
        "HERMES-MCP-SAMPLING",
        "MCP servers may request bounded LLM sampling with model allowlists, token/time/rate/tool-round caps",
        "ELO External Capability Gateway",
        "introduce delegated inference as a constrained external request, preserving ELO authorization and provenance",
        ("MCP sampling handler", "rate limiter"),
        ("EXT-MCP-HERMES", "ExecutionBoundary", "ELO Model/Tool Routing"),
        "policy-bound contract validation",
    ),
    HermesSurfaceDelta(
        "HERMES-DELEGATION-CONTROLS",
        "bounded child concurrency, depth controls, isolated contexts and heartbeat propagation",
        "ELO Agent Delegation",
        "refine delegated execution with explicit concurrency/depth/continuity metadata",
        ("delegate_task", "AgentOrchestrator"),
        ("EXT-MULTIAGENT-HERMES", "EXT-PROFILE-HERMES"),
        "controlled delegation-contract validation",
    ),
    HermesSurfaceDelta(
        "HERMES-WEBHOOK-COALESCE",
        "event coalescing with quiet windows, maximum wait, delivery-id idempotency and at-most-once scheduler claims",
        "ELO Workflow/Automation",
        "introduce event burst compression as a derived scheduling signal, never as a business fact",
        ("webhook adapter", "cron runtime"),
        ("EXT-HOOK-HERMES", "EXT-CRON-HERMES"),
        "deterministic event-grouping validation",
    ),
    HermesSurfaceDelta(
        "HERMES-SKILL-LIFECYCLE",
        "skill search, update checks, custom sources and configuration snapshots",
        "ELO Knowledge & Skills",
        "introduce skill-source provenance and lifecycle metadata before any governed skill admission",
        ("skills registry", "skill manager"),
        ("EXT-LEARN-HERMES", "ELO Learning Governance"),
        "candidate metadata validation",
    ),
    HermesSurfaceDelta(
        "HERMES-SESSION-LINEAGE",
        "session titles/lineage, export/resume and full-text historical session search",
        "ELO Context",
        "introduce session lineage as context provenance rather than learning or canonical memory",
        ("session store", "session_search"),
        ("EXT-CONTEXTREF-HERMES", "ELO Memory"),
        "provenance-only validation",
    ),
    HermesSurfaceDelta(
        "HERMES-PROFILE-ISOLATION",
        "profiles isolate configuration, credentials, memory, sessions, skills and cron jobs",
        "ELO Agent Context & Delegation",
        "refine profile scope metadata and isolation checks without transferring authority",
        ("profile manager", "agent runtime"),
        ("EXT-PROFILE-HERMES", "EXT-MULTIAGENT-HERMES"),
        "tenant/profile invariant validation",
    ),
)

def get_surface_delta(mechanism_id: str) -> HermesSurfaceDelta:
    for item in SURFACE_DELTAS:
        if item.mechanism_id == mechanism_id:
            return item
    raise KeyError(mechanism_id)

def validate_registry() -> Mapping[str, int]:
    ids = [item.mechanism_id for item in SURFACE_DELTAS]
    assert len(ids) == len(set(ids))
    assert all(item.candidate_only for item in SURFACE_DELTAS)
    assert all(not item.canonical_mutation for item in SURFACE_DELTAS)
    assert all(not item.business_operation for item in SURFACE_DELTAS)
    assert all(item.elo_owner and item.candidate_introduction for item in SURFACE_DELTAS)
    return {"mechanisms": len(SURFACE_DELTAS), "candidate_only": len(SURFACE_DELTAS)}

__all__ = ["HermesSurfaceDelta", "SURFACE_DELTAS", "get_surface_delta", "validate_registry"]
