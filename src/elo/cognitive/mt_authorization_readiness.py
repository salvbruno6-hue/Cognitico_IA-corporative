"""Read-only MT authorization readiness reasoning for the ELO Symbiont.

This module converts explicit live authorization/data signals into granular
system-health findings. It never assigns identities, scopes, roles,
capabilities, tenants, rewrites RLS, or authorizes a migration.
"""
from __future__ import annotations

from dataclasses import dataclass

from elo.cognitive.system_health_assessment import HealthSeverity, SystemHealthFinding


@dataclass(frozen=True, slots=True)
class MTAuthorizationSignals:
    eligible_google_identities: int
    enterprise_multiteiner_links: int
    identities_with_domain_scope: int
    identities_with_pcp_capability: int
    fully_ready_identities: int
    tenant_rows: int
    direct_tenant_tables: int
    estimated_populated_tables: int
    unverified_populated_tables: int
    repair_rows: int
    repair_rows_with_tenant: int
    legacy_policy_objects: int
    legacy_tables: int
    evidence_ref: str = "supabase/health/elo_mt_authorization_readiness.sql"

    def __post_init__(self) -> None:
        values = (
            self.eligible_google_identities,
            self.enterprise_multiteiner_links,
            self.identities_with_domain_scope,
            self.identities_with_pcp_capability,
            self.fully_ready_identities,
            self.tenant_rows,
            self.direct_tenant_tables,
            self.estimated_populated_tables,
            self.unverified_populated_tables,
            self.repair_rows,
            self.repair_rows_with_tenant,
            self.legacy_policy_objects,
            self.legacy_tables,
        )
        if any(value < 0 for value in values):
            raise ValueError("MT authorization signals cannot be negative")
        if self.repair_rows_with_tenant > self.repair_rows:
            raise ValueError("tenant-covered repair rows cannot exceed total repair rows")
        if self.estimated_populated_tables > self.direct_tenant_tables:
            raise ValueError("populated tenant tables cannot exceed direct tenant tables")
        if self.unverified_populated_tables > self.estimated_populated_tables:
            raise ValueError("unverified populated tables cannot exceed populated tables")
        if not self.evidence_ref.strip():
            raise ValueError("evidence_ref is required")


@dataclass(frozen=True, slots=True)
class MTAuthorizationReadiness:
    findings: tuple[SystemHealthFinding, ...]
    next_required_condition: str | None
    operator_ready: bool
    tenant_data_ready: bool
    ready_for_policy_rewrite: bool
    canonical_mutation: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "next_required_condition": self.next_required_condition,
            "operator_ready": self.operator_ready,
            "tenant_data_ready": self.tenant_data_ready,
            "ready_for_policy_rewrite": self.ready_for_policy_rewrite,
            "canonical_mutation": self.canonical_mutation,
            "findings": [item.finding_id for item in self.findings],
        }


def _finding(
    *,
    finding_id: str,
    dimension: str,
    passed: bool,
    weight: float,
    owner: str,
    evidence_ref: str,
    detail: str,
) -> SystemHealthFinding:
    return SystemHealthFinding(
        finding_id=finding_id,
        dimension=dimension,
        severity=HealthSeverity.PASS if passed else HealthSeverity.GAP_HIGH,
        weight=weight,
        evidence_refs=(evidence_ref,),
        detail=detail,
        owner=owner,
    )


