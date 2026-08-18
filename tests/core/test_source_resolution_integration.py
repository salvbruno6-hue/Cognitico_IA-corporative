from decimal import Decimal

from elo.adapters.source_adapters import GitHubSourceAdapter
from elo.core.budgeting import BudgetInput, BudgetInputClass, BudgetLine, BudgetLineType, BudgetRequest, GovernedBudgetingService
from elo.core.source_discovery import SourceDiscoveryEngine
from elo.core.source_resolver import RetrievedSource, SourceResolutionRequest, SourceResolver


def _request(scope: str = "source.github.read") -> SourceResolutionRequest:
    return SourceResolutionRequest(
        query="quantidade de unidades para orçamento",
        tenant_id="tenant-a",
        domain="budgeting",
        principal_id="principal-a",
        session_id="session-a",
        request_id="request-a",
        correlation_id="correlation-a",
        conversation_id="conversation-a",
        authorization_scope=scope,
    )


def test_semantic_discovery_emits_adapter_capability_and_retrieval_reaches_temporal_memory():
    plan = SourceDiscoveryEngine().plan("qual a arquitetura do projeto ELO?")
    candidate = next(item for item in plan.candidates if item.kind == "GITHUB")
    assert candidate.required_capability == "source.github.read"

    adapter = GitHubSourceAdapter(
        lambda candidate, request: (
            RetrievedSource(
                source_id="github-evidence-1",
                source_type="GITHUB",
                content="quantity=10",
                provenance={"uri": "github://evidence-1"},
            ),
        )
    )
    result = SourceResolver((adapter,)).resolve(candidate, _request())
    assert result.status == "RETRIEVED_TO_TEMPORAL"
    assert result.temporal_records[0].provenance["tenant_id"] == "tenant-a"
    assert result.temporal_records[0].provenance["adapter_kind"] == "GITHUB"


def test_retrieved_evidence_can_feed_canonical_budgeting_without_bypassing_provenance():
    plan = SourceDiscoveryEngine().plan("qual a arquitetura do orçamento do projeto?")
    candidate = next(item for item in plan.candidates if item.kind == "GITHUB")
    evidence = {
        "quantity": RetrievedSource("e-q", "GITHUB", "10", {"uri": "github://q"}),
        "unit_cost": RetrievedSource("e-c", "GITHUB", "25", {"uri": "github://c"}),
    }
    adapter = GitHubSourceAdapter(lambda candidate, request: tuple(evidence.values()))
    result = SourceResolver((adapter,)).resolve(candidate, _request())
    assert result.status == "RETRIEVED_TO_TEMPORAL"

    request = BudgetRequest("budget-request", "tenant-a", "principal-a", "budgeting", "2026-08", "project budget", "project")
    inputs = (
        BudgetInput.create(tenant_id="tenant-a", domain="budgeting", name="quantity", classification=BudgetInputClass.FACT, value=10, unit="unit", source_id="e-q", provenance={"uri": "github://q"}),
        BudgetInput.create(tenant_id="tenant-a", domain="budgeting", name="unit_cost", classification=BudgetInputClass.FACT, value=25, unit="BRL", source_id="e-c", provenance={"uri": "github://c"}),
    )
    lines = (BudgetLine("line-1", "project cost", BudgetLineType.COST, inputs[0].input_id, inputs[1].input_id),)
    version = GovernedBudgetingService().calculate(request, inputs=inputs, lines=lines)
    assert version.known_cost_subtotal == Decimal("250")
    assert version.evidence_ids == ("e-q", "e-c")
    assert version.is_reproducible


def test_source_unavailability_is_explicit_and_does_not_fabricate_evidence():
    plan = SourceDiscoveryEngine().plan("qual a arquitetura do projeto?")
    candidate = next(item for item in plan.candidates if item.kind == "GITHUB")
    adapter = GitHubSourceAdapter(lambda candidate, request: (), available_state=False)
    result = SourceResolver((adapter,)).resolve(candidate, _request())
    assert result.status == "UNAVAILABLE"
    assert result.retrieved == ()
    assert result.temporal_records == ()
    assert result.gap
