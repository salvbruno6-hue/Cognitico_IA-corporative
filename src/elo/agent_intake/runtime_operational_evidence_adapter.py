"""Bridge runtime operational evidence into the existing functional-value contract.

This adapter does not authorize implementation. It converts repeated,
candidate-attributed runtime observations into the evidence shape already
consumed by the governed Hermes/ELO loop.

Runtime evidence proves an operational outcome only. Production proof remains
an explicit, separately governed evidence claim and is never inferred here.
"""

from __future__ import annotations

from .hermes_functional_value_proof import FunctionalValueEvidence
from .runtime_operational_evidence import RuntimeOperationalEvidence, aggregate_repeatability


def to_operational_outcome(
    observations: tuple[RuntimeOperationalEvidence, ...],
) -> FunctionalValueEvidence:
    if not observations:
        raise ValueError("at least one runtime observation is required")

    first = observations[0]
    execution_ids = tuple(item.execution_id for item in observations)
    if len(set(execution_ids)) != len(execution_ids):
        raise ValueError("runtime observations must have distinct execution_id values")
    if any(item.candidate_id != first.candidate_id for item in observations):
        raise ValueError("all observations must belong to the same candidate")
    if any(item.metric != first.metric for item in observations):
        raise ValueError("all observations must use the same metric")
    if any(item.direction != first.direction for item in observations):
        raise ValueError("all observations must use the same metric direction")
    if any(item.owner != first.owner for item in observations):
        raise ValueError("all observations must belong to the same owner")
    if any(item.runtime_entrypoint != first.runtime_entrypoint for item in observations):
        raise ValueError("all observations must use the same runtime entrypoint")

    repeatability = aggregate_repeatability(observations)
    provenance = tuple(
        f"runtime:{item.execution_id}:{item.provenance.runtime_trace}"
        for item in observations
    )
    operational = (
        repeatability.executions >= 2
        and repeatability.successful == repeatability.executions
        and all(
            item.action_observed
            and item.attribution == "candidate"
            and bool(item.provenance.commit)
            and bool(item.provenance.runtime_trace)
            and not item.regression
            for item in observations
        )
    )

    return FunctionalValueEvidence(
        candidate_id=first.candidate_id,
        level="OPERATIONAL_OUTCOME" if operational else "FUNCTIONAL_CONTROLLED_GAIN",
        baseline=first.baseline,
        adapted=first.observed_value,
        metric=first.metric,
        direction=first.direction,
        repeatable=operational,
        regressions=tuple(
            sorted(
                {
                    reason
                    for item in observations
                    for reason in (("REGRESSION_DETECTED",) if item.regression else ())
                }
            )
        ),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope=f"runtime owner {first.owner}; {first.runtime_entrypoint}",
        provenance_refs=provenance,
        production_proven=False,
    )


__all__ = ["to_operational_outcome"]
