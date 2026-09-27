"""Candidate contracts for newly surfaced Hermes mechanisms (2026-09-27)."""

from dataclasses import dataclass
from .hermes_capability_loops import CapabilityKind

@dataclass(frozen=True, slots=True)
class HermesSurfaceCandidate:
    candidate_id: str
    mechanism: str
    native_name: str
    kind: CapabilityKind
    interface: str
    invariants: tuple[str, ...]
    dependencies: tuple[str, ...]
    relations: tuple[str, ...]

CURRENT_SURFACE_CANDIDATES = (
    HermesSurfaceCandidate("EXT-BOT-MODE-HERMES", "persistent specialist Bot Mode", "elo_specialist_agent_profile", CapabilityKind.FUNCTION,
        "isolated specialist identity/context/toolset contract",
        ("identity-isolated", "context-isolated", "toolset-bounded", "no-authority-transfer"),
        ("agent-context", "delegation", "skills"), ("multiagent", "profiles", "governance")),
    HermesSurfaceCandidate("EXT-CONTEXT-FILES-HERMES", "project context files", "elo_context_file_assembly", CapabilityKind.STRUCTURE,
        "scoped context-source metadata and precedence contract",
        ("scope-explicit", "provenance-preserved", "precedence-deterministic", "bounded-context"),
        ("context-engine", "artifact-resolution"), ("contextref", "memory", "skills")),
    HermesSurfaceCandidate("EXT-SESSION-SEARCH-HERMES", "cross-session search", "elo_session_evidence_search", CapabilityKind.FUNCTION,
        "read-only historical-session retrieval contract",
        ("read-only", "tenant-isolated", "provenance-preserved", "no-memory-promotion"),
        ("memory", "session-store"), ("context", "evidence", "learning")),
)

def validate_surface_candidate(candidate):
    issues = []
    if not candidate.candidate_id.startswith("EXT-"): issues.append("invalid candidate identity")
    if not candidate.native_name.startswith("elo_"): issues.append("native contract must be ELO-owned")
    if not candidate.interface: issues.append("missing interface")
    if not candidate.invariants: issues.append("missing invariants")
    if not candidate.dependencies: issues.append("missing dependencies")
    if not candidate.relations: issues.append("missing relations")
    return not issues, tuple(issues)
