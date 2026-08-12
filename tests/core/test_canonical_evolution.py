from elo.core.canonical_identity import CanonicalIdentityRegistry, EloCanonicalIdentity
from elo.core.evolution_memory import EvolutionMemory, EvolutionRecord
from elo.core.knowledge_admission import AdmissionRequest, KnowledgeAdmission


def test_canonical_identity_is_read_only_and_architectural_changes_require_gate():
    identity = EloCanonicalIdentity(
        name="ELO",
        purpose="Enterprise cognitive platform",
        architecture_version="canonical",
        cognitive_core_path="src/elo/",
        principles=("experience does not redefine identity",),
        canonical_boundaries=("Context", "Knowledge", "Evidence", "Memory"),
        governance_policy="explicit architectural gate",
        current_verified_state="ELO-002",
        metadata={},
    )
    registry = CanonicalIdentityRegistry(identity)
    assert registry.get().name == "ELO"
    proposal = registry.propose_change("test architectural change")
    assert proposal["requires_governance_gate"] == "true"


def test_evolution_memory_requires_scope_and_provenance():
    memory = EvolutionMemory()
    record = EvolutionRecord(
        evolution_id="ev-1",
        tenant_id="tenant-a",
        domain="contracts",
        source_type="llm",
        source_id="gpt",
        content="candidate contract interpretation",
        provenance={"request_id": "req-1"},
    )
    assert memory.store(record) == record
    assert memory.list("tenant-a", "contracts") == [record]
    assert memory.list("tenant-b", "contracts") == []


def test_admission_keeps_authorized_non_decision_information_non_canonical():
    result = KnowledgeAdmission().evaluate(
        AdmissionRequest(
            tenant_id="tenant-a",
            domain="contracts",
            source_type="llm",
            source_id="gpt",
            content="exploratory analysis",
            provenance={"request_id": "req-1"},
            authorized=True,
            relevant=True,
            decision_relevant=False,
            evidence_available=False,
        )
    )
    assert result.outcome == "OBSERVATION"


def test_architecture_proposal_never_bypasses_governance():
    result = KnowledgeAdmission().evaluate(
        AdmissionRequest(
            tenant_id="tenant-a",
            domain="architecture",
            source_type="llm",
            source_id="claude",
            content="proposal",
            provenance={"request_id": "req-2"},
            authorized=True,
            relevant=True,
            architectural_change_proposed=True,
        )
    )
    assert result.outcome == "ARCHITECTURAL_PROPOSAL"
