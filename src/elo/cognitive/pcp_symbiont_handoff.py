"""PCP-to-Symbiont governed handoff payload.

This is a translation boundary only. It prepares the canonical observation
shape for the existing Symbiont lifecycle; it does not execute the lifecycle,
persist observations, learn, or promote capabilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .pcp_operational_evidence import PCPOperationalEvidencePackage


@dataclass(frozen=True)
class PCPSymbiontHandoff:
    observation: dict[str, Any]
    source_package: PCPOperationalEvidencePackage


def prepare_pcp_symbiont_handoff(
    package: PCPOperationalEvidencePackage,
    *,
    tenant_id: str,
    decision_id: str,
    observation_id: str,
    source_commit: str | None = None,
) -> PCPSymbiontHandoff:
    """Translate PCP evidence into the existing observation vocabulary."""
    diagnosis = package.diagnosis
    observation = {
        "observation_id": observation_id,
        "tenant_id": tenant_id,
        "domain": "PCP",
        "decision_id": decision_id,
        "expected_outcome": {
            "diagnosis_status": diagnosis.status,
            "confronted": diagnosis.confronted,
            "not_located": diagnosis.not_located,
        },
        "observed_outcome": {
            "total": diagnosis.total,
            "dimensions": diagnosis.dimensions,
            "impact": diagnosis.impact,
        },
        "evidence_ids": list(package.evidence_ids),
        "source_ref": package.source_ref,
        "source_commit": source_commit,
        "hypothesis": None,
        "baseline": {
            "confrontations": len(package.confrontations),
        },
        "experiment": None,
        "result": {
            "status": diagnosis.status,
            "confronted": diagnosis.confronted,
            "not_located": diagnosis.not_located,
        },
        "regression_status": None,
        "generalization_status": None,
        "risk": None,
        "existing_owner": "SKILL_PLANEJAMENTO_MULTITEINER",
        "scope": "PCP",
        "tenant_scope": tenant_id,
        "source_kind": package.source_kind,
    }
    return PCPSymbiontHandoff(
        observation=observation,
        source_package=package,
    )
