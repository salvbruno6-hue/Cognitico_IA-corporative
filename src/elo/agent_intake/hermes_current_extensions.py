"""Candidate-only adaptations from currently documented Hermes mechanisms.

This registry is descriptive and deterministic. It does not execute Hermes,
change canonical ELO state, or promote a candidate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


CANDIDATES: tuple[tuple[str, str, str, str], ...] = (
    ("EXT-CONTEXTREF-HERMES", "context references", "ELO Context", "provenance-bounded reference resolution"),
    ("EXT-CHECKPOINT-HERMES", "checkpoints", "ELO State Recovery", "pre-mutation checkpoint contract"),
    ("EXT-HOOK-HERMES", "event hooks", "ELO Workflow/Automation", "lifecycle evidence and guardrail hooks"),
    ("EXT-ROUTE-HERMES", "provider routing/fallback/credential pools", "ELO Model/Tool Routing", "policy-based bounded failover"),
    ("EXT-PROFILE-HERMES", "profiles/Bot Mode", "ELO Agent Context & Delegation", "isolated agent-context profiles"),
    ("EXT-BATCH-HERMES", "batch processing", "ELO Evaluation & Learning", "bounded batch evaluation intake"),
    ("EXT-MEMPROVIDER-HERMES", "external memory providers", "ELO Memory", "provider adapter without authority transfer"),
    ("EXT-LEARN-HERMES", "skill learning / /learn", "ELO Knowledge & Skills", "candidate skill synthesis with governed admission"),
    ("EXT-LEARNING-GRAPH-HERMES", "learning graph / curator", "ELO Evolution Memory", "evidence-linked learning relationships without autonomous promotion"),
    ("EXT-CONTEXT-PLUGIN-HERMES", "context engine plugins", "ELO Context", "bounded context-engine adapter behind existing context authority"),
    ("EXT-WORKTREE-HERMES", "isolated git worktrees", "ELO Forge", "isolated technical workspaces with governed merge"),
    ("EXT-MULTIAGENT-HERMES", "subagent delegation / parallel workstreams", "ELO Agent Delegation", "bounded delegated execution with evidence and authority limits"),
    ("EXT-CRON-HERMES", "scheduled agent tasks", "ELO Workflow/Automation", "deterministic scheduled invocation with ELO governance"),
    ("EXT-MCP-HERMES", "external MCP capabilities", "ELO External Capability Gateway", "allowlisted external capability access with governed evidence"),
    ("EXT-TOOL-SEARCH-HERMES", "progressive tool-schema disclosure / tool_search", "ELO Model/Tool Routing", "bounded tool discovery without eager schema exposure"),
    ("EXT-CODE-EXEC-HERMES", "programmatic tool calling / execute_code", "ELO Model/Tool Routing", "bounded programmatic tool orchestration"),
    ("EXT-API-HERMES", "OpenAI-compatible API server", "ELO External Capability Gateway", "authenticated external API boundary"),
    ("EXT-ACP-HERMES", "Agent Client Protocol / IDE integration", "ELO Agent Context & Delegation", "isolated agent-client session boundary"),
    ("EXT-PLUGIN-CATALOG-HERMES", "curated plugin catalog/discovery", "ELO External Capability Gateway", "discover-before-activate capability contract"),
    ("EXT-PROMPT-CACHE-HERMES", "cross-session prompt caching", "ELO Model/Tool Routing", "bounded cache scope and invalidation contract"),
)

CURRENT_DISCOVERY_DATE = "2026-10-02"
CURRENT_DISCOVERY_SOURCE = "Hermes public capability documentation"


@dataclass(frozen=True, slots=True)
class HermesSurfaceObservation:
    """Current source observation; never an ELO authorization or promotion."""

    candidate_id: str
    change: str
    interface: str
    dependencies: tuple[str, ...]
    relations: tuple[str, ...]
    safety_boundary: tuple[str, ...]
    validation_state: str = "SOURCE_OBSERVED_CANDIDATE_ONLY"


CURRENT_SURFACE_OBSERVATIONS: tuple[HermesSurfaceObservation, ...] = (
    HermesSurfaceObservation("EXT-TOOL-SEARCH-HERMES", "Progressive disclosure now defers MCP/plugin tools and optionally named built-ins behind tool_search/tool_describe/tool_call; connector results can be searched remotely.", "tool_search(queries), tool_describe(names), tool_call(calls)", ("MCP", "plugin tools", "connector gateway"), ("ELO Model/Tool Routing", "ELO External Capability Gateway", "skills"), ("selected tool is not executed during discovery", "catalog size and schema disclosure remain bounded")),
    HermesSurfaceObservation("EXT-MCP-HERMES", "MCP supports stdio and HTTP servers, startup discovery, per-server filtering, and connector-backed remote discovery.", "MCP server descriptor + filtered tool registration", ("MCP transport", "external tool server", "connector gateway"), ("ELO External Capability Gateway", "ELO Model/Tool Routing"), ("server/tool allowlist", "external results are untrusted data")),
    HermesSurfaceObservation("EXT-PLUGIN-CATALOG-HERMES", "Plugin discovery is broader: general, memory-provider, context-engine, and model-provider surfaces; installs/updates apply static security scanning and activation remains explicit for general plugins.", "plugin.yaml + register(ctx) + provider selection", ("plugin catalog", "security scanner", "MCP allowlist"), ("skills", "tool routing", "external capability gateway"), ("discovery is not activation", "untrusted plugin code is not treated as audited")),
    HermesSurfaceObservation("EXT-MEMPROVIDER-HERMES", "Current documentation lists eight external memory providers; exactly one external provider is active while built-in memory remains additive.", "memory.provider selection + provider lifecycle", ("persistent memory", "provider plugin"), ("ELO Memory", "ELO Context", "learning governance"), ("provider does not become memory authority", "scope/provenance must remain explicit")),
    HermesSurfaceObservation("EXT-CODE-EXEC-HERMES", "execute_code runs programmatic tool orchestration in a child process through RPC; intermediate tool results stay out of model context.", "execute_code script + Hermes RPC transport", ("tool registry", "sandbox/child process", "RPC"), ("ELO Model/Tool Routing", "ExecutionBoundary", "evidence"), ("no business operation during discovery", "authorization and side-effect class remain ELO controls")),
    HermesSurfaceObservation("EXT-API-HERMES", "API surface now includes OpenAI-compatible chat/responses, runs/events, jobs, capability discovery, idempotency keys and session-key correlation.", "HTTP API + bearer auth + run/session metadata", ("API server", "profile routing", "persistent response/session state"), ("ELO External Capability Gateway", "ELO Workflow/Automation", "ELO Agent Context & Delegation"), ("authenticated boundary", "idempotent retries must preserve identity", "read-only capability discovery")),
    HermesSurfaceObservation("EXT-ACP-HERMES", "ACP exposes a curated editor toolset including terminal, execute_code and delegation while intentionally excluding cron/messaging; hosts may own MCP per session.", "ACP stdio session + curated toolset", ("agent-client protocol", "MCP session injection", "host approvals"), ("ELO Agent Context & Delegation", "ELO Context", "ELO External Capability Gateway"), ("host-controlled permissions can be unattended", "session identity and authorization must not be inferred")),
)


@dataclass(frozen=True, slots=True)
class HermesCandidate:
    candidate_id: str
    mechanism: str
    owner: str
    adaptation: str
    evidence_state: str = "source_observed"
    promotion_state: str = "candidate_only"
    canonical_mutation: bool = False


@dataclass(frozen=True, slots=True)
class CandidateMeasurement:
    candidate_id: str
    baseline: Mapping[str, float]
    adapted: Mapping[str, float]
    regressions: tuple[str, ...]
    repeatable: bool
    result: str


def build_candidate(candidate_id: str) -> HermesCandidate:
    for item in CANDIDATES:
        if item[0] == candidate_id:
            return HermesCandidate(*item)
    raise ValueError(f"unknown Hermes candidate: {candidate_id}")


def evaluate_candidate(candidate: HermesCandidate, baseline: Mapping[str, float], adapted: Mapping[str, float], *, regressions: tuple[str, ...] = (), repeatable: bool = False, metric_directions: Mapping[str, str] | None = None) -> CandidateMeasurement:
    if candidate.promotion_state != "candidate_only" or candidate.canonical_mutation:
        return CandidateMeasurement(candidate.candidate_id, baseline, adapted, regressions, repeatable, "REJECT")
    common = baseline.keys() & adapted.keys()
    if metric_directions is None:
        gains = [adapted[key] - baseline[key] for key in common]
    else:
        gains = []
        for key in common:
            direction = metric_directions.get(key)
            if direction not in {"maximize", "minimize"}:
                gains = []
                break
            delta = adapted[key] - baseline[key]
            if (direction == "maximize" and delta > 0) or (direction == "minimize" and delta < 0):
                gains.append(delta)
    if regressions:
        result = "REJECT"
    elif not gains or not repeatable:
        result = "RETEST"
    else:
        result = "EVOLUTION_GATE_REQUIRED"
    return CandidateMeasurement(candidate.candidate_id, baseline, adapted, regressions, repeatable, result)


__all__ = ["CANDIDATES", "CURRENT_DISCOVERY_DATE", "CURRENT_DISCOVERY_SOURCE", "CURRENT_SURFACE_OBSERVATIONS", "CandidateMeasurement", "HermesCandidate", "HermesSurfaceObservation", "build_candidate", "evaluate_candidate"]
