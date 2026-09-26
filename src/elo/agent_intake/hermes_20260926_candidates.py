"""Native ELO candidate contracts for newly observed Hermes surfaces (2026-09-26).

Discovery/validation only. No Hermes runtime is imported or mutated.
No business operation is executed and no candidate is promoted here.
"""
from __future__ import annotations

from dataclasses import dataclass

from .hermes_capability_loops import CapabilityEvidence, CapabilityKind, CapabilityState, TransformationCandidate


@dataclass(frozen=True)
class HermesCurrentCandidateSpec:
    candidate_id: str
    mechanism: str
    native_name: str
    kind: CapabilityKind
    interface: str
    invariants: tuple[str, ...]
    dependencies: tuple[str, ...]
    relations: tuple[str, ...]


CURRENT_CANDIDATES: tuple[HermesCurrentCandidateSpec, ...] = (
    HermesCurrentCandidateSpec(
        "EXT-CODE-EXEC-HERMES",
        "programmatic tool calling / execute_code",
        "elo_programmatic_tool_orchestration",
        CapabilityKind.FUNCTION,
        "bounded code-execution request/response contract",
        ("no-business-side-effects", "bounded-tool-scope", "provenance-preserved", "explicit-authorization"),
        ("tool-registry", "execution-sandbox"),
        ("model-tool-routing", "evidence"),
    ),
    HermesCurrentCandidateSpec(
        "EXT-API-HERMES",
        "OpenAI-compatible API server",
        "elo_external_api_boundary",
        CapabilityKind.STRUCTURE,
        "authenticated provider/API boundary metadata",
        ("external-boundary", "provenance-preserved", "no-authority-transfer", "explicit-authorization"),
        ("external-ai-contract", "auth-boundary"),
        ("mcp", "routing", "agent-context"),
    ),
    HermesCurrentCandidateSpec(
        "EXT-ACP-HERMES",
        "Agent Client Protocol / IDE integration",
        "elo_agent_client_boundary",
        CapabilityKind.STRUCTURE,
        "client/session capability contract",
        ("session-isolated", "identity-preserved", "provenance-preserved", "no-authority-transfer"),
        ("agent-context", "external-connection"),
        ("delegation", "context"),
    ),
    HermesCurrentCandidateSpec(
        "EXT-PLUGIN-CATALOG-HERMES",
        "curated plugin catalog/discovery",
        "elo_capability_discovery_catalog",
        CapabilityKind.FUNCTION,
        "discover-before-activate capability contract",
        ("discovery-not-authority", "activation-explicit", "provenance-preserved", "allowlist-bound"),
        ("capability-registry", "external-capability-gateway"),
        ("skills", "tool-routing", "governance"),
    ),
    HermesCurrentCandidateSpec(
        "EXT-PROMPT-CACHE-HERMES",
        "cross-session prompt caching",
        "elo_prompt_cache_boundary",
        CapabilityKind.FUNCTION,
        "cache-key/scope/invalidation contract",
        ("tenant-isolated", "scope-explicit", "stale-data-bounded", "provenance-preserved"),
        ("context", "model-runtime"),
        ("memory", "tool-routing", "context"),
    ),
)


def build_evidence(spec: HermesCurrentCandidateSpec, revision: str) -> CapabilityEvidence:
    return CapabilityEvidence(
        mechanism_id=spec.candidate_id,
        source="Hermes public capability documentation",
        revision=revision,
        interface=spec.interface,
        invariants=spec.invariants,
        dependencies=spec.dependencies,
        relations=spec.relations,
        evidence_refs=(f"hermes:{spec.candidate_id}:source",),
    )


def build_native_candidate(
    evidence: CapabilityEvidence,
    spec: HermesCurrentCandidateSpec,
    variant: int = 0,
) -> TransformationCandidate:
    if evidence.mechanism_id != spec.candidate_id:
        raise ValueError("candidate/spec mechanism mismatch")
    return TransformationCandidate(
        mechanism_id=spec.candidate_id,
        candidate_id=f"ELO-{spec.candidate_id}",
        kind=spec.kind,
        state=CapabilityState.TRANSFORMING,
        native_name=spec.native_name,
        contract=(
            "read-only discovery contract",
            "explicit authorization boundary",
            "evidence/provenance output",
            "fail-closed on missing governance",
        ),
        source=evidence.source,
        revision=evidence.revision,
        evidence_refs=evidence.evidence_refs,
        invariants=evidence.invariants,
        dependencies=evidence.dependencies,
        relations=evidence.relations,
        transformation_notes=("candidate-only; no Hermes runtime dependency",),
        variant=variant,
    )


def validate_native_contract(candidate: TransformationCandidate) -> tuple[bool, tuple[str, ...]]:
    issues: list[str] = []
    if not candidate.contract:
        issues.append("missing native contract")
    if not candidate.evidence_refs:
        issues.append("missing evidence")
    if not candidate.invariants:
        issues.append("missing invariants")
    if any("authority" in item.lower() and "transfer" in item.lower() for item in candidate.invariants):
        pass
    if "Hermes" in candidate.native_name:
        issues.append("native implementation must not import Hermes runtime")
    if not candidate.transformation_notes:
        issues.append("missing transformation boundary")
    return not issues, tuple(issues)
