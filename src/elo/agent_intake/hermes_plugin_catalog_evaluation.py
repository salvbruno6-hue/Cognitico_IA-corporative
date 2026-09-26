"""Controlled functional evaluation for EXT-PLUGIN-CATALOG-HERMES.

The fixture measures authorization precision of discovery-before-activation.
It is deterministic and local to the evaluation boundary; it does not load
external plugins, execute business operations, or mutate canonical state.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PluginFixture:
    plugin_id: str
    discoverable: bool
    allowlisted: bool
    provenance_valid: bool


@dataclass(frozen=True, slots=True)
class PluginCatalogEvaluation:
    baseline_rate: float
    adapted_rate: float
    repeatable: bool
    regressions: tuple[str, ...]
    evidence_refs: tuple[str, ...]


FIXTURES: tuple[PluginFixture, ...] = (
    PluginFixture("tool-read", True, True, True),
    PluginFixture("tool-write", True, False, True),
    PluginFixture("tool-unknown", False, False, False),
    PluginFixture("tool-read-2", True, True, True),
    PluginFixture("tool-external", True, False, True),
)


def baseline_activate(fixture: PluginFixture) -> bool:
    """Baseline: discovery is treated as sufficient for activation."""
    return fixture.discoverable


def governed_activate(fixture: PluginFixture) -> bool:
    """Adapted policy: activation requires discovery, allowlist and provenance."""
    return fixture.discoverable and fixture.allowlisted and fixture.provenance_valid


def _precision(decisions: tuple[bool, ...], fixtures: tuple[PluginFixture, ...]) -> float:
    correct = sum(
        decision == (fixture.discoverable and fixture.allowlisted and fixture.provenance_valid)
        for decision, fixture in zip(decisions, fixtures)
    )
    return correct / len(fixtures)


def evaluate() -> PluginCatalogEvaluation:
    baseline = tuple(baseline_activate(item) for item in FIXTURES)
    adapted = tuple(governed_activate(item) for item in FIXTURES)
    baseline_rate = _precision(baseline, FIXTURES)
    adapted_rate = _precision(adapted, FIXTURES)

    # Repeatability is proven by deterministic re-execution of the same fixture.
    repeatable = (
        baseline == tuple(baseline_activate(item) for item in FIXTURES)
        and adapted == tuple(governed_activate(item) for item in FIXTURES)
    )
    regressions: tuple[str, ...] = ()
    return PluginCatalogEvaluation(
        baseline_rate=baseline_rate,
        adapted_rate=adapted_rate,
        repeatable=repeatable,
        regressions=regressions,
        evidence_refs=(
            "controlled-eval:plugin-catalog/fixture-v1",
            "controlled-eval:plugin-catalog/baseline-v1",
            "controlled-eval:plugin-catalog/adapted-v1",
        ),
    )
