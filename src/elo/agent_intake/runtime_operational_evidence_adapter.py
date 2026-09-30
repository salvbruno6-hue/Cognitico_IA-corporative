"""Bridge runtime operational evidence into the existing functional-value contract.

This adapter does not authorize implementation. It converts repeated,
candidate-attributed runtime observations into the evidence shape already
consumed by the governed Hermes/ELO loop.

Runtime evidence proves an operational outcome only. Production proof remains
an explicit, separately governed evidence claim and is never inferred here.
"""

from __future__ import annotations

from elo.application.use_cases.orchestrator import AuthorizationDecision
from elo.core.execution_boundary import ExecutionOutcome, ExecutionStatus

from .hermes_functional_value_proof import FunctionalValueEvidence
from .runtime_operational_evidence import RuntimeOperationalEvidence, aggregate_repeatability


def validate_decision_pattern_execution_binding(
    *,
    observation: RuntimeOperationalEvidence,
    execution_outcome: ExecutionOutcome,
) -> tuple[bool, tuple[str, ...]]:
    """Validate the existing candidate provenance against a real execution.

    This is a validation boundary only. It does not authorize, execute,
    promote, or persist anything.
    """
    errors: list[str] = []

    if execution_outcome.status is not ExecutionStatus.EXECUTED or not execution_outcome.executed:
        errors.append("EXECUTION_NOT_COMPLETED")
    if execution_outcome.request_id != observation.execution_id:
        errors.append("EXECUTION_ID_MISMATCH")
    if not execution_outcome.decision_pattern_candidate_ref:
        errors.append("DECISION_PATTERN_PROVENANCE_MISSING")
    if not observation.decision_pattern_candidate_ref:
        errors.append("RUNTIME_EVIDENCE_PROVENANCE_MISSING")
    if (
        execution_outcome.decision_pattern_candidate_ref
        and observation.decision_pattern_candidate_ref
        and execution_outcome.decision_pattern_candidate_ref
        != observation.decision_pattern_candidate_ref
    ):
        errors.append("DECISION_PATTERN_PROVENANCE_MISMATCH")

    return not errors, tuple(errors)


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
    pattern_refs = {item.decision_pattern_candidate_ref for item in observations}
    if len(pattern_refs - {None}) > 1:
        raise ValueError("all observations must preserve the same decision pattern provenance")
    if None in pattern_refs and len(pattern_refs - {None}) > 0:
        raise ValueError("runtime observations must not mix bound and unbound decision pattern provenance")

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


def to_production_outcome(
    *,
    observations: tuple[RuntimeOperationalEvidence, ...],
    execution_outcomes: tuple[ExecutionOutcome, ...],
    authorizations: tuple[AuthorizationDecision, ...],
    candidate_id: str,
) -> FunctionalValueEvidence:
    """Admit production evidence only from externally authorized real executions.

    This function is an evidence adapter, not an authorization authority. It
    never executes work and never changes canonical state. Production status is
    accepted only when the external runtime explicitly reports environment=production
    and each execution is bound to a transport-valid elo-authz decision, the
    candidate, and its own runtime observation.
    """
    if not candidate_id:
        raise ValueError("candidate_id is required")
    if len(observations) < 2:
        raise ValueError("production evidence requires at least two observations")
    if len(execution_outcomes) != len(observations):
        raise ValueError("each runtime observation must have one execution outcome")
    if len(authorizations) != len(observations):
        raise ValueError("each runtime observation must have one authorization decision")

    execution_ids = tuple(item.execution_id for item in observations)
    if len(set(execution_ids)) != len(execution_ids):
        raise ValueError("production evidence requires distinct execution identities")

    for observation, outcome, authorization in zip(
        observations, execution_outcomes, authorizations, strict=True
    ):
        if observation.candidate_id != candidate_id:
            raise ValueError("all observations must belong to candidate_id")
        binding_valid, binding_errors = validate_decision_pattern_execution_binding(
            observation=observation,
            execution_outcome=outcome,
        )
        if (observation.decision_pattern_candidate_ref is not None or outcome.decision_pattern_candidate_ref is not None) and not binding_valid:
            raise ValueError("decision pattern provenance binding failed:" + ",".join(binding_errors))
        if outcome.status is not ExecutionStatus.EXECUTED or not outcome.executed:
            raise ValueError("production evidence requires successfully executed outcomes")
        if outcome.request_id != observation.execution_id:
            raise ValueError("execution outcome is not bound to runtime observation")
        if outcome.occurred_at is None:
            raise ValueError("production execution timestamp is required")
        if outcome.authorization_id != authorization.grant_id:
            raise ValueError("execution outcome is not bound to authorization grant")
        if authorization.resource_id != candidate_id:
            raise ValueError("authorization resource is not bound to candidate_id")
        if authorization.evidence_ref not in outcome.evidence_ids:
            raise ValueError("authorization evidence is not bound to execution evidence")
        if outcome.provenance.get("source_commit") and outcome.provenance.get("source_commit") != observation.provenance.commit:
            raise ValueError("execution source commit is not bound to runtime evidence")
        if not authorization.is_transport_valid(now=outcome.occurred_at):
            raise ValueError("authorization transport is not valid for production execution")
        if outcome.provenance.get("environment") != "production":
            raise ValueError("production evidence requires explicit production environment provenance")

    first = observations[0]
    if any(
        item.candidate_id != first.candidate_id
        or item.metric != first.metric
        or item.direction != first.direction
        or item.owner != first.owner
        or item.runtime_entrypoint != first.runtime_entrypoint
        for item in observations
    ):
        raise ValueError("production observations must share candidate, metric, owner and entrypoint")

    repeatability = aggregate_repeatability(observations)
    if repeatability.executions < 2 or repeatability.successful != repeatability.executions:
        raise ValueError("production repeatability is not established")

    return FunctionalValueEvidence(
        candidate_id=candidate_id,
        level="OPERATIONAL_OUTCOME",
        baseline=first.baseline,
        adapted=observations[-1].observed_value,
        metric=first.metric,
        direction=first.direction,
        repeatable=True,
        regressions=(),
        attribution="CANDIDATE_ATTRIBUTED",
        proof_scope=f"production runtime owner {first.owner}; {first.runtime_entrypoint}",
        provenance_refs=tuple(
            f"production:{item.execution_id}:{item.provenance.runtime_trace}"
            for item in observations
        ),
        production_proven=True,
    )


__all__ = [
    "to_operational_outcome",
    "to_production_outcome",
    "validate_decision_pattern_execution_binding",
]
