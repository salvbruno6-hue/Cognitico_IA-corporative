# ELO — External Cognitive Research Admission

**Status:** FORGE / RESEARCH BASELINE
**Branch:** forge/cognitive-capability-evolution-2026-08
**Purpose:** transformar conhecimento útil encontrado em projetos externos em capacidades nativas do ELO, sem copiar autoridade arquitetural, sem contaminar Soul/Core e sem promover código sem evidência.

## 1. Regra de incorporação

O ELO não incorpora repositórios externos como autoridade. Ele extrai:

- conceitos;
- padrões arquiteturais;
- algoritmos;
- contratos;
- métricas;
- mecanismos de avaliação;
- técnicas de otimização;
- estratégias de memória;
- estratégias de raciocínio;
- estratégias de roteamento;
- técnicas de inferência;
- evidências experimentais.

Fluxo obrigatório:

`SOURCE → ANALYSIS → ADAPTATION → EXPERIMENT → BENCHMARK → GOVERNANCE → CANONICAL CAPABILITY`

## 2. Fontes prioritárias auditadas

### 2.1 Stanford DSPy

Repository: `stanfordnlp/dspy`

Valor para ELO: muito alto.

Capacidades relevantes:
- módulos cognitivos composicionais;
- assinaturas de entrada/saída;
- otimização por métricas;
- few-shot automático;
- otimização de instruções;
- otimização de programas compostos;
- rastreamento/histórico de execução;
- avaliação paralela;
- otimização orientada por dados.

Decisão ELO: ADOPT-CONCEPT.

Adaptação nativa:
- `cognitive/modules`;
- `cognitive/optimization`;
- `cognitive/evaluation`;
- `cognitive/tracing`;
- `forge/experiments`.

Não incorporar como dependência obrigatória do Core.

### 2.2 Nir Diamant — Agent Memory Techniques

Repository: `NirDiamant/Agent_Memory_Techniques`

Valor para ELO: muito alto.

Capacidades relevantes:
- memória de curto prazo;
- memória persistente;
- memória episódica;
- memória semântica;
- working memory;
- memória hierárquica;
- reflexão;
- roteamento de memória;
- recuperação híbrida;
- grafos de conhecimento;
- memória entre sessões;
- avaliação de memória;
- consolidação e padrões de produção.

Decisão ELO: ADOPT-CONCEPT + EXPERIMENT.

Adaptação nativa:
- `cognitive/memory`;
- `cognitive/retrieval`;
- `cognitive/consolidation`;
- `cognitive/provenance`.

Regra adicional: memória Canonical, Tenant, Experience, Session e Working devem ser tipos distintos, com políticas de acesso e promoção próprias.

### 2.3 Princeton Tree of Thoughts

Repository: `princeton-nlp/tree-of-thought-llm`

Valor para ELO: alto para problemas que exigem busca deliberativa.

Capacidades relevantes:
- geração de pensamentos candidatos;
- avaliação de candidatos;
- busca em árvore;
- BFS;
- seleção/pruning;
- estratégias configuráveis de geração, avaliação e seleção.

Decisão ELO: ADOPT-PATTERN.

Adaptação nativa:
- `cognitive/reasoning/search`;
- `cognitive/reasoning/hypothesis`;
- `cognitive/verification`.

Regra: ToT não deve ser usado indiscriminadamente. O Cognitive Routing deve decidir quando a complexidade justifica busca deliberativa.

### 2.4 vLLM Semantic Router

Repository: `vllm-project/semantic-router`

Valor para ELO: muito alto.

Capacidades relevantes:
- classificação por múltiplos sinais;
- roteamento por intenção;
- seleção de modelo;
- seleção de caminho de execução;
- políticas de custo, qualidade, segurança e latência;
- composição/dispatch de modelos.

Decisão ELO: ADOPT-CONCEPT + ARCHITECTURAL REFERENCE.

Adaptação nativa:
- `cognitive/routing`;
- `runtime/model_selection`;
- `runtime/policy`.

Extensão ELO: o roteador não deve escolher apenas modelo. Deve escolher capacidade, ferramenta, profundidade de raciocínio, necessidade de verificação e nível de memória.

### 2.5 vLLM

Repository: `vllm-project/vllm`

Valor para ELO: alto para execução.

Capacidades relevantes:
- engine de inferência;
- batching/execução eficiente;
- interface Python;
- abstração entre aplicação e motor de inferência;
- execução de modelos em servidor.

Decisão ELO: ADOPT-AS-INFRASTRUCTURE.

Local: `runtime/inference`.

Regra: vLLM não define raciocínio, Soul, Canon ou Governance.

### 2.6 llama.cpp

Repository: `ggml-org/llama.cpp`

Valor para ELO: alto para soberania de execução local.

Capacidades relevantes:
- inferência local;
- quantização;
- CPU/GPU híbrido;
- múltiplos backends;
- servidor compatível com API OpenAI;
- grammar-constrained output;
- speculative decoding;
- embeddings e reranking.

Decisão ELO: ADOPT-AS-INFRASTRUCTURE.

Local: `runtime/inference/local`.

Regra: modelo local é mecanismo de execução, não autoridade cognitiva.

## 3. Matriz de capacidade ELO

