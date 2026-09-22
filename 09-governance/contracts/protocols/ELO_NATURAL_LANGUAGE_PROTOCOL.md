---
artifact_id: ELO-NATURAL-LANGUAGE-PROTOCOL
title: ELO Natural Language Protocol
family: 09-governance
layer: governance
type: protocol
status: normative
owner: ELO Governance
version: 1.0.0
related:
  - ELO_EXTERNAL_AI_AUTHORITY_CONTRACT
  - ADR-0014-cognitive-runtime-loop
  - ADR-0015-crl-learn-policy
---

# ELO Natural Language Protocol

## 1. Propósito

Definir a linguagem natural oficial pela qual humanos podem acionar o ELO sem conhecer sintaxe técnica (JSON, issue, label).

O ELO aceita comandos em português natural. O parser (src/elo/cognitive/runtime/intake/natural_language.py) traduz a linguagem para um payload estruturado.

## 2. Comandos canônicos

### 2.1 confere_analise

**Nome canônico:** confere_analise
**Variações aceitas:**
- "ELO, confere essa análise da SO X"
- "ELO, revisa isso da SO X"
- "ELO, olha essa análise da SO X"
- "ELO, valida a análise da SO X"

**Payload gerado:**
{
  "intent": "confere_analise",
  "so_id": "SO-X",
  "chatgpt_analysis": "<texto seguinte ao comando>"
}

**O que o ELO faz:** roda o CRL completo, gera delta (aligned/improvements/corrections/conflicts), persiste e devolve.

### 2.2 o_que_sabe

**Nome canônico:** o_que_sabe
**Variações:**
- "ELO, o que você sabe sobre a SO X"
- "ELO, me conta sobre a SO X"
- "ELO, analisa a SO X"

**Payload:**
{
  "intent": "o_que_sabe",
  "so_id": "SO-X"
}

**O que o ELO faz:** consulta SO resolver, retorna aprendizado + handbook + precedentes.

### 2.3 guarda_aprendizado

**Nome canônico:** guarda_aprendizado
**Variações:**
- "ELO, guarda isso da SO X"
- "ELO, anota o aprendizado da SO X"
- "ELO, registra isso"
- "ELO, aprende com a SO X"

**Payload:**
{
  "intent": "guarda_aprendizado",
  "so_id": "SO-X",
  "learning": "<texto seguinte ao comando>"
}

**O que o ELO faz:** persiste aprendizado em memory/solicitations_learning/.

### 2.4 status_decisao

**Nome canônico:** status_decisao
**Variações:**
- "ELO, como está a decisão DEC-X"
- "ELO, status da decisão DEC-X"

**Payload:**
{
  "intent": "status_decisao",
  "decision_id": "DEC-X"
}

### 2.5 lista_abertas

**Nome canônico:** lista_abertas
**Variações:**
- "ELO, o que está aberto"
- "ELO, lista pendências"
- "ELO, quais decisões estão abertas"

**Payload:**
{
  "intent": "lista_abertas",
  "state_filter": ["proposed", "approved", "executed", "observing", "evaluated", "attributed"]
}

### 2.6 busca_precedente

**Nome canônico:** busca_precedente
**Variações:**
- "ELO, já vimos algo parecido com a SO X"
- "ELO, tem precedente para X"
- "ELO, compara com outras SOs"

**Payload:**
{
  "intent": "busca_precedente",
  "query": "<texto seguinte ao comando>"
}

## 3. Regras

1. O parser aceita variações coloquiais e formais.
2. Se o comando não for reconhecido, o parser tenta JSON.
3. Se ambos falharem, retorna erro estruturado com sugestões.
4. A linguagem canônica é registrada em auditoria (intent).
5. Novos comandos exigem ADR.

## 4. Compatibilidade

O parser aceita também o payload JSON original (retrocompatível):

<!-- elo-request-payload
{"so_id": "...", "chatgpt_analysis": "..."}
-->

Se a issue tiver esse bloco, ele tem prioridade sobre a linguagem natural.

## 5. Vigência

Entra em vigor na aprovação da PR 10. Alterações exigem ADR.
