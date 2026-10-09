from decimal import Decimal

import pytest

from elo.application.queries.okr_evidence import OkrEvidenceResolver
from elo.contracts.okr import KeyResult, KeyResultDirection
from elo.evidence import Evidence, EvidenceAccessError, EvidenceRepository


def _save(repository: EvidenceRepository, *, tenant_id: str, claim: str) -> Evidence:
    return repository.save(
        Evidence.create(
            tenant_id=tenant_id,
            domain="strategy",
            source_type="test",
            source_id=claim,
            claim=claim,
            content_ref=f"test://{claim}",
        )
    )


def _kr(*, baseline_refs=(), target_refs=()):
    return KeyResult(
        tenant_id="tenant-a",
        key_result_id="KR-1",
        objective_id="OBJ-1",
        title="Reduce lead time",
        metric_code="KPI-LEAD-TIME",
        direction=KeyResultDirection.DECREASE,
        baseline=Decimal("15") if baseline_refs else None,
        target=Decimal("10") if target_refs else None,
        baseline_evidence_refs=baseline_refs,
        target_evidence_refs=target_refs,
    )


def test_no_refs_remains_sem_dado():
    resolver = OkrEvidenceResolver(EvidenceRepository())

    state = resolver.resolve_refs(tenant_id="tenant-a", evidence_refs=())

    assert state.state == "SEM_DADO"
    assert state.evidence == ()


def test_all_refs_resolve_as_comprovado():
    repository = EvidenceRepository()
    baseline = _save(repository, tenant_id="tenant-a", claim="baseline")
    resolver = OkrEvidenceResolver(repository)

    state = resolver.key_result_baseline(_kr(baseline_refs=(baseline.evidence_id,)))

    assert state.state == "COMPROVADO"
    assert state.evidence[0].evidence_id == baseline.evidence_id
    assert state.missing_refs == ()


def test_partial_and_missing_refs_are_explicit():
    repository = EvidenceRepository()
    observed = _save(repository, tenant_id="tenant-a", claim="target")
    resolver = OkrEvidenceResolver(repository)

    state = resolver.resolve_refs(
        tenant_id="tenant-a",
        evidence_refs=(observed.evidence_id, "ev:missing"),
    )

    assert state.state == "PARCIAL"
    assert state.missing_refs == ("ev:missing",)


def test_cross_tenant_evidence_never_resolves_silently():
    repository = EvidenceRepository()
    other = _save(repository, tenant_id="tenant-b", claim="other-tenant")
    resolver = OkrEvidenceResolver(repository)

    with pytest.raises(EvidenceAccessError):
        resolver.resolve_refs(
            tenant_id="tenant-a",
            evidence_refs=(other.evidence_id,),
        )
