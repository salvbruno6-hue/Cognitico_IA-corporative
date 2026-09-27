"""Bridge runtime operational evidence into the existing functional-value contract.

This adapter does not authorize implementation. It only converts repeated,
candidate-attributed runtime observations into the evidence shape already
consumed by the governed Hermes/ELO loop.
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
    if any(item.candidate_id != first.candidate_id for item in observations):
        raise ValueError("all observations must belong to the same candidate")
    if any(item.metric != first.metric for item in observations):
        raise ValueError("all observations must use the same metric")
    if any(item.direction != first.direction for item in observations):
        raise ValueError("all observations must use the same metric direction")
    if any(item.owner != first.owner for item in observations):
        raise ValueError("all observations must belong to the same owner")

    repeatability = aggregate_repeatability(observations)
    provenance = tuple(
        f"runtime:{item.execution_id}:{item.provenance.runtime_trace}"
        for item in observations
    )
    operational = (
        repeatability.executions >= 2
        and repeatability.successful == repeatability.executions
        and all(item.operational_outcome_proven for item in observations)
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
            sorted({reason for item in observations for reason in (
                ("REGRESSION_DETECTED",) if item.regression else ()
            )})
        ),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope=f"runtime owner {first.owner}; {first.runtime_entrypoint}",
        provenance_refs=provenance,
        production_proven=operational,
    )


__all__ = ["to_operational_outcome"]
