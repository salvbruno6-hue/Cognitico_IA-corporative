from elo.agent_intake.deployment_environment_reality import (
    DeploymentEnvironmentEvidence,
    DeploymentRealityStatus,
    assess_deployment_reality,
)


def _evidence(**overrides):
    values = dict(
        environment_id="elo-web-prod",
        environment_kind="vercel-production",
        deployment_id="dep-123",
        commit_sha="abc123",
        artifact_ref="artifact:elo-web",
        runtime_endpoint="https://example.invalid/health",
        healthcheck_ref="healthcheck:123",
        runtime_observed=True,
        operational_observed=True,
        production_outcome_observed=False,
        governance_approved=False,
        evidence_refs=("deployment:123", "runtime:123"),
    )
    values.update(overrides)
    return DeploymentEnvironmentEvidence(**values)


def test_absent_environment_is_not_proven():
    result = assess_deployment_reality(None)
    assert result.status is DeploymentRealityStatus.NOT_DECLARED
    assert result.deployment_proven is False
    assert result.production_proven is False


def test_declaration_alone_is_not_deployment_proof():
    result = assess_deployment_reality(
        DeploymentEnvironmentEvidence(
            environment_id="elo-web-prod",
            environment_kind="vercel-production",
        )
    )
    assert result.status is DeploymentRealityStatus.DECLARED_ONLY
    assert result.deployment_proven is False


def test_artifact_evidence_is_not_runtime_proof():
    result = assess_deployment_reality(
        _evidence(runtime_observed=False, runtime_endpoint="", healthcheck_ref="")
    )
    assert result.status is DeploymentRealityStatus.ARTIFACT_VERIFIED
    assert result.deployment_proven is True
    assert result.runtime_proven is False
    assert result.production_proven is False


def test_runtime_observation_is_not_production_proof():
    result = assess_deployment_reality( _evidence(operational_observed=False) )
    assert result.status is DeploymentRealityStatus.RUNTIME_VERIFIED
    assert result.runtime_proven is True
    assert result.production_proven is False


def test_operational_observation_still_requires_governance_for_production():
    result = assess_deployment_reality(_evidence())
    assert result.status is DeploymentRealityStatus.OPERATIONALLY_VERIFIED
    assert result.production_proven is False


def test_production_proof_requires_observed_outcome_and_governance():
    result = assess_deployment_reality(
        _evidence(production_outcome_observed=True, governance_approved=True)
    )
    assert result.status is DeploymentRealityStatus.PRODUCTION_PROVEN
    assert result.production_proven is True


def test_ci_or_configuration_refs_cannot_replace_deployment_evidence():
    result = assess_deployment_reality(
        _evidence(
            deployment_id="",
            evidence_refs=("ci:success", "config:vercel"),
        )
    )
    assert result.status is DeploymentRealityStatus.DECLARED_ONLY
    assert result.deployment_proven is False
