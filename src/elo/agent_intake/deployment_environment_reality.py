"""Fail-closed contract for proving that a deployment environment is real.

This module separates declared configuration from observed deployment/runtime
evidence. It never treats source files, CI success, mocks, or configuration
alone as proof that an environment was deployed or executed.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DeploymentRealityStatus(StrEnum):
    NOT_DECLARED = "NOT_DECLARED"
    DECLARED_ONLY = "DECLARED_ONLY"
    ARTIFACT_VERIFIED = "ARTIFACT_VERIFIED"
    RUNTIME_VERIFIED = "RUNTIME_VERIFIED"
    OPERATIONALLY_VERIFIED = "OPERATIONALLY_VERIFIED"
    PRODUCTION_PROVEN = "PRODUCTION_PROVEN"


@dataclass(frozen=True)
class DeploymentEnvironmentEvidence:
    environment_id: str
    environment_kind: str
    deployment_id: str = ""
    commit_sha: str = ""
    artifact_ref: str = ""
    runtime_endpoint: str = ""
    healthcheck_ref: str = ""
    runtime_observed: bool = False
    operational_observed: bool = False
    production_outcome_observed: bool = False
    governance_approved: bool = False
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class DeploymentRealityAssessment:
    status: DeploymentRealityStatus
    reasons: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    deployment_proven: bool = False
    runtime_proven: bool = False
    production_proven: bool = False


def assess_deployment_reality(
    evidence: DeploymentEnvironmentEvidence | None,
) -> DeploymentRealityAssessment:
    """Classify deployment reality without inferring missing evidence."""
    if evidence is None:
        return DeploymentRealityAssessment(
            DeploymentRealityStatus.NOT_DECLARED,
            ("deployment environment evidence is absent",),
            (),
        )

    if not evidence.environment_id or not evidence.environment_kind:
        return DeploymentRealityAssessment(
            DeploymentRealityStatus.NOT_DECLARED,
            ("environment identity and kind are required",),
            evidence.evidence_refs,
        )

    if not evidence.deployment_id or not evidence.commit_sha or not evidence.artifact_ref:
        return DeploymentRealityAssessment(
            DeploymentRealityStatus.DECLARED_ONLY,
            ("deployment id, commit sha and artifact reference are required",),
            evidence.evidence_refs,
        )

    if not evidence.evidence_refs:
        return DeploymentRealityAssessment(
            DeploymentRealityStatus.DECLARED_ONLY,
            ("independent deployment evidence reference is required",),
            (),
        )

    if not evidence.runtime_observed or not evidence.runtime_endpoint or not evidence.healthcheck_ref:
        return DeploymentRealityAssessment(
            DeploymentRealityStatus.ARTIFACT_VERIFIED,
            ("runtime observation, endpoint and healthcheck evidence are required",),
            evidence.evidence_refs,
            deployment_proven=True,
        )

    if not evidence.operational_observed:
        return DeploymentRealityAssessment(
            DeploymentRealityStatus.RUNTIME_VERIFIED,
            ("operational observation is required before operational verification",),
            evidence.evidence_refs,
            deployment_proven=True,
            runtime_proven=True,
        )

    if not evidence.production_outcome_observed or not evidence.governance_approved:
        return DeploymentRealityAssessment(
            DeploymentRealityStatus.OPERATIONALLY_VERIFIED,
            ("production outcome and explicit governance approval are required for production proof",),
            evidence.evidence_refs,
            deployment_proven=True,
            runtime_proven=True,
        )

    return DeploymentRealityAssessment(
        DeploymentRealityStatus.PRODUCTION_PROVEN,
        (),
        evidence.evidence_refs,
        deployment_proven=True,
        runtime_proven=True,
        production_proven=True,
    )
