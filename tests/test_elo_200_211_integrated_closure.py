from decimal import Decimal

from elo.core.budgeting import BudgetInputClass
from elo.core.budgeting_retrieval import retrieved_to_budget_input
from elo.core.capability_registry import CapabilityProbe, CapabilityRegistry, CapabilityStatus
from elo.core.consultative_orchestration import ConsultativeOrchestrator
from elo.core.context_resolution import ContextEvidence, ContextPack, ContextQuery, ContextSource, ContextResolutionEngine
from elo.core.evolution_gate import EvolutionClassification, EvolutionGate, EvolutionProposal
from elo.core.gpt_handoff import ConsultativeReturn
from elo.core.hybrid_bridge import HybridCapabilityBridge
from elo.core.local_capabilities import probe_local_tools
from elo.core.source_discovery import SourceDiscoveryEngine
from elo.core.source_resolver import RetrievedSource
from elo.core.specialist_feedback import SpecialistFeedback, SpecialistFeedbackRegistry
from elo.core.diagnostic_scenarios import DiagnosticLens, DiagnosticObservation, DiagnosticScenario, DiagnosticStatus
from elo.core.scenario_gates import MultiScenarioGate


def context():
    source = ContextSource(source_id="src-1", source_type="fixture", authority="test",
                           tenant_id="tenant-a", domain="BUDGET", principal_id="p-1", provenance={"fixture": "closure"})
    evidence = ContextEvidence(source_id="src-1", fact="evidence", confidence=0.95,
                               tenant_id="tenant-a", domain="BUDGET", provenance={"principal_id": "p-1"})
    query = ContextQuery(question="validate budget", tenant_id="tenant-a", domain="BUDGET",
                         principal_id="p-1", request_id="req-1", correlation_id="corr-1")
    resolved = ContextResolutionEngine().resolve(query)
    return ContextPack(query=resolved.query, discovery_plan=resolved.discovery_plan,
                       sources=(source,), evidence=(evidence,))


def test_200_semantic_discovery_emits_adapter_capability():
    plan = SourceDiscoveryEngine().plan("revisar arquitetura do projeto")
    github = next(item for item in plan.candidates if item.kind == "GITHUB")
    assert github.required_capability == "source.github.read"


def test_201_evolution_gate_never_mutates_canonical_state():
    proposal = EvolutionProposal("p-1", "tenant-a", "src-1", "compatible improvement",
                                  True, True, True, True, ("e-1",), 0.9, None, {"request_id": "r-1"})
    result = EvolutionGate().evaluate(proposal)
    assert result.classification == EvolutionClassification.COMPATIBLE
    assert result.canonical_mutation_allowed is False


def test_202_hybrid_bridge_selects_healthy_provider_and_degrades_without_one():
    registry = CapabilityRegistry((CapabilityProbe("REMOTE_AI", "remote", health_check=lambda: True),
                                   CapabilityProbe("LOCAL_AI", "ollama", health_check=lambda: False)))
    selection = HybridCapabilityBridge(registry).select(preferred_kinds=("LOCAL_AI", "REMOTE_AI"))
    assert selection.status == "AVAILABLE" and selection.capability_name == "remote"
    degraded = HybridCapabilityBridge(CapabilityRegistry((CapabilityProbe("LOCAL_AI", "ollama", health_check=lambda: False),))).select()
    assert degraded.status == "DEGRADED"


def test_205_consultative_orchestration_cannot_accept_canonical_authority():
    maturity = HybridCapabilityBridge.assess_maturity({})
    handoff = ConsultativeOrchestrator().prepare(context=context(), maturity=maturity, objective="review")
    returned = ConsultativeReturn(status="OK", classification="ADVISORY", confidence=.8,
                                  provenance={"canonical_authority": "false"})
    outcome = ConsultativeOrchestrator().consult(handoff, lambda _payload: returned)
    assert outcome.status == "RETURNED"
    assert outcome.handoff.tenant_id == "tenant-a"


def test_206_forge_skill_pack_uses_shared_faculty_without_parallel_core():
    text = open("forge/skill-packs/ELO_FORGE_HR_PCP_CALCULATION_v1.yaml", encoding="utf-8").read()
    assert "shared_faculty: Core" in text
    assert "direct_forge_to_core_promotion: false" in text


def test_207_specialist_feedback_is_append_only_and_scoped():
    registry = SpecialistFeedbackRegistry()
    feedback = SpecialistFeedback("f-1", "PCP-1", "tenant-a", "PCP", "mt-001", "capacity changed",
                                   ("e-1",), {"request_id": "r-1"})
    registry.ingest(feedback)
    assert registry.list(tenant_id="tenant-a", domain="PCP") == (feedback,)
    assert registry.list(tenant_id="tenant-b", domain="PCP") == ()
    try:
        registry.ingest(feedback)
    except ValueError:
        pass
    else:
        raise AssertionError("historical feedback must be immutable")
