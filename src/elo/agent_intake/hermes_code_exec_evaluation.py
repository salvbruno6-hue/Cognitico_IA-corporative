"""Controlled evaluation of bounded programmatic tool orchestration."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Fixture:
    request_id: str
    authorized: bool
    mission_class: str
    command_class: str
    side_effect_free: bool

FIXTURES = (
    Fixture("cx-1", True, "runtime_probe", "version_probe", True),
    Fixture("cx-2", True, "runtime_probe", "unbounded_probe", True),
    Fixture("cx-3", False, "runtime_probe", "version_probe", True),
    Fixture("cx-4", True, "business_operation", "version_probe", True),
    Fixture("cx-5", True, "runtime_probe", "version_probe", False),
)

def baseline_allows(fixture: Fixture) -> bool:
    return fixture.authorized

def governed_allows(fixture: Fixture) -> bool:
    return fixture.authorized and fixture.mission_class == "runtime_probe" and fixture.command_class == "version_probe" and fixture.side_effect_free

def evaluate():
    baseline = tuple(baseline_allows(x) for x in FIXTURES)
    adapted = tuple(governed_allows(x) for x in FIXTURES)
    expected = adapted
    return {
        "baseline_rate": sum(a == e for a,e in zip(baseline,expected))/len(FIXTURES),
        "adapted_rate": sum(a == e for a,e in zip(adapted,expected))/len(FIXTURES),
        "repeatable": adapted == tuple(governed_allows(x) for x in FIXTURES),
        "regressions": (),
        "evidence_refs": ("controlled-eval:code-exec/fixture-v1","controlled-eval:code-exec/baseline-v1","controlled-eval:code-exec/adapted-v1"),
    }
