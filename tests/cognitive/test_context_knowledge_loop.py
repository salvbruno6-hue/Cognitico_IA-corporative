from elo.cognitive.context import ContextSignal, resolve_context
from elo.cognitive.knowledge.graph import CognitiveKnowledgeGraph, KnowledgeEdge, KnowledgeNode
from elo.cognitive.memory.store import CognitiveMemoryStore
from elo.cognitive.reasoning.search import BreadthDeliberativeSearch
from elo.cognitive.routing.router import CognitiveRouter, RoutingRequest
from elo.cognitive.verification import CognitiveVerifier
from elo.cognitive.evaluation import exact_match


def test_context_and_graph():
    context = resolve_context("analisar orçamento", tenant_id="empresa-a", signals=(ContextSignal("domain", "budget"),))
    assert context.tenant_id == "empresa-a"
    graph = CognitiveKnowledgeGraph()
    graph.add_node(KnowledgeNode("a", "orçamento", "tenant"))
    graph.add_node(KnowledgeNode("b", "material", "tenant"))
    graph.add_edge(KnowledgeEdge("a", "b", "contains"))
    assert graph.neighbors("a")[0].id == "b"


def test_memory_retrieval_and_verification():
    store = CognitiveMemoryStore()
    from elo.cognitive.memory.types import MemoryItem, MemoryKind
    store.put(MemoryItem(id="canon", kind=MemoryKind.CANONICAL, content="regra orçamento", source="canon", confidence=1.0))
    store.put(MemoryItem(id="tenant", kind=MemoryKind.TENANT, content="preço empresa", source="empresa", tenant_id="a", confidence=1.0))
    assert store.search("preço", tenant_id="b") == ()
    assert store.search("regra orçamento", tenant_id="b")
    result = CognitiveVerifier().verify(answer="ok", evidence=("source",))
    assert result.accepted
    assert exact_match("x", "x") == 1.0


def test_router_and_deliberation():
    route = CognitiveRouter().route(RoutingRequest(query="calcular", complexity=0.9, risk=0.8, uncertainty=0.7))
    assert route.verification_required
    search = BreadthDeliberativeSearch(expand=lambda x: (x + "a", x + "b"), evaluate=lambda x: 1.0 if x.endswith("b") else 0.5)
    assert search.run("root", depth=1) == "rootb"
