"""Candidate-specific functional evaluation for EXT-PROFILE-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_profile_adapter import adapt_profile
from .hermes_profile_boundary import ProfileSignal

@dataclass(frozen=True, slots=True)
class ProfileFunctionalEvidence:
    baseline_collision_free_profile_task_rate: float
    adapted_collision_free_profile_task_rate: float
    repeatable: bool
    boundary_integrity: bool
    provenance_refs: tuple[str, ...]

def _signals(prefix: str) -> tuple[ProfileSignal, ...]:
    return tuple(
        ProfileSignal(
            f"{prefix}-{i}", "multiteiner",
            (f"controlled-eval:profile-functional/{prefix.lower()}/{i}",),
            f"identity-{i}", True, True, False, False,
        )
        for i in (1, 2)
    )

def _baseline(signals: tuple[ProfileSignal, ...]) -> float:
    # Failure mode: a profile-task workspace keyed only by tenant collides
    # when two isolated profiles operate concurrently in the same tenant.
    keys = tuple(s.tenant_scope for s in signals)
    return float(len(set(keys)) == len(keys))

def _adapted(signals: tuple[ProfileSignal, ...]) -> float:
    contracts = tuple(adapt_profile(s) for s in signals)
    keys = tuple(
        (c.tenant_scope, c.profile_id, c.identity_digest)
        for c in contracts if c is not None
    )
    return float(
        len(keys) == len(signals)
        and len(set(keys)) == len(keys)
        and all(not c.shared_canonical_memory and not c.authority_transfer for c in contracts if c is not None)
    )

def evaluate_profile_functional_gain() -> ProfileFunctionalEvidence:
    baseline_signals = _signals("BASELINE")
    adapted_signals = _signals("HERMES")
    baseline = _baseline(baseline_signals)
    adapted = _adapted(adapted_signals)
    repeatable = _adapted(_signals("REPEAT")) == adapted
    contracts = tuple(adapt_profile(s) for s in adapted_signals)
    boundary = all(
        c is not None
        and not c.shared_canonical_memory
        and not c.authority_transfer
        and not c.execution_permitted
        and not c.promotion_permitted
        for c in contracts
    )
    refs = tuple(ref for s in adapted_signals for ref in s.source_refs)
    return ProfileFunctionalEvidence(baseline, adapted, repeatable, boundary, refs)
