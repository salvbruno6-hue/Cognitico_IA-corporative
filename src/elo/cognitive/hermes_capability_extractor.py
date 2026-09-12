"""Deterministic extraction of portable capabilities from Hermes evidence.

The extractor is intentionally provider-neutral: it consumes an evidence-bearing
snapshot (file path -> text) and emits external capability observations. It does
not write ELO state, grant authorization, or promote learning. The existing
Symbiont Pattern Intake, Capability Absorber and Evolution Gate remain the
validation and promotion boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .symbiont_capability_absorption import ExternalCapabilityObservation
from .symbiont_pattern_intake import ExternalPatternInput

HERMES_PROVIDER = "ELO-Hermes-Agent"


@dataclass(frozen=True)
class HermesCapabilityPattern:
    capability_id: str
    title: str
    purpose: str
    mechanism: str
    interface_contract: str
    evidence_paths: tuple[str, ...]
    risk: str = "LOW"


# These patterns are architectural mechanisms observed in Hermes, not copied
# implementations. The markers make extraction auditable and deterministic.
PATTERN_RULES: tuple[tuple[str, HermesCapabilityPattern], ...] = (
    (
        "governed_execution_boundary",
        HermesCapabilityPattern(
            capability_id="HERMES-CAP-001",
            title="Governed execution boundary",
            purpose="Execute an already-authorized mission without transferring ELO authority to Hermes.",
            mechanism="Separate authorization/context construction from external execution and return evidence/outcome to ELO.",
            interface_contract="Request carries intent, tenant scope, mission class, authorized capabilities and evidence requirements; result carries status, evidence and outcome.",
            evidence_paths=("elo_bridge/contract.py", "elo_bridge/adapter.py", "elo_bridge/http_runtime.py"),
        ),
    ),
    (
        "non_canonical_learning",
        HermesCapabilityPattern(
            capability_id="HERMES-CAP-002",
            title="Non-canonical learning candidate",
            purpose="Prevent external execution from becoming canonical knowledge automatically.",
            mechanism="Validate learning candidates as candidate/pending/rejected and reject canonical decision fields at the bridge boundary.",
            interface_contract="Learning payload remains explicitly non-canonical and is returned as evidence-bearing candidate data.",
            evidence_paths=("elo_bridge/contract.py", "elo_bridge/skill_runtime.py"),
        ),
    ),
    (
        "runtime_contract_validation",
        HermesCapabilityPattern(
            capability_id="HERMES-CAP-003",
            title="Runtime contract validation",
            purpose="Continuously prove that the governed bridge still satisfies its execution contract.",
            mechanism="Run focused bridge, skill-runtime and HTTP-runtime tests in CI on changes to the governed bridge.",
            interface_contract="Validation is reproducible through the existing test suite and CI workflow; failure blocks confidence in the runtime contract.",
            evidence_paths=(".github/workflows/elo-hermes-runtime-validation.yml", "tests/test_elo_bridge_contract.py", "tests/test_elo_skill_runtime.py", "tests/test_elo_http_runtime.py"),
        ),
    ),
)


def extract_patterns(snapshot: Mapping[str, str]) -> tuple[HermesCapabilityPattern, ...]:
    """Extract only patterns whose declared evidence exists in ``snapshot``.

    ``snapshot`` is deliberately supplied by the caller so the ELO Core never
    gains implicit repository/network authority as a side effect of learning.
    """
    found: list[HermesCapabilityPattern] = []
    for _, pattern in PATTERN_RULES:
        if all(path in snapshot and snapshot[path].strip() for path in pattern.evidence_paths):
            found.append(pattern)
    return tuple(found)


def to_external_pattern(
    pattern: HermesCapabilityPattern,
    *,
    tenant_id: str,
    source_commit: str,
) -> ExternalPatternInput:
    """Translate an extracted pattern into the existing governed intake contract."""
    return ExternalPatternInput(
        pattern_id=pattern.capability_id,
        tenant_id=tenant_id,
        domain="runtime-governance",
        source_ref=HERMES_PROVIDER,
        source_commit=source_commit,
        problem=pattern.purpose,
        mechanism=pattern.mechanism,
        evidence_ids=tuple(f"hermes:{path}" for path in pattern.evidence_paths),
        existing_owner="Hermes",
        scope="symbiont-hermes-capability-absorption",
        source_kind="repository",
        risk=pattern.risk,
    )


def to_observation(
    pattern: HermesCapabilityPattern,
    *,
    tenant_id: str,
    source_commit: str,
) -> ExternalCapabilityObservation:
    """Build the evidence-bearing observation consumed by Capability Absorption."""
    return ExternalCapabilityObservation(
        capability_id=pattern.capability_id,
        provider=HERMES_PROVIDER,
        capability=pattern.title,
        purpose=pattern.purpose,
        mechanism=pattern.mechanism,
        interface_contract=pattern.interface_contract,
        evidence_ids=tuple(f"hermes:{path}" for path in pattern.evidence_paths),
        source_ref=HERMES_PROVIDER,
        source_commit=source_commit,
        tenant_id=tenant_id,
        domain="runtime-governance",
        risk=pattern.risk,
    )
