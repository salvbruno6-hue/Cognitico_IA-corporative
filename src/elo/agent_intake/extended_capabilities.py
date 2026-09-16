"""Governed Hermes/OpenClaw capability extensions attached to existing ELO owners.

An extension is not a new ELO capability. It is a bounded adaptation candidate
that extends an existing owner with an observed mechanism from Hermes or OpenClaw.
The module is deterministic and side-effect free.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


EXTENSIONS: tuple[tuple[str, str, str, str], ...] = (
    ("EXT-MEM-HERMES", "Hermes", "ELO Memory", "scoped state retention"),
    ("EXT-MEM-OPENCLAW", "OpenClaw", "ELO Memory", "authorized recall/search and controlled promotion"),
    ("EXT-SKILL-HERMES", "Hermes", "ELO Skills", "named executable capability"),
    ("EXT-SKILL-OPENCLAW", "OpenClaw", "ELO Skills", "plugin skill discovery and controlled loading"),
    ("EXT-TOOL-HERMES", "Hermes", "ELO Toolset Resolution", "capability allowlisting"),
    ("EXT-TOOL-OPENCLAW", "OpenClaw", "ELO Toolset Resolution", "explicit tool policy and deny-by-default"),
    ("EXT-CONTEXT-HERMES", "Hermes", "ELO Context", "hierarchical context composition"),
    ("EXT-CONTEXT-OPENCLAW", "OpenClaw", "ELO Context", "context assembly lifecycle"),
    ("EXT-DELEG-HERMES", "Hermes", "ELO Delegation", "bounded worker handoff"),
    ("EXT-DELEG-OPENCLAW", "OpenClaw", "ELO Delegation", "scoped subagent spawn"),
    ("EXT-AUTO-HERMES", "Hermes", "ELO Automation", "explicit repeatable schedule registration"),
    ("EXT-AUTO-OPENCLAW", "OpenClaw", "ELO Automation", "schedule identity and lifecycle"),
    ("EXT-MCP-HERMES", "Hermes", "ELO External Capability Gateway", "external capability allowlisting"),
    ("EXT-MCP-OPENCLAW", "OpenClaw", "ELO External Capability Gateway", "MCP boundary under policy"),
    ("EXT-STATE-HERMES", "Hermes", "ELO State Recovery", "scoped snapshot and restore"),
    ("EXT-STATE-OPENCLAW", "OpenClaw", "ELO State Recovery", "session repair and recovery"),
)


@dataclass(frozen=True, slots=True)
class ExtendedCapability:
    extension_id: str
    source_provider: str
    extends_capability: str
    mechanism: str
    adapted: bool
    evidence_quality: str
    promotion_state: str = "candidate_only"
    canonical_mutation: bool = False


@dataclass(frozen=True, slots=True)
class EvolutionMeasurement:
    extension_id: str
    baseline: Mapping[str, float]
    adapted: Mapping[str, float]
    regressions: tuple[str, ...]
    repeatable: bool
    result: str
    measured_gain: Mapping[str, float]


def _quality(evidence: Mapping[str, Any]) -> str:
    if evidence.get("live_execution") is True and evidence.get("outcome"):
        return "execution_verified"
    if evidence.get("controlled_test") is True and evidence.get("outcome"):
        return "controlled_verified"
    if evidence.get("source_reference"):
        return "reference_only"
    return "insufficient"


def extend_capability(extension_id: str, evidence: Mapping[str, Any]) -> ExtendedCapability:
    matches = [row for row in EXTENSIONS if row[0] == extension_id]
    if not matches:
        raise ValueError(f"unknown extension: {extension_id}")
    extension, provider, owner, mechanism = matches[0]
    return ExtendedCapability(
        extension_id=extension,
        source_provider=provider,
        extends_capability=owner,
        mechanism=mechanism,
        adapted=True,
        evidence_quality=_quality(evidence),
    )


def extension_is_eligible_for_test(extension: ExtendedCapability) -> bool:
    return extension.evidence_quality in {"controlled_verified", "execution_verified"}


def measure_evolution(
    extension: ExtendedCapability,
    baseline: Mapping[str, float],
    adapted: Mapping[str, float],
    *,
    regressions: tuple[str, ...] = (),
    repeatable: bool = False,
) -> EvolutionMeasurement:
    """Evaluate measured improvement against the existing ELO capability baseline.

    Higher-is-better metrics are assumed. Gains are normalized to a stable decimal
    precision so deterministic tests do not depend on binary floating-point artifacts.
    The function never changes canonical state or promotion status.
    """
    if not extension_is_eligible_for_test(extension):
        return EvolutionMeasurement(
            extension.extension_id,
            baseline,
            adapted,
            regressions,
            repeatable,
            "REJECT",
            {},
        )

    gain = {
        key: round(adapted[key] - baseline[key], 10)
        for key in baseline.keys() & adapted.keys()
        if adapted[key] - baseline[key] > 0
    }
    if regressions:
        result = "REJECT"
    elif not gain or not repeatable:
        result = "RETEST"
    else:
        result = "STRENGTHEN"
    return EvolutionMeasurement(
        extension.extension_id,
        baseline,
        adapted,
        regressions,
        repeatable,
        result,
        gain,
    )


__all__ = [
    "EXTENSIONS",
    "EvolutionMeasurement",
    "ExtendedCapability",
    "extend_capability",
    "extension_is_eligible_for_test",
    "measure_evolution",
]
