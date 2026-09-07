"""Optional LangGraph runtime for the ELO agentic knowledge boundary.

The canonical ELO contracts remain framework-neutral. LangGraph is an optional
execution layer and must not own identity, governance, persistence, promotion,
or canonical knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, TypedDict

from .contracts import IntentSpec, KnowledgeContext
from .orchestrator import KnowledgeOrchestrator


class GraphState(TypedDict, total=False):
    """Bounded state carried through the agentic graph."""

    question: str
    intent: IntentSpec
    context: KnowledgeContext
    grounded: bool
    trace: tuple[str, ...]


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

    The graph is intentionally a thin runtime adapter. Canonical ELO contracts,
    retrieval and governance remain framework-neutral and authoritative.
    """
    policy = policy or GraphRuntimePolicy()
    if policy.allow_writes or policy.allow_canonical_mutation:
        raise ValueError("agentic graph is read-only and cannot enable canonical mutation")
    if policy.max_steps < 1:
        raise ValueError("max_steps must be positive")

    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "LangGraph is not installed; use the framework-neutral orchestrator"
        ) from exc

    graph = StateGraph(GraphState)

    def append_trace(state: GraphState, stage: str) -> tuple[str, ...]:
        trace = tuple(state.get("trace", ())) + (stage,)
        if len(trace) > policy.max_steps:
            raise RuntimeError("agentic graph step limit exceeded")
        return trace

    def interpret(state: GraphState) -> GraphState:
        trace = append_trace(state, "interpret")
        if "intent" in state:
            return {"trace": trace}
        question = state.get("question", "").strip()
        if not question:
            raise ValueError("question or intent is required")
        if intent_interpreter is None:
            raise ValueError("intent_interpreter is required when intent is absent")
        return {"intent": intent_interpreter(question), "trace": trace}

    def retrieve(state: GraphState) -> GraphState:
        trace = append_trace(state, "retrieve")
        intent = state.get("intent")
        if intent is None:
            raise ValueError("retrieve requires intent")
        return {"context": orchestrator.run(intent), "trace": trace}

    def ground(state: GraphState) -> GraphState:
        trace = append_trace(state, "ground")
        context = state.get("context")
        if context is None:
            raise ValueError("grounding requires KnowledgeContext")
        grounded = context.grounded and not context.conflicts
        return {"grounded": grounded, "trace": trace}

    graph.add_node("interpret", interpret)
    graph.add_node("retrieve", retrieve)
    graph.add_node("ground", ground)
    graph.add_edge(START, "interpret")
    graph.add_edge("interpret", "retrieve")
    graph.add_edge("retrieve", "ground")
    graph.add_edge("ground", END)

    return graph.compile()
