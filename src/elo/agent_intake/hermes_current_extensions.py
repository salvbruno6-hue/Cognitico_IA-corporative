"""Candidate-only adaptations from currently documented Hermes mechanisms.

This registry is descriptive and deterministic. It does not execute Hermes,
change canonical ELO state, or promote a candidate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


CANDIDATES: tuple[tuple[str, str, str, str], ...] = (
    ("EXT-CONTEXTREF-HERMES", "context references", "ELO Context", "provenance-bounded reference resolution"),
    ("EXT-CHECKPOINT-HERMES", "checkpoints", "ELO State Recovery", "pre-mutation checkpoint contract"),
    ("EXT-HOOK-HERMES", "event hooks", "ELO Workflow/Automation", "lifecycle evidence and guardrail hooks"),
    ("EXT-ROUTE-HERMES", "provider routing/fallback/credential pools", "ELO Model/Tool Routing", "policy-based bounded failover"),
    ("EXT-PROFILE-HERMES", "profiles/Bot Mode", "ELO Agent Context & Delegation", "isolated agent-context profiles"),
    ("EXT-BATCH-HERMES", "batch processing", "ELO Evaluation & Learning", "bounded batch evaluation intake"),
    ("EXT-MEMPROVIDER-HERMES", "external memory providers", "ELO Memory", "provider adapter without authority transfer"),
    ("EXT-LEARN-HERMES", "skill learning / /learn", "ELO Knowledge & Skills", "candidate skill synthesis with governed admission"),
    ("EXT-LEARNING-GRAPH-HERMES", "learning graph / curator", "ELO Evolution Memory", "evidence-linked learning relationships without autonomous promotion"),
    ("EXT-CONTEXT-PLUGIN-HERMES", "context engine plugins", "ELO Context", "bounded context-engine adapter behind existing context authority"),
    ("EXT-WORKTREE-HERMES", "isolated git worktrees", "ELO Forge", "isolated technical workspaces with governed merge"),
    ("EXT-MULTIAGENT-HERMES", "subagent delegation / parallel workstreams", "ELO Agent Delegation", "bounded delegated execution with evidence and authority limits"),
    ("EXT-CRON-HERMES", "scheduled agent tasks", "ELO Workflow/Automation", "deterministic scheduled invocation with ELO governance"),
)


@dataclass(frozen=True, slots=True)
class HermesCandidate:
    candidate_id: str
    mechanism: str
    owner: str
    adaptation: str
    evidence_state: str = "source_observed"
    promotion_state: str = "candidate_only"
    canonical_mutation: bool = False


@dataclass(frozen=True, slots=True)
class CandidateMeasurement:
    candidate_id: str
    baseline: Mapping[str, float]
    adapted: Mapping[str, float]
    regressions: tuple[str, ...]
    repeatable: bool
    result: str


def build_candidate(candidate_id: str) -> HermesCandidate:
    for item in CANDIDATES:
        if item[0] == candidate_id:
            return HermesCandidate(*item)
    raise ValueError(f"unknown Hermes candidate: {candidate_id}")


def evaluate_candidate(
    candidate: HermesCandidate,
    baseline: Mapping[str, float],
    adapted: Mapping[str, float],
    *,
    regressions: tuple[str, ...] = (),
    repeatable: bool = False,
    metric_directions: Mapping[str, str] | None = None,
) -> CandidateMeasurement:
    if candidate.promotion_state != "candidate_only" or candidate.canonical_mutation:
        return CandidateMeasurement(candidate.candidate_id, baseline, adapted, regressions, repeatable, "REJECT")
    common = baseline.keys() & adapted.keys()
    directions = metric_directions or {}
    gains = []
    for key in common:
        direction = directions.get(key)
        if direction not in {"maximize", "minimize"}:
            gains = []
            break
        delta = adapted[key] - baseline[key]
        if (direction == "maximize" and delta > 0) or (direction == "minimize" and delta < 0):
            gains.append(delta)
    if regressions:
        result = "REJECT"
    elif not gains or not repeatable:
        result = "RETEST"
    else:
        result = "EVOLUTION_GATE_REQUIRED"
    return CandidateMeasurement(candidate.candidate_id, baseline, adapted, regressions, repeatable, result)


__all__ = ["CANDIDATES", "CandidateMeasurement", "HermesCandidate", "build_candidate", "evaluate_candidate"]
