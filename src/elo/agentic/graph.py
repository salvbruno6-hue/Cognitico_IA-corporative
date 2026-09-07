"""Optional LangGraph runtime for the ELO agentic knowledge boundary.

The canonical ELO contracts remain framework-neutral. LangGraph is an optional
execution layer and must not own identity, governance, persistence, promotion,
or canonical knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .contracts import IntentSpec, KnowledgeContext
from .orchestrator import KnowledgeOrchestrator


@dataclass
class AgenticState:
    """Serializable state carried between orchestration stages."""

    intent: IntentSpec
    context: KnowledgeContext | None = None
    trace: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class GraphRuntimePolicy:
    """Safety limits for the optional graph runtime."""

    max_steps: int = 12
    allow_writes: bool = False
    allow_canonical_mutation: bool = False


def build_agentic_graph(
    orchestrator: KnowledgeOrchestrator,
    *,
    policy: GraphRuntimePolicy | None = None,
    intent_interpreter: Callable[[str], IntentSpec] | None = None,
) -> Any:
    """Build the LangGraph pipeline when LangGraph is installed.

    Import is intentionally local so the canonical ELO package does not acquire
    a hard dependency on LangGraph. The graph only calls the read-oriented
    orchestrator and returns a KnowledgeContext.
    """
    policy = policy or GraphRuntimePolicy()
    if policy.allow_writes or policy.allow_canonical_mutation:
        raise ValueError("agentic graph is read-only and cannot enable canonical mutation")

    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:  # pragma: no cover - exercised only without optional dependency
        raise RuntimeError("LangGraph is not installed; use the framework-neutral orchestrator") from exc

    class GraphState(dict):
        pass

    graph = StateGraph(GraphState)

    def interpret(state: GraphState) -> GraphState:
        state["trace"] = list(state.get("trace", [])) + ["interpret"]
        if "intent" not in state:
            question = state.get("question", "")
            if intent_interpreter is None:
                raise ValueError("intent or intent_interpreter is required")
            state["intent"] = intent_interpreter(question)
        return state

    def retrieve(state: GraphState) -> GraphState:
        state["trace"] = list(state.get("trace", [])) + ["retrieve"]
        state["context"] = orchestrator.run(state["intent"])
        return state

    def ground(state: GraphState) -> GraphState:
        state["trace"] = list(state.get("trace", [])) + ["ground"]
        context = state["context"]
        if context is None:
            raise ValueError("grounding requires KnowledgeContext")
        state["grounded"] = not any(g.blocks_decision for g in context.gaps)
        return state

    graph.add_node("interpret", interpret)
    graph.add_node("retrieve", retrieve)
    graph.add_node("ground", ground)
    graph.add_edge(START, "interpret")
    graph.add_edge("interpret", "retrieve")
    graph.add_edge("retrieve", "ground")
    graph.add_edge("ground", END)

    compiled = graph.compile()
    return compiled
