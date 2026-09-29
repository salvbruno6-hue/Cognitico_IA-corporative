"""Candidate-specific functional evaluation for EXT-CRON-HERMES."""
from __future__ import annotations
from dataclasses import dataclass
from .hermes_cron_adapter import adapt_schedule
from .hermes_cron_boundary import ScheduleSignal

@dataclass(frozen=True, slots=True)
class CronFunctionalEvidence:
    baseline_idempotency_collision_free_rate: float
    adapted_idempotency_collision_free_rate: float
    repeatable: bool
    boundary_integrity: bool
    provenance_refs: tuple[str, ...]
    continuity_baseline_rate: float = 0.0
    continuity_adapted_rate: float = 0.0
    continuity_repeatable: bool = False
    continuity_boundary_integrity: bool = False
    continuity_provenance_refs: tuple[str, ...] = ()

def _signals(prefix: str) -> tuple[ScheduleSignal, ...]:
    return tuple(
        ScheduleSignal(
            f"{prefix}-{i}", "multiteiner", f"task-{i}",
            (f"controlled-eval:cron-functional/{prefix.lower()}/{i}",),
            "0 8 * * *", "elo", True, True, True, False
        )
        for i in (1, 2)
    )

def _baseline(signals: tuple[ScheduleSignal, ...]) -> float:
    # Failure mode: a scheduler key built only from tenant + schedule expression
    # collides when distinct tasks share the same schedule.
    keys = tuple(f"{s.tenant_scope}:{s.schedule_expression}" for s in signals)
    return float(len(set(keys)) == len(signals))

def _adapted(signals: tuple[ScheduleSignal, ...]) -> float:
    contracts = tuple(adapt_schedule(s) for s in signals)
    keys = tuple(c.idempotency_key for c in contracts if c is not None)
    return float(
        len(keys) == len(signals)
        and len(set(keys)) == len(keys)
    )

def evaluate_cron_functional_gain() -> CronFunctionalEvidence:
    baseline = _signals("BASELINE")
    adapted = _signals("HERMES")
    baseline_rate = _baseline(baseline)
    adapted_rate = _adapted(adapted)
    repeatable = _adapted(_signals("REPEAT")) == adapted_rate
    contracts = tuple(adapt_schedule(s) for s in adapted)
    boundary = all(
        c is not None
        and not c.execution_permitted
        and not c.canonical_authority
        and bool(c.idempotency_key)
        for c in contracts
    )
    refs = tuple(ref for s in adapted for ref in s.source_refs)
    continuity = evaluate_cron_continuity_gain()
    return CronFunctionalEvidence(baseline_rate, adapted_rate, repeatable, boundary, refs, continuity[0], continuity[1], continuity[2], continuity[3], continuity[4])
