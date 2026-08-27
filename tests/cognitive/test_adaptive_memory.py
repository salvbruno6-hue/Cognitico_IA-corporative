from elo.cognitive.memory.store import CognitiveMemoryStore
from elo.cognitive.memory.types import MemoryItem, MemoryKind
from elo.cognitive.routing.learned import AdaptiveCognitiveRouter, RoutingExperience
from elo.cognitive.routing.router import RoutingRequest


def test_memory_search_respects_tenant_isolation() -> None:
    store = CognitiveMemoryStore()
    store.put(MemoryItem(id="canon", kind=MemoryKind.CANONICAL, content="safety policy", source="canon"))
    store.put(MemoryItem(id="a", kind=MemoryKind.TENANT, tenant_id="A", content="pricing policy", source="A"))
    store.put(MemoryItem(id="b", kind=MemoryKind.TENANT, tenant_id="B", content="pricing policy", source="B"))

    results = store.search("pricing", tenant_id="A")
    assert [match.item.id for match in results] == ["a"]


def test_adaptive_router_can_learn_a_better_path() -> None:
    router = AdaptiveCognitiveRouter()
    for _ in range(4):
        router.record(RoutingExperience("multi_step_reasoning", 0.95, 20, True))
    route = router.route(RoutingRequest(task="analysis", complexity=0.3, available_capabilities=frozenset({"direct_reasoning", "multi_step_reasoning"})))
    assert route.capability == "multi_step_reasoning"
    assert router.experience_count("multi_step_reasoning") == 4
