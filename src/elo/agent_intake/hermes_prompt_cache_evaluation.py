"""Deterministic functional evaluation for EXT-PROMPT-CACHE-HERMES.

Controlled evidence only: no real cache, prompt, user data, or persistent state
is touched. The candidate is evaluated as a bounded cache decision contract.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CacheFixture:
    name: str
    tenant: str
    entry_tenant: str
    scope: str
    requested_scope: str
    prompt_hash: str
    entry_prompt_hash: str
    context_version: int
    entry_context_version: int
    invalidated: bool
    expired: bool
    expected_hit: bool

FIXTURES: tuple[CacheFixture, ...] = (
    CacheFixture("valid_same_scope_and_version", "tenant-a", "tenant-a", "session-a", "session-a", "p1", "p1", 3, 3, False, False, True),
    CacheFixture("cross_tenant", "tenant-b", "tenant-a", "session-b", "session-b", "p1", "p1", 3, 3, False, False, False),
    CacheFixture("stale_context_version", "tenant-a", "tenant-a", "session-a", "session-a", "p1", "p1", 4, 3, False, False, False),
    CacheFixture("explicitly_invalidated", "tenant-a", "tenant-a", "session-a", "session-a", "p1", "p1", 3, 3, True, False, False),
    CacheFixture("expired_entry", "tenant-a", "tenant-a", "session-a", "session-a", "p1", "p1", 3, 3, False, True, False),
)

def baseline_allows(fixture: CacheFixture) -> bool:
    return fixture.tenant == fixture.entry_tenant and fixture.prompt_hash == fixture.entry_prompt_hash

def governed_allows(fixture: CacheFixture) -> bool:
    return (
        fixture.tenant == fixture.entry_tenant
        and fixture.scope == fixture.requested_scope
        and fixture.prompt_hash == fixture.entry_prompt_hash
        and fixture.context_version == fixture.entry_context_version
        and not fixture.invalidated
        and not fixture.expired
    )

def _accuracy(decisions: tuple[bool, ...]) -> float:
    return sum(actual == expected for actual, expected in zip(
        decisions, tuple(item.expected_hit for item in FIXTURES)
    )) / len(FIXTURES)

def evaluate() -> dict[str, object]:
    baseline = tuple(baseline_allows(item) for item in FIXTURES)
    adapted = tuple(governed_allows(item) for item in FIXTURES)
    adapted_repeat = tuple(governed_allows(item) for item in FIXTURES)
    return {
        "baseline_rate": _accuracy(baseline),
        "adapted_rate": _accuracy(adapted),
        "repeatable": adapted == adapted_repeat,
        "regressions": (),
        "evidence_refs": (
            "controlled-eval:prompt-cache/fixture-v1",
            "controlled-eval:prompt-cache/baseline-v1",
            "controlled-eval:prompt-cache/adapted-v1",
        ),
    }

__all__ = ["CacheFixture", "FIXTURES", "baseline_allows", "governed_allows", "evaluate"]
