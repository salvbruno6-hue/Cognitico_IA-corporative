"""Refined Symbiont adaptation for ELO capability evolution.

The Symbiont does not create a competing runtime or authority. It converts
validated external experience into a bounded, explicit ELO skill adjustment
candidate attached to an existing ELO capability.

The adapter is deterministic and side-effect free: it never mutates canonical
knowledge, Soul, Core contracts, routing authority, or infrastructure state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .native_capabilities import CAPABILITY_IDS


@dataclass(frozen=True, slots=True)
class CapabilityProfile:
    capability_id: str
    existing_capacity: str
    refinement_focus: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SymbiontAdaptation:
    capability_id: str
    existing_capacity: str
    mechanism: str
    adjustment: str
    rationale: tuple[str, ...]
    expected_gain: tuple[str, ...]
    source_experience: tuple[str, ...]
    evidence_quality: str
    promotion_state: str = "candidate_only"
    canonical_mutation: bool = False


PROFILES: dict[str, CapabilityProfile] = {
    "HERMES-MEMORY": CapabilityProfile(
        "HERMES-MEMORY", "ELO Memory", ("structure", "retrieval", "isolation")
    ),
    "HERMES-SKILLS": CapabilityProfile(
        "HERMES-SKILLS", "ELO Skills", ("registration", "execution", "reuse")
    ),
    "HERMES-TOOLSETS": CapabilityProfile(
        "HERMES-TOOLSETS", "ELO Toolset Resolution", ("allowlist", "scope", "denial")
    ),
    "HERMES-CONTEXT": CapabilityProfile(
        "HERMES-CONTEXT", "ELO Context", ("hierarchy", "precedence", "clarity")
    ),
    "HERMES-DELEGATION": CapabilityProfile(
        "HERMES-DELEGATION", "ELO Delegation", ("scope", "handoff", "result")
    ),
    "HERMES-AUTOMATION": CapabilityProfile(
        "HERMES-AUTOMATION", "ELO Automation", ("registration", "safety", "repeatability")
    ),
    "HERMES-MCP": CapabilityProfile(
        "HERMES-MCP", "ELO External Capability Gateway", ("trust", "allowlist", "boundary")
    ),
    "HERMES-CHECKPOINT": CapabilityProfile(
        "HERMES-CHECKPOINT", "ELO State Recovery", ("snapshot", "restore", "scope")
    ),
}

# These are experience surfaces, not additional ELO capability identities.
EXPERIENCE_SOURCES: dict[str, tuple[str, ...]] = {
    "HERMES-MEMORY": ("Hermes: memory runtime", "OpenClaw: extensions/memory-core/index.ts"),
    "HERMES-SKILLS": ("Hermes: operational skills", "OpenClaw: src/agents/skills/plugin-skills.ts"),
    "HERMES-TOOLSETS": ("Hermes: tools/plugins", "OpenClaw: src/agents/tool-policy.ts"),
    "HERMES-CONTEXT": ("Hermes: contextual execution", "OpenClaw: src/agents/harness/context-engine-lifecycle.ts"),
    "HERMES-DELEGATION": ("Hermes: subagents", "OpenClaw: src/agents/subagent-spawn.ts"),
    "HERMES-AUTOMATION": ("Hermes: execution scheduling", "OpenClaw: src/cron/schedule.ts"),
    "HERMES-MCP": ("Hermes: external tools/plugins", "OpenClaw: src/mcp/tools-stdio-server.ts"),
    "HERMES-CHECKPOINT": ("Hermes: execution state", "OpenClaw: src/agents/session-file-repair.ts"),
}

MECHANISMS: dict[str, tuple[str, str]] = {
    "HERMES-MEMORY": ("scoped state retention", "attach reusable memory operations to tenant-scoped ELO memory"),
    "HERMES-SKILLS": ("named executable capability", "make skill registration and execution explicit and reusable"),
    "HERMES-TOOLSETS": ("capability allowlisting", "resolve tools through explicit authorization instead of implicit availability"),
    "HERMES-CONTEXT": ("hierarchical context composition", "preserve parent context while allowing explicit child precedence"),
    "HERMES-DELEGATION": ("bounded worker handoff", "delegate only an authorized payload and return a scoped result"),
    "HERMES-AUTOMATION": ("explicit schedule registration", "represent repeatable automation as a governed registration rather than hidden execution"),
    "HERMES-MCP": ("external capability boundary", "require explicit allowlisting before an external capability is considered available"),
    "HERMES-CHECKPOINT": ("scoped state snapshot and restore", "recover execution state without changing canonical knowledge"),
}


def _successful_outcome(evidence: Mapping[str, Any]) -> bool:
    """Return true only when an execution outcome explicitly contains no false result."""
    outcome = evidence.get("outcome")
    return isinstance(outcome, Mapping) and bool(outcome) and all(value is True for value in outcome.values())


def _quality(evidence: Mapping[str, Any]) -> str:
    """Classify evidence conservatively; failed outcomes are not execution proof."""
    if evidence.get("live_execution") is True and _successful_outcome(evidence):
        return "execution_verified"
    if evidence.get("controlled_test") is True and _successful_outcome(evidence):
        return "controlled_verified"
    if evidence.get("source_reference"):
        return "reference_only"
    return "insufficient"


def refine_capability(capability_id: str, evidence: Mapping[str, Any]) -> SymbiontAdaptation:
    """Produce a refined candidate adjustment attached to an existing ELO capacity."""
    if capability_id not in CAPABILITY_IDS:
        raise ValueError(f"unknown capability: {capability_id}")

    profile = PROFILES[capability_id]
    mechanism, adjustment = MECHANISMS[capability_id]
    quality = _quality(evidence)
    rationale = (
        f"Reuse existing capacity: {profile.existing_capacity}.",
        f"Refine through {mechanism}.",
        "Keep authorization and canonical ownership inside ELO.",
        "Require measurable evidence before promotion.",
    )
    expected_gain = tuple(f"improve {focus}" for focus in profile.refinement_focus)
    return SymbiontAdaptation(
        capability_id=capability_id,
        existing_capacity=profile.existing_capacity,
        mechanism=mechanism,
        adjustment=adjustment,
        rationale=rationale,
        expected_gain=expected_gain,
        source_experience=EXPERIENCE_SOURCES[capability_id],
        evidence_quality=quality,
    )


def refinement_is_eligible_for_test(adaptation: SymbiontAdaptation) -> bool:
    """Only validated evidence can enter the controlled refinement test."""
    return adaptation.evidence_quality in {"controlled_verified", "execution_verified"}


__all__ = [
    "CapabilityProfile",
    "SymbiontAdaptation",
    "PROFILES",
    "EXPERIENCE_SOURCES",
    "refine_capability",
    "refinement_is_eligible_for_test",
]
