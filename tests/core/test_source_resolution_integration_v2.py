from decimal import Decimal

from elo.adapters.source_adapters import GitHubSourceAdapter
from elo.core.budgeting import BudgetInput, BudgetInputClass, BudgetLine, BudgetLineType, BudgetRequest, GovernedBudgetingService
from elo.core.source_discovery import SourceDiscoveryEngine
from elo.core.source_resolver import RetrievedSource, SourceResolutionRequest, SourceResolver


def _request() -> SourceResolutionRequest:
    return SourceResolutionRequest(
        query="quantidade para orçamento",
        tenant_id="tenant-a",
        domain="budgeting",
        principal_id="principal-a",
        session_id="session-a",
        request_id="request-a",
        correlation_id="correlation-a",
        conversation_id="conversation-a",
        authorization_scope="source:github:read",
    )


def test_discovery_capability_matches_authorized_adapter_and_reaches_temporal_memory():
    plan = SourceDiscoveryEngine().plan("qual a arquitetura do projeto ELO?")
    candidate = next(item for item in plan.candidates if item.kind == "GITHUB")
    assert candidate.required_capability == "source.github.read"

    adapter = GitHubSourceAdapter(
        lambda candidate, request: (
            RetrievedSource("github-evidence-1", "GITHUB", "quantity=10", {"uri": "github://evidence-1"}),
        )
    )
    result = SourceResolver((adapter,)).resolve(candidate, _request())
    assert result.status == "RETRIEVED_TO_TEMPORAL"
    assert result.temporal_records[0].provenance["tenant_id"] == "tenant-a"
    assert result.temporal_records[0].provenance["adapter_kind"] == "GITHUB"


def test_retrieved_source_evidence_can_feed_canonical_budgeting():
    plan = SourceDiscoveryEngine().plan("qual a arquitetura do orçamento do projeto?")
    candidate = next(item for item in plan.candidates if item.kind == "GITHUB")
    adapter = GitHubSourceAdapter(
        lambda candidate, request: (
            RetrievedSource("e-q", "GITHUB", "10", {"uri": "github://q"}),
            RetrievedSource("e-c", "GITHUB", "25", {"uri": "github://c"}),
        )
    )
    result = SourceResolver((adapter,)).resolve(candidate, _request())
    assert result.status == "RETRIEVED_TO_TEMPORAL"

    request = BudgetRequest("budget-request", "tenant-a", "principal-a", "budgeting", "2026-08", "project budget", "project")
    inputs = (
        BudgetInput.create(tenant_id="tenant-a", domain="budgeting", name="quantity", classification=BudgetInputClass.FACT, value=10, unit="unit", source_id="e-q", provenance={"uri": "github://q"}),
        BudgetInput.create(tenant_id="tenant-a", domain="budgeting", name="unit_cost", classification=BudgetInputClass.FACT, value=25, unit="BRL", source_id="e-c", provenance={"uri": "github://c"}),
    )
    version = GovernedBudgetingService().calculate(
        request,
        inputs=inputs,
        lines=(BudgetLine("line-1", "project cost", BudgetLineType.COST, inputs[0].input_id, inputs[1].input_id),),
    )
    assert version.known_cost_subtotal == Decimal("250")
    assert version.evidence_ids == ("e-q", "e-c")
    assert version.is_reproducible


def test_unavailable_source_returns_explicit_gap_without_evidence():
    plan = SourceDiscoveryEngine().plan("qual a arquitetura do projeto?")
    candidate = next(item for item in plan.candidates if item.kind == "GITHUB")
    adapter = GitHubSourceAdapter(lambda candidate, request: (), available_state=False)
    result = SourceResolver((adapter,)).resolve(candidate, _request())
    assert result.status == "UNAVAILABLE"
    assert result.retrieved == ()
    assert result.temporal_records == ()
    assert result.gap
