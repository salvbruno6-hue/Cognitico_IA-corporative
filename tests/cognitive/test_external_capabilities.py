from elo.cognitive.evaluation import Evaluator, exact_match
from elo.cognitive.memory import InMemoryMemoryStore, MemoryKind, MemoryRecord
from elo.cognitive.reasoning.search import BreadthDeliberativeSearch
from elo.cognitive.routing import CognitiveRouter, RoutingRequest


def test_router_escalates_high_risk_to_deliberation() -> None:
    route = CognitiveRouter().route(
        RoutingRequest(task="complex decision", complexity=0.9, risk=0.9)
    )
    assert route.capability == "deliberative_search"
    assert route.reasoning_depth == 3
    assert route.verification_required is True


def test_router_uses_deterministic_path() -> None:
    route = CognitiveRouter().route(
        RoutingRequest(task="calculate", deterministic=True)
    )
    assert route.capability == "deterministic"


def test_memory_keeps_tenant_and_canonical_scopes_distinct() -> None:
    store = InMemoryMemoryStore()
    store.put(
        MemoryRecord(
            id="tenant-a-1",
            kind=MemoryKind.TENANT,
            content="tenant-specific rule",
            tenant_id="tenant-a",
            source="tenant",
            confidence=0.9,
        )
    )
    store.put(
        MemoryRecord(
            id="canon-1",
            kind=MemoryKind.CANONICAL,
            content="canonical principle",
            tenant_id=None,
            source="canon",
            confidence=1.0,
        )
    )
    assert [r.id for r in store.query(tenant_id="tenant-a")] == ["tenant-a-1"]
    assert [r.id for r in store.query(kind=MemoryKind.CANONICAL)] == ["canon-1"]


def test_deliberative_search_prunes_to_best_width() -> None:
    search = BreadthDeliberativeSearch[int](width=2, depth=2)
    result = search.solve(
        initial=0,
        expand=lambda value: (value + 1, value + 2),
        evaluate=lambda value: float(value),
    )
    assert result.state == 4
    assert result.path == (0, 2, 4)


def test_metric_evaluation_produces_comparable_score() -> None:
    result = Evaluator().evaluate(
        ["a", "b"],
        predict=lambda value: value,
        metric=lambda expected, predicted: exact_match(expected, predicted),
    )
    assert result.score == 1.0
    assert result.failures == 0
