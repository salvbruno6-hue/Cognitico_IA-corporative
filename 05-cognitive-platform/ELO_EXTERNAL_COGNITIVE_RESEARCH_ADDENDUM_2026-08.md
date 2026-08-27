# ELO — External Cognitive Research Addendum

## Additional high-value references found during the first-pass audit

### Microsoft GraphRAG — `microsoft/graphrag`

GraphRAG is directly relevant to ELO knowledge/memory architecture because it builds structured representations from unstructured data: entities, relationships, claims, hierarchical communities and summaries, then uses those structures for retrieval and reasoning. Microsoft explicitly describes it as a research project and notes that the repository is largely in maintenance mode; therefore the ELO should absorb the methodology, not make the project a runtime dependency. citeturn1search0turn1search2turn1search3

**ELO decision:** ADOPT-CONCEPT / RESEARCH.

Potential native capabilities:
- entity/relationship/claim extraction;
- knowledge graph memory;
- hierarchical community structure;
- multi-level summaries;
- graph-aware retrieval;
- provenance from source text to graph fact;
- complex-question retrieval strategy.

**Canonical placement:** `cognitive/knowledge`, `cognitive/memory`, `cognitive/retrieval`.

**Important:** GraphRAG indexing can be expensive; ELO should route graph indexing only when the expected reasoning benefit justifies its cost. citeturn1search5

### NVIDIA NeMo Agent Toolkit — `NVIDIA/NeMo-Agent-Toolkit`

NeMo Agent Toolkit is valuable for the ELO's evaluation, observability, optimization and distributed execution ideas. Its current documentation describes offline workflow evaluation with accuracy, reliability and latency metrics, configurable evaluators, reproducible configuration artifacts, profiling and workflow outputs. citeturn1search1

Its broader architecture also includes evaluation, prompt/hyper-parameter optimization, agent performance primitives, parallel execution, speculative branching, node-level priority routing, MCP serving and A2A integration. citeturn1search7

**ELO decision:** ADOPT-CONCEPT / RESEARCH.

Potential native capabilities:
- evaluation harness;
- reproducible evaluation runs;
- trajectory capture;
- latency/performance profiling;
- parallel cognitive branches;
- speculative branches;
- priority routing;
- MCP exposure at Access Layer;
- workflow-level observability.

**Canonical placement:** `cognitive/evaluation`, `cognitive/tracing`, `runtime`, `access`.

### Combined conclusion

The first research wave should therefore not be limited to six projects. The ELO research matrix now contains three complementary planes:

```text
KNOWLEDGE / MEMORY
GraphRAG + Agent Memory Techniques

COGNITION / OPTIMIZATION
DSPy + Tree of Thoughts + Semantic Router

EXECUTION / EVALUATION
vLLM + llama.cpp + NeMo Agent Toolkit
```

This is a stronger basis for the ELO than selecting a single agent framework.

## Admission rule

No external repository becomes an ELO dependency merely because it is popular or technically impressive. Each technique must be converted into an ELO capability, benchmarked against a baseline, checked for regressions and security/tenant implications, and then promoted through the existing ELO governance maturity gates.
