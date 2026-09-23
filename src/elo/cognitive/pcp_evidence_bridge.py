"""PCP evidence bridge to the canonical Symbiont runtime.

This module is the only PCP-side integration boundary. The analytical PCP kernel
does not import Symbiont components and remains executable independently.

Architecture:
    PCP / Comercial / Engenharia
              |
           EVIDENCIA
              |
           SYMBIONT
          /        \
      aprender   adaptar
          \        /
        EVOLUTION GATE

The bridge does not create a new lifecycle, memory, adapter, router or gate.
It only translates PCP evidence into the canonical Symbiont observation and
delegates governance to the existing runtime.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from elo.core.decision_outcome_loop import DecisionLifecycle
from .symbiont_skill_runtime import SymbiontSkillRuntime
from .symbionte_lab import SymbiontLabObservation


def prepare_symbiont_evidence(
    *,
    request_id: str,
    source_ref: str,
    source_commit: str,
    evidence_ids: Sequence[str],
    baseline: str,
    experiment: str,
    result: str,
    expected_outcome: str,
    observed_outcome: str,
    regression_status: str,
    generalization_status: str,
    existing_owner: str,
    scope: str,
    tenant_id: str = "pcp",
    domain: str = "PCP",
) -> dict[str, object]:
    """Translate domain evidence into the canonical Symbiont observation shape.

    No adapter call and no persistence happen here.
    """
    return {
        "observation_id": request_id,
        "tenant_id": tenant_id,
        "domain": domain,
        "decision_id": request_id,
        "expected_outcome": expected_outcome,
        "observed_outcome": observed_outcome,
        "evidence_ids": tuple(evidence_ids),
        "source_ref": source_ref,
        "source_commit": source_commit,
        "hypothesis": result,
        "baseline": baseline,
        "experiment": experiment,
        "result": result,
        "regression_status": regression_status,
        "generalization_status": generalization_status,
        "risk": "LOW",
        "existing_owner": existing_owner,
        "scope": scope,
        "tenant_scope": tenant_id,
        "source_kind": "benchmark",
    }


def handoff_symbiont_evidence(
    lifecycle: DecisionLifecycle,
    *,
    adapter: object,
    evidence_payload: Mapping[str, object],
    principal_id: str,
    dataset_version: str,
):
    """Send domain evidence through the existing canonical Symbiont handoff."""
    observation = SymbiontLabObservation(
        observation_id=str(evidence_payload["observation_id"]),
        tenant_id=str(evidence_payload["tenant_id"]),
        domain=str(evidence_payload["domain"]),
        decision_id=str(evidence_payload["decision_id"]),
        expected_outcome=str(evidence_payload["expected_outcome"]),
        observed_outcome=str(evidence_payload["observed_outcome"]),
        evidence_ids=tuple(evidence_payload["evidence_ids"]),
        source_ref=str(evidence_payload["source_ref"]),
        source_commit=str(evidence_payload["source_commit"]),
        hypothesis=str(evidence_payload["hypothesis"]),
        baseline=str(evidence_payload["baseline"]),
        experiment=str(evidence_payload["experiment"]),
        result=str(evidence_payload["result"]),
        regression_status=str(evidence_payload["regression_status"]),
        generalization_status=str(evidence_payload["generalization_status"]),
        risk=str(evidence_payload["risk"]),
        existing_owner=str(evidence_payload["existing_owner"]),
        scope=str(evidence_payload["scope"]),
        tenant_scope=(
            str(evidence_payload["tenant_scope"])
            if evidence_payload.get("tenant_scope") is not None
            else None
        ),
        source_kind=(
            str(evidence_payload["source_kind"])
            if evidence_payload.get("source_kind") is not None
            else None
        ),
    )
    return SymbiontSkillRuntime.handoff_decision(
        lifecycle,
        adapter=adapter,
        observation=observation,
        principal_id=principal_id,
        dataset_version=dataset_version,
    )
