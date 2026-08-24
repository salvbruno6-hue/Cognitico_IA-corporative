---
id: ELO-012
name: Modular Flow Ingestion Protocol
type: normative
layer: process
owner: ELO knowledge engineering / Multiteiner process context
status: normative
authority: baseline
version: 0.2
related:
  - ELO-PROC-MULTITEINER-001
  - MULTITEINER_ORGANIZATIONAL_CONTEXT
  - ELO_CONTEXT_RESOLUTION
  - ELO_TRIGGER_REGISTRY
depends_on: []
---

# ELO-012 — Modular Flow Ingestion Protocol

## Objective

Use the Multiteiner process-flow material as an operational knowledge source while preserving source authority, provenance and epistemic boundaries.

The detailed process sequence is maintained in the canonical process-library artifact:

`03-process-library/MULTITEINER_END_TO_END_PROCESS_FLOW.md`

That artifact is the primary retrieval target when the ELO needs to reconstruct the Multiteiner flow in detail.

## 1. Extraction model

```text
Source document
  → process
  → stage
  → activity
  → input
  → decision/gate
  → resource
  → person/role
  → equipment
  → material
  → dependency
  → constraint
  → output
  → exception
  → return path
  → risk
  → evidence reference
```

The ELO should preserve the hierarchy. A process must not be flattened into an undifferentiated text block when the sequence is required for reasoning or retrieval.

## 2. Canonical process retrieval

For questions about the Multiteiner flow, retrieve in this order:

1. `ELO-PROC-MULTITEINER-001` for detailed process sequence;
2. `MULTITEINER_ORGANIZATIONAL_CONTEXT.md` for organizational context and sector relationships;
3. specialized Multiteiner documents for budgeting, KPIs, validation, simulation or other domain-specific questions;
4. current operational data for the present state;
5. experience/knowledge records for historical comparison.

The ELO should not answer a request for the complete flow from a KPI document alone.

## 3. Detail preservation

The detailed process must preserve, at minimum:

- macro flow;
- subprocess;
- stage;
- activity;
- gate/decision;
- input;
- output;
- responsible sector/role when known;
- material/resource dependency;
- exception;
- rework/return path;
- relationship with other sectors;
- data generated;
- validation state.

When the user requests "minuciosamente", the ELO should expand from macro flow to subprocesses and activities rather than returning only the top-level chain.

## 4. Interpretation rules

- The source is authoritative only for what it explicitly establishes.
- Inferences must be marked as inference.
- Missing process steps remain unknown.
- Conflicting sources create a contradiction state.
- Current observed behavior may differ from documented design and must be represented as a process deviation, not silently overwrite the documented process.
- A process description does not constitute current operational telemetry.
- A current KPI does not redefine the process sequence.

## 5. Process-versus-state distinction

The ELO must distinguish:

```text
PROCESS KNOWLEDGE
= how the process is represented/documented

CURRENT STATE
= what the operation is actually doing now

DEVIATION
= difference between documented/expected flow and observed flow
```

This distinction is required for reliable planning and diagnosis.

## 6. Cross-sector links

The extracted flow can be linked to:

- purchasing lead time;
- stock availability;
- production orders;
- maintenance events;
- quality records;
- logistics movements;
- financial costs;
- commercial deadlines;
- workforce capability and allocation;
- budget/customization history;
- return and repair records;
- inventory/stock-security state.

These links create hypotheses for investigation. They do not establish causality without evidence.

## 7. Multiteiner flow retrieval examples

### Question: "Qual é o fluxo da Multiteiner?"

Retrieve `ELO-PROC-MULTITEINER-001` and return the macro sequence first, followed by the relevant subprocesses.

### Question: "Qual é o fluxo do PCP?"

Retrieve the PCP section and its interfaces with Commercial/Locação, Orçamento/Customização, Almoxarifado, Compras, Produção, Qualidade, Expedição and Reparos.

### Question: "Qual é o fluxo de reparos?"

Retrieve the repair subprocess:

```text
Retorno
→ Recebimento
→ Quarentena
→ Limpeza
→ Identificação / Checklist de Avarias
→ Diagnóstico
→ Definição de Intervenção
→ Verificação de Material
→ Oficinas
→ Reparo
→ Testes
→ Qualidade
→ Estoque de Segurança
```

If quality fails, retrieve the return path:

```text
Qualidade
→ Retrabalho
→ Nova inspeção
→ Aprovação
→ Estoque de Segurança
```

### Question: "Como reparo conversa com Almoxarifado?"

Retrieve the relationship:

```text
Avaria
→ Diagnóstico
→ Material necessário
→ Disponibilidade
→ Requisição/Compra
→ Consumo
→ Custo
→ Resultado do reparo
```

### Question: "Como orçamento conversa com PCP?"

Retrieve:

```text
Demanda/customização
→ Modelo/configuração
→ Excedentes/variações
→ Materiais/serviços
→ Carga potencial
→ Planejamento
```

## 8. Search aliases

Index and resolve the following aliases:

- fluxo Multiteiner;
- fluxo completo;
- fluxo end-to-end;
- processo Multiteiner;
- fluxo modular;
- produção modular;
- linha modular;
- fluxo puxado modular;
- fluxo customizado;
- módulo personalizado;
- retorno de módulo;
- pós-locação;
- quarentena;
- avaria;
- reparo;
- recuperação;
- oficina;
- estoque de segurança;
- PCP;
- planejamento;
- AF;
- orçamento;
- customização;
- almoxarifado;
- expedição.

## 9. Provenance and contradictions

When process information is returned, preserve:

- artifact ID;
- source path;
- status;
- authority;
- validation state;
- relevant section/stage.

If another source presents a different sequence:

```text
Detect contradiction
→ identify sources
→ compare authority
→ compare version/date when available
→ preserve evidence
→ request validation when necessary
```

Do not silently overwrite the canonical process.

## 10. Example investigation

```text
Observation: high equipment maintenance cost
        ↓
Potential relations:
  route / floor condition / usage / maintenance practice / equipment condition
        ↓
Evidence search:
  maintenance history + movement events + operational context
        ↓
Information gaps
        ↓
Specialist questions
        ↓
Scenario comparison
        ↓
Recommendation
```

The ELO must not declare a person, sector or supplier responsible solely from correlation.

## 11. ELO cognitive use

The process document is knowledge. The ELO cognitive layer uses it as context for:

```text
QUESTION
→ CONTEXT RESOLUTION
→ PROCESS RETRIEVAL
→ RELEVANT STAGE(S)
→ CURRENT DATA
→ EVIDENCE
→ REASONING
→ RESPONSE / ORIENTATION
```

The ELO must keep separate:

- documented process;
- current operational state;
- evidence;
- hypothesis;
- recommendation;
- human decision.

## 12. Completion rule

The purpose of this protocol is not to create a parallel process architecture. It establishes how the existing Multiteiner process knowledge is extracted, indexed and retrieved by the ELO.

The detailed process itself belongs to the process library. This protocol governs its ingestion and use.
