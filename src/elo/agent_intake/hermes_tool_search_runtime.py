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
    RuntimeProvenance,
    RepeatabilityEvidence,
    create_execution_id,
)

CANDIDATE_ID = "EXT-TOOL-SEARCH-HERMES"
OWNER = "ELO Model/Tool Routing"
RUNTIME_ENTRYPOINT = "ExecutionRouter.search_tool_schemas"


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
    execution context. Repeatability is deliberately set to one execution;
    the collector must aggregate independent executions before operational
    outcome is evaluated.
    """
    if not source_commit.strip():
        raise ValueError("source_commit is required")
    if not runtime_trace.strip():
        raise ValueError("runtime_trace is required")
    if baseline_representation_chars <= 0:
        raise ValueError("baseline_representation_chars must be > 0")

    selection = router.search_tool_schemas(query, tool_schemas, limit=limit)

    if selection.executed:
        raise RuntimeError("tool-search schema discovery must not execute a selected tool")
    if selection.canonical_mutation:
        raise RuntimeError("tool-search schema discovery must not mutate canonical memory")

    execution_id = execution_id or create_execution_id(CANDIDATE_ID)
    observed = float(selection.representation_chars)
    regression = observed >= baseline_representation_chars

    evidence = RuntimeOperationalEvidence(
        execution_id=execution_id,
        candidate_id=CANDIDATE_ID,
        owner=OWNER,
        runtime_entrypoint=RUNTIME_ENTRYPOINT,
        timestamp=__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        action_observed=True,
        metric="representation_footprint_chars",
        direction="minimize",
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
        evidence_hash="",
    )

    from dataclasses import replace
    from hashlib import sha256

    payload = "|".join(
        (
            evidence.execution_id,
            evidence.candidate_id,
            evidence.owner,
            evidence.runtime_entrypoint,
            evidence.timestamp,
            evidence.metric,
            evidence.direction,
            str(evidence.baseline),
            str(evidence.observed_value),
            evidence.attribution,
            evidence.provenance.commit,
            evidence.provenance.runtime_trace,
            str(evidence.regression),
            str(evidence.repeatability.executions),
            str(evidence.repeatability.successful),
        )
    )
    evidence = replace(evidence, evidence_hash=sha256(payload.encode("utf-8")).hexdigest())

    return ToolSearchRuntimeObservation(selection=selection, evidence=evidence)
