import pytest

from elo.cognitive.symbionte_lab import SymbiontLabAdapter, SymbiontLabObservation
from elo.core.evolution_gate import EvolutionGate
from elo.core.learning_governance import GovernedLearningService, PromotionPackage


class MemoryStub:
    def __init__(self):
        self.calls = []

    def remember(self, **kwargs):
        self.calls.append(kwargs)


def make_observation(**overrides):
    values = dict(
        observation_id="lab-adjust-001",
        tenant_id="tenant-a",
        domain="ORCAMENTO",
        decision_id="decision-1",
        expected_outcome="resultado reproduzivel",
        observed_outcome="resultado reproduzivel",
        evidence_ids=("e-1", "e-2"),
        source_ref="pr:lab-adjustments",
        source_commit="HEAD",
        hypothesis="ajuste governado melhora resultado",
        baseline="fluxo atual",
        experiment="comparação pareada",
        result="resultado validado",
        regression_status="PASS",
        generalization_status="CONFIRMED",
        risk="LOW",
        existing_owner=None,
        scope="tenant-a",
        tenant_scope="tenant-a",
        source_kind="pr",
    )
    values.update(overrides)
    return SymbiontLabObservation(**values)


def test_lab_evaluation_keeps_learning_candidate_non_canonical():
    memory = MemoryStub()
    result = SymbiontLabAdapter(GovernedLearningService(memory)).evaluate(
        make_observation(), principal_id="principal-1", dataset_version="ds-1"
    )

    assert result.state == "LAB_ONLY"
    assert result.candidate is not None
    assert result.candidate.state == "CANDIDATE"
    assert result.evolution_classification == "COMPATIBLE"
    assert result.disposition == "CANDIDATE_FOR_GOVERNED_LEARNING"
    assert len(memory.calls) == 1


def test_promotion_package_requires_gate_decision_and_never_grants_mutation_authority():
    gate = EvolutionGate()
    result = gate.evaluate(
        __import__("elo.core.evolution_gate", fromlist=["EvolutionProposal"]).EvolutionProposal(
            proposal_id="lab-adjust-001",
            tenant_id="tenant-a",
            source_id="pr:lab-adjustments",
            summary="ajuste governado melhora resultado",
            purpose_alignment=True,
            identity_compatible=True,
            architecture_compatible=True,
            governance_compatible=True,
            evidence_ids=("e-1", "e-2"),
            maturity_score=0.9,
            provenance={"source": "lab"},
        )
    )

    package = GovernedLearningService.prepare_knowledge_promotion(
        learning_id="learning-1",
        knowledge_key="ELO.LAB.AJUSTE.001",
        title="Ajuste laboratorial validado",
        concept="Ajuste controlado com evidência",
        provenance={"source_ref": "pr:lab-adjustments", "source_commit": "HEAD"},
        scope="tenant-a",
        evidence_refs=("e-1", "e-2"),
        confidence=0.9,
        evolution_decision=result,
    )

    assert isinstance(package, PromotionPackage)
    assert package.status == "PROMOTABLE_KNOWLEDGE"
    assert package.payload["promotion"] == "VALIDATED_LEARNING_TO_REUSABLE_KNOWLEDGE"
    assert result.canonical_mutation_allowed is False


def test_promotion_package_fails_closed_without_evidence_or_gate():
    missing_evidence = GovernedLearningService.prepare_knowledge_promotion(
        learning_id="learning-1",
        knowledge_key="ELO.LAB.AJUSTE.002",
        title="Sem evidência",
        concept="Não deve promover",
        provenance={"source": "lab"},
        scope="tenant-a",
        evidence_refs=(),
        confidence=0.9,
    )
    assert missing_evidence.status == "PROMOTION_BLOCKED"
    assert missing_evidence.reason == "evidence_missing"

    missing_gate = GovernedLearningService.prepare_knowledge_promotion(
        learning_id="learning-1",
        knowledge_key="ELO.LAB.AJUSTE.003",
        title="Sem gate",
        concept="Não deve promover",
        provenance={"source": "lab"},
        scope="tenant-a",
        evidence_refs=("e-1",),
        confidence=0.9,
    )
    assert missing_gate.status == "PROMOTION_BLOCKED"
    assert missing_gate.reason == "evolution_gate_decision_missing"