def assess_mt_authorization_readiness(
    signals: MTAuthorizationSignals,
) -> MTAuthorizationReadiness:
    """Evaluate prerequisite order without granting or inferring authority."""
    repair_coverage_ready = signals.tenant_rows > 0 and (
        signals.repair_rows == 0 or signals.repair_rows_with_tenant == signals.repair_rows
    )
    all_populated_tenant_tables_verified = signals.unverified_populated_tables == 0

    checks = (
        (
            "MT_AUTHZ_IDENTITY_BOUND",
            signals.eligible_google_identities > 0,
            "eligible_google_identity",
            "authorization",
            7.0,
            "elo-authz",
            f"eligible_google_identities={signals.eligible_google_identities}",
        ),
        (
            "MT_AUTHZ_ENTERPRISE_SCOPE",
            signals.enterprise_multiteiner_links > 0,
            "enterprise_multiteiner_scope",
            "authorization",
            6.0,
            "elo-authz",
            f"enterprise_multiteiner_links={signals.enterprise_multiteiner_links}",
        ),
        (
            "MT_AUTHZ_DOMAIN_SCOPE",
            signals.identities_with_domain_scope > 0,
            "domain_scope",
            "authorization",
            5.0,
            "elo-authz",
            f"identities_with_domain_scope={signals.identities_with_domain_scope}",
        ),
        (
            "MT_AUTHZ_PCP_CAPABILITY",
            signals.identities_with_pcp_capability > 0,
            "pcp_capability",
            "authorization",
            4.0,
            "elo-authz",
            f"identities_with_pcp_capability={signals.identities_with_pcp_capability}",
        ),
        (
            "MT_AUTHZ_FULL_OPERATOR",
            signals.fully_ready_identities > 0,
            "fully_ready_operator",
            "authorization",
            3.0,
            "elo-authz",
            f"fully_ready_identities={signals.fully_ready_identities}",
        ),
        (
            "MT_TENANT_REGISTRY",
            signals.tenant_rows > 0,
            "tenant_registry",
            "data_governance",
            3.0,
            "mt-data-governance",
            f"tenant_rows={signals.tenant_rows}",
        ),
        (
            "MT_TENANT_POPULATED_TABLES_VERIFIED",
            all_populated_tenant_tables_verified,
            "verify_all_populated_tenant_tables",
            "data_governance",
            2.5,
            "mt-data-governance",
            (
                f"direct_tenant_tables={signals.direct_tenant_tables} "
                f"estimated_populated_tables={signals.estimated_populated_tables} "
                f"unverified_populated_tables={signals.unverified_populated_tables}"
            ),
        ),
        (
            "MT_REPAIR_TENANT_COVERAGE",
            repair_coverage_ready,
            "repair_tenant_coverage",
            "data_governance",
            2.0,
            "mt-data-governance",
            (
                f"repair_rows={signals.repair_rows} "
                f"repair_rows_with_tenant={signals.repair_rows_with_tenant}"
            ),
        ),
    )

    findings = tuple(
        _finding(
            finding_id=finding_id,
            dimension=dimension,
            passed=passed,
            weight=weight,
            owner=owner,
            evidence_ref=signals.evidence_ref,
            detail=detail,
        )
        for finding_id, passed, _condition, dimension, weight, owner, detail in checks
    )

    legacy_clear = signals.legacy_policy_objects == 0
    findings += (
        _finding(
            finding_id="MT_LEGACY_LITERAL_TRUE_SURFACE",
            dimension="authorization",
            passed=legacy_clear,
            weight=3.0,
            owner="elo-authz",
            evidence_ref=signals.evidence_ref,
            detail=(
                f"legacy_policy_objects={signals.legacy_policy_objects} "
                f"legacy_tables={signals.legacy_tables}"
            ),
        ),
    )

    next_required_condition = next(
        (condition for _id, passed, condition, _dimension, _weight, _owner, _detail in checks if not passed),
        None,
    )
    operator_ready = signals.fully_ready_identities > 0
    tenant_data_ready = (
        signals.tenant_rows > 0
        and all_populated_tenant_tables_verified
        and repair_coverage_ready
    )
    return MTAuthorizationReadiness(
        findings=findings,
        next_required_condition=next_required_condition,
        operator_ready=operator_ready,
        tenant_data_ready=tenant_data_ready,
        ready_for_policy_rewrite=operator_ready and tenant_data_ready,
    )


__all__ = [
    "MTAuthorizationReadiness",
    "MTAuthorizationSignals",
    "assess_mt_authorization_readiness",
]
