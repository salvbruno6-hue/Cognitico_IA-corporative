"""Runtime evidence bridge for the governed Hermes tool-search capability.

This bridge executes the existing ExecutionRouter schema-search path and records
only facts observed at that runtime boundary. It does not execute a selected
tool, mutate canonical memory, authorize promotion, or aggregate repeatability.
Repeatability remains owned by RuntimeOperationalEvidenceCollector.
"""

from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.routing.execution_routing import ExecutionRouter
from .runtime_operational_evidence import (
    RuntimeOperationalEvidence,
    RepeatabilityEvidence,
    RuntimeProvenance,
    create_execution_id,
    create_runtime_evidence,
)

CANDIDATE_ID = "EXT-TOOL-SEARCH-HERMES"
OWNER = "ELO Model/Tool Routing"
RUNTIME_ENTRYPOINT = "ExecutionRouter.search_tool_schemas"
METRIC = "representation_footprint_chars"
DIRECTION = "minimize"


@dataclass(frozen=True, slots=True)
class ToolSearchRuntimeObservation:
    selection: object
    evidence: RuntimeOperationalEvidence


def search_tool_schemas_with_runtime_evidence(
    router: ExecutionRouter,
    query: str,
    tool_schemas: dict[str, str],
    *,
    baseline_representation_chars: float,
    source_commit: str,
    runtime_trace: str,
    execution_id: str | None = None,
    limit: int = 5,
) -> ToolSearchRuntimeObservation:
    """Run the real Router path and record one runtime observation.

    The caller must provide provenance and the baseline measured for this
    execution context. Repeatability is deliberately one execution; the
    canonical collector aggregates independent executions.
    """
    if baseline_representation_chars <= 0:
        raise ValueError("baseline_representation_chars must be > 0")

    selection = router.search_tool_schemas(query, tool_schemas, limit=limit)

    if selection.executed:
        raise RuntimeError("tool-search schema discovery must not execute a selected tool")
    if selection.canonical_mutation:
        raise RuntimeError("tool-search schema discovery must not mutate canonical memory")

    observed = float(selection.representation_chars)
    regression = observed >= baseline_representation_chars
    execution_id = execution_id or create_execution_id(CANDIDATE_ID)

    evidence = create_runtime_evidence(
        execution_id=execution_id,
        candidate_id=CANDIDATE_ID,
        owner=OWNER,
        runtime_entrypoint=RUNTIME_ENTRYPOINT,
        action_observed=True,
        metric=METRIC,
        direction=DIRECTION,
        baseline=float(baseline_representation_chars),
        observed_value=observed,
        attribution="candidate",
        provenance=RuntimeProvenance(
            commit=source_commit,
            runtime_trace=runtime_trace,
        ),
        regression=regression,
        repeatability=RepeatabilityEvidence(
            executions=1,
            successful=1 if not regression else 0,
            rate=1.0 if not regression else 0.0,
        ),
    )

    return ToolSearchRuntimeObservation(selection=selection, evidence=evidence)
