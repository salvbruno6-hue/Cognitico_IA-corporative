"""Candidate-only registry for Hermes v0.21.x surface deltas observed since the
previous ELO intake. No Hermes runtime or business operation is invoked.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class HermesCurrentDelta:
    mechanism_id: str
    observed_capability: str
    elo_owner: str
    candidate_introduction: str
    dependencies: tuple[str, ...]
    relations: tuple[str, ...]
    candidate_only: bool = True
    canonical_mutation: bool = False
    business_operation: bool = False

CURRENT_DELTAS = (
    HermesCurrentDelta(
        "HERMES-WIRE-CONTRACT-REGISTRY",
        "Pydantic wire-contract registry with generated TS/OpenRPC and server-to-client JSON-RPC",
        "ELO Context/Interfaces",
        "introduce versioned interface contracts and generated schema evidence at integration boundaries",
        ("Pydantic contracts", "JSON-RPC", "generated schemas"),
        ("ExecutionBoundary", "External Capability Gateway"),
    ),
    HermesCurrentDelta(
        "HERMES-MCP-ISSUER-BOUND-AUTH",
        "MCP OAuth refresh tokens bound to issuer plus re-authentication health nudges",
        "ELO External Capability Gateway",
        "introduce issuer-bound credential provenance and explicit re-auth state without treating connectivity as authorization",
        ("MCP OAuth", "issuer identity", "health state"),
        ("EXT-MCP-HERMES", "External Capability Gateway"),
    ),
    HermesCurrentDelta(
        "HERMES-SESSION-WRITER-REGISTRY",
        "read-only session DB attachments and shared in-process writer handle registry",
        "ELO Context/State",
        "introduce explicit reader/writer topology metadata and contention-safety evidence",
        ("state.db", "session registry", "WAL"),
        ("HERMES-SESSION-LINEAGE", "ExecutionBoundary"),
    ),
    HermesCurrentDelta(
        "HERMES-LIVE-DELEGATION-STEERING",
        "running child listing, mid-flight steering, early stop, partial-result retention and child output JSON schema",
        "ELO Agent Delegation",
        "refine delegated execution with explicit steering provenance, termination reason and output-contract evidence",
        ("delegate_task", "child registry", "output schema"),
        ("EXT-MULTIAGENT-HERMES", "HERMES-DELEGATION-CONTROLS"),
    ),
    HermesCurrentDelta(
        "HERMES-CRON-CONTINUITY",
        "persistent cron memory, continuity between runs, durable scratchpad and no-change monitor short-circuit",
        "ELO Workflow/Automation",
        "introduce run-lineage and continuity metadata as operational context, never as automatic learning",
        ("cron runtime", "memory", "scratchpad"),
        ("EXT-CRON-HERMES", "HERMES-SESSION-LINEAGE"),
    ),
    HermesCurrentDelta(
        "HERMES-PROTECTED-INSTRUCTION-SURFACES",
        "AGENTS.md, skills and memory stores require write approval; redaction expanded across logs/checkpoints/ACP",
        "ELO Security/ExecutionBoundary",
        "introduce protected-instruction provenance and write-approval evidence as a boundary invariant",
        ("approval system", "redaction", "instruction stores"),
        ("ExecutionBoundary", "EXT-LEARN-HERMES"),
    ),
    HermesCurrentDelta(
        "HERMES-BOT-PEER-MESSAGING",
        "durable bot-to-bot DMs across profiles/gateways with canonical Bot Chat",
        "ELO Agent Delegation",
        "introduce durable inter-agent message provenance without equating message receipt with authorization or learning",
        ("Bot Chat", "profiles", "gateway"),
        ("EXT-MULTIAGENT-HERMES", "HERMES-DELEGATION-CONTROLS"),
    ),
    HermesCurrentDelta(
        "HERMES-DESKTOP-BROWSER-ACTION",
        "agent navigation/click/read inside the desktop browser with link context",
        "ELO ExecutionBoundary",
        "introduce browser interaction as an explicit externally-effectful capability requiring the canonical execution boundary",
        ("browser runtime", "approval controls"),
        ("ExecutionBoundary", "External Capability Gateway"),
    ),
    HermesCurrentDelta(
        "HERMES-MODEL-CAPABILITY-METADATA",
        "per-model context/pricing/capability overrides and training-tier selection warnings",
        "ELO Model/Tool Routing",
        "introduce model capability metadata and selection-risk evidence before routing decisions",
        ("model catalog", "selection guard"),
        ("ELO Model/Tool Routing", "HERMES-TOOL-LOOP-GUARD"),
    ),
)

def validate_current_deltas() -> int:
    ids = [item.mechanism_id for item in CURRENT_DELTAS]
    assert len(ids) == len(set(ids))
    assert len(CURRENT_DELTAS) == 9
    assert all(item.candidate_only for item in CURRENT_DELTAS)
    assert all(not item.canonical_mutation for item in CURRENT_DELTAS)
    assert all(not item.business_operation for item in CURRENT_DELTAS)
    assert all(item.elo_owner and item.candidate_introduction for item in CURRENT_DELTAS)
    return len(CURRENT_DELTAS)
