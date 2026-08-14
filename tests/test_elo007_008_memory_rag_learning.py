import pytest

from elo.core.learning_governance import GovernedLearningService, LearningGovernanceError
from elo.knowledge.rag import GovernedRetriever
from elo.memory.persistent import MemoryAdmissionError, PersistentMemoryStore


def test_persistent_memory_round_trip_and_tenant_isolation():
    store = PersistentMemoryStore()
    record = store.remember(
        tenant_id="tenant-a",
        domain="finance",
        principal_id="manager-a",
        content="invoice payment mismatch requires reconciliation",
        source_id="erp-001",
        provenance={"request_id": "req-1"},
    )
    assert store.get(record.memory_id, tenant_id="tenant-a", domain="finance") == record
    assert store.get(record.memory_id, tenant_id="tenant-b", domain="finance") is None
    assert store.search("invoice reconciliation", tenant_id="tenant-b", domain="finance") == []
    store.close()


def test_memory_admission_requires_governance_context():
    store = PersistentMemoryStore()
    with pytest.raises(MemoryAdmissionError):
        store.remember(
            tenant_id="tenant-a",
            domain="finance",
            principal_id="manager-a",
            content="x",
            source_id="source",
            provenance={},
        )
    store.close()


def test_rag_context_contains_only_scoped_evidence_and_citations():
    store = PersistentMemoryStore()
    store.remember(
        tenant_id="tenant-a",
        domain="production",
        principal_id="manager-a",
        content="forklift route crosses uneven floor",
        source_id="maintenance-01",
        provenance={"request_id": "req-2"},
    )
    store.remember(
        tenant_id="tenant-a",
        domain="hr",
        principal_id="manager-a",
        content="forklift training policy",
        source_id="hr-01",
        provenance={"request_id": "req-3"},
    )
    context = GovernedRetriever(store).build_context(
        "forklift floor", tenant_id="tenant-a", domain="production"
    )
    assert context.sufficient is True
    assert len(context.evidence) == 1
    assert context.evidence[0].source_id == "maintenance-01"
    assert context.citations == (context.evidence[0].evidence_id,)
    store.close()


def test_rag_reports_no_verified_evidence():
    store = PersistentMemoryStore()
    context = GovernedRetriever(store).build_context(
        "unknown issue", tenant_id="tenant-a", domain="production"
    )
    assert context.sufficient is False
    assert GovernedRetriever.prompt_context(context) == "NO_VERIFIED_EVIDENCE_AVAILABLE"
    store.close()


def test_learning_requires_threshold_and_human_approval():
    store = PersistentMemoryStore()
    service = GovernedLearningService(store)
    experience = service.capture_outcome(
        tenant_id="tenant-a",
        domain="finance",
        principal_id="manager-a",
        decision_id="decision-1",
        expected_outcome="invoice reconciled",
        observed_outcome="invoice reconciled",
        evidence_ids=("evidence-1",),
    )
    candidate = service.propose_candidate(
        experience, dataset_version="dataset-1", hypothesis="reconciliation rule is reusable"
    )
    evaluation = service.evaluate(
        candidate, metric="precision", score=0.9, threshold=0.8, evaluator="offline-suite"
    )
    with pytest.raises(LearningGovernanceError):
        service.approve_for_promotion(candidate, evaluation, human_approved=False)
    approved = service.approve_for_promotion(candidate, evaluation, human_approved=True)
    assert approved.state == "APPROVED"
    store.close()


def test_learning_below_threshold_cannot_promote():
    store = PersistentMemoryStore()
    service = GovernedLearningService(store)
    experience = service.capture_outcome(
        tenant_id="tenant-a",
        domain="pcp",
        principal_id="manager-a",
        decision_id="decision-2",
        expected_outcome="delay reduced",
        observed_outcome="delay unchanged",
        evidence_ids=("evidence-2",),
    )
    candidate = service.propose_candidate(
        experience, dataset_version="dataset-2", hypothesis="capacity adjustment helps"
    )
    evaluation = service.evaluate(
        candidate, metric="f1", score=0.5, threshold=0.8, evaluator="offline-suite"
    )
    with pytest.raises(LearningGovernanceError):
        service.approve_for_promotion(candidate, evaluation, human_approved=True)
    store.close()
