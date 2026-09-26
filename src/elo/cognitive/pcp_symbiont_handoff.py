"""PCP-to-Symbiont canonical observation translator.

The canonical laboratory contract requires experiment, regression,
generalization and risk fields. PCP does not infer those fields; callers must
provide them as explicit evidence-bearing inputs.
"""

from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.symbionte_lab import SymbiontLabObservation

from .pcp_operational_evidence import PCPOperationalEvidencePackage


@dataclass(frozen=True)
class PCPSymbiontHandoff:
    observation: SymbiontLabObservation
    source_package: PCPOperationalEvidencePackage


def prepare_pcp_symbiont_handoff(
    package: PCPOperationalEvidencePackage,
    *,
    tenant_id: str,
    decision_id: str,
    observation_id: str,
    source_ref: str,
    source_commit: str,
    hypothesis: str,
    baseline: str,
    experiment: str,
    result: str,
    regression_status: str,
    generalization_status: str,
    risk: str,
    scope: str = "PCP",
) -> PCPSymbiontHandoff:
    if not package.evidence_ids:
        raise ValueError("PCP Symbiont handoff requires evidence")
    observation = SymbiontLabObservation(
        observation_id=observation_id,
        tenant_id=tenant_id,
        domain="PCP",
        decision_id=decision_id,
        expected_outcome=str(package.diagnosis.status),
        observed_outcome=(
            f"total={package.diagnosis.total};"
            f"confronted={package.diagnosis.confronted};"
            f"not_located={package.diagnosis.not_located}"
        ),
        evidence_ids=package.evidence_ids,
        source_ref=source_ref,
        source_commit=source_commit,
        hypothesis=hypothesis,
        baseline=baseline,
        experiment=experiment,
        result=result,
        regression_status=regression_status,
        generalization_status=generalization_status,
        risk=risk,
        existing_owner="SKILL_PLANEJAMENTO_MULTITEINER",
        scope=scope,
        tenant_scope=tenant_id,
        source_kind=package.source_kind,
    )
    return PCPSymbiontHandoff(
        observation=observation,
        source_package=package,
    )