| Capacidade | Fonte principal | Destino | Promoção inicial |
|---|---|---|---|
| Cognitive Modules | DSPy | Cognitive | Canon candidate |
| Metric-driven Optimization | DSPy | Cognitive/Forge | Canon candidate |
| Evaluation Harness | DSPy | Cognitive/Forge | Canon candidate |
| Trace-based Improvement | DSPy | Forge | Canon candidate |
| Working Memory | Memory Techniques | Cognitive | Canon candidate |
| Episodic Memory | Memory Techniques | Cognitive | Canon candidate |
| Semantic Memory | Memory Techniques | Cognitive | Canon candidate |
| Procedural Memory | Memory Techniques | Cognitive | Canon candidate |
| Memory Routing | Memory Techniques | Cognitive | Canon candidate |
| Memory Consolidation | Memory Techniques | Cognitive | Experimental |
| Reasoning Search | Tree of Thoughts | Cognitive | Canon candidate |
| Hypothesis Branching | Tree of Thoughts | Cognitive | Canon candidate |
| Pruning | Tree of Thoughts | Cognitive | Canon candidate |
| Verification | ToT + ELO governance | Cognitive | Canon candidate |
| Cognitive Routing | Semantic Router | Cognitive | Canon candidate |
| Model Routing | Semantic Router | Runtime | Canon candidate |
| Complexity Routing | ELO-native | Cognitive | New capability |
| Cost/Latency Routing | Semantic Router | Runtime | Canon candidate |
| High-throughput inference | vLLM | Runtime | Infrastructure |
| Local inference | llama.cpp | Runtime | Infrastructure |
| Quantized inference | llama.cpp | Runtime | Infrastructure |
| Self-improvement loop | DSPy + Forge | Forge | Experimental |
| Autonomous self-modification | External research | Forge | Rejected from Core |

## 4. Canonical cognitive principles derived

### ELO-COG-PRINCIPLE-001 — Metric-Driven Improvement

Uma capacidade cognitiva só é considerada melhor quando uma métrica previamente definida demonstra melhoria sem regressão relevante.

### ELO-COG-PRINCIPLE-002 — Capability Routing

O ELO deve selecionar dinamicamente a capacidade cognitiva adequada ao problema, em vez de aplicar sempre o mesmo caminho.

### ELO-COG-PRINCIPLE-003 — Adaptive Reasoning Depth

A profundidade do raciocínio deve ser proporcional à complexidade, risco, incerteza e valor da decisão.

### ELO-COG-PRINCIPLE-004 — Typed Memory

Memória deve possuir tipo, origem, escopo, validade, confiança, proveniência e política de promoção.

### ELO-COG-PRINCIPLE-005 — Deliberative Search on Demand

Busca por múltiplas hipóteses deve ser acionada quando a complexidade ou incerteza justificar seu custo.

### ELO-COG-PRINCIPLE-006 — Verification Before High-impact Decision

Decisões de maior impacto devem possuir verificação proporcional ao risco antes da recomendação.

### ELO-COG-PRINCIPLE-007 — Inference Independence

A cognição do ELO não pode depender de um único provedor ou engine de inferência.

### ELO-COG-PRINCIPLE-008 — Evidence-Based Evolution

Experiência, benchmark e regressão são requisitos para promover melhoria cognitiva ao Canon.

## 5. Arquitetura cognitiva alvo

```text
INPUT
  ↓
PERCEPTION
  ↓
CONTEXT RESOLUTION
  ↓
MEMORY RETRIEVAL
  ↓
COMPLEXITY / RISK / UNCERTAINTY ESTIMATION
  ↓
COGNITIVE ROUTER
  ├── Direct Reasoning
  ├── Tool Reasoning
  ├── Retrieval Reasoning
  ├── Tree Search
  ├── Graph Search
  ├── Numerical/Deterministic Engine
  └── Multi-step Deliberation
  ↓
VERIFICATION
  ↓
DECISION / RECOMMENDATION
  ↓
EXPERIENCE CAPTURE
  ↓
EVALUATION
  ↓
MEMORY CONSOLIDATION
  ↓
FORGE LEARNING CANDIDATE
  ↓
GOVERNANCE
  ↓
CANON / TENANT / EXPERIENCE MEMORY
```

## 6. Adaptação para execução

A implementação deve permanecer provider-agnostic:

```text
ELO Cognitive
  ↓
Model/Inference Port
  ├── OpenAI-compatible API
  ├── vLLM
  ├── llama.cpp
  └── future providers
```

O Cognitive Router seleciona a porta; a porta seleciona o mecanismo; o mecanismo não altera o contrato cognitivo.

## 7. Métricas mínimas

Cada capacidade nova deve registrar, quando aplicável:

- accuracy/correctness;
- groundedness;
- completeness;
- contradiction rate;
- unsupported-claim rate;
- calibration/confidence;
- latency p50/p95;
- token/input-output cost;
- tool success rate;
- retrieval precision/recall;
- memory usefulness;
- regression rate;
- human override rate;
- provenance completeness.

## 8. Critério de promoção

Nenhuma técnica externa entra diretamente no Canon.

Níveis:

`L0 absent → L1 conceptual → L2 documented → L3 contracted → L4 implemented → L5 tested → L6 verified → L7 operationally evidenced`

Promoção para Canon exige, no mínimo:

- contrato definido;
- implementação ELO-native ou dependência explicitamente justificada;
- testes executáveis;
- benchmark reproduzível;
- comparação com baseline;
- regressão verificada;
- segurança/tenant review quando aplicável;
- proveniência da origem;
- decisão de governança.

## 9. Não objetivos

Não fazer nesta fase:

- copiar repositórios inteiros para o Core;
- transformar fornecedor de modelo em autoridade;
- permitir autoalteração irrestrita do Core;
- promover conhecimento de Tenant para Canon automaticamente;
- substituir governança por score de benchmark;
- criar interface própria do ELO;
- acoplar ELO Cognitive a um único LLM.

## 10. Estado da pesquisa

Este documento é uma base de admissão do Forge. Ele não afirma que todas as capacidades estão implementadas. Implementação e maturidade devem ser demonstradas por código, testes e execução.
