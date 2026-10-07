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
- "ELO, confere essa análise da SO NNN.AA"
- "ELO, revisa isso da SO NNN.AA"
- "ELO, olha essa análise da SO NNN.AA"
- "ELO, valida a análise da SO NNN.AA"

**Payload gerado:**
{
  "intent": "confere_analise",
  "so_id": "SO NNN.AA",
  "chatgpt_analysis": "<texto seguinte ao comando>"
}

**O que o ELO faz:** roda o CRL completo, gera delta (aligned/improvements/corrections/conflicts), persiste e devolve.

### 2.2 o_que_sabe

**Nome canônico:** o_que_sabe
**Variações:**
- "ELO, o que você sabe sobre a SO NNN.AA"
- "ELO, me conta sobre a SO NNN.AA"
- "ELO, analisa a SO NNN.AA"

**Payload:**
{
  "intent": "o_que_sabe",
  "so_id": "SO NNN.AA"
}

**O que o ELO faz:** consulta SO resolver, retorna aprendizado + handbook + precedentes.

### 2.3 guarda_aprendizado

**Nome canônico:** guarda_aprendizado
**Variações:**
- "ELO, guarda isso da SO NNN.AA"
- "ELO, anota o aprendizado da SO NNN.AA"
- "ELO, registra isso"
- "ELO, aprende com a SO NNN.AA"

**Payload:**
{
  "intent": "guarda_aprendizado",
  "so_id": "SO NNN.AA",
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
- "ELO, já vimos algo parecido com a SO NNN.AA"
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

### 3.1 Autoridade da SO

A atribuição do número da SO é responsabilidade do **Analista de Orçamento**.

O ELO pode:
- receber a SO já atribuída;
- validar seu formato;
- normalizar sua representação textual;
- resolver referências pelo identificador;
- transportar e preservar a SO durante o ciclo de vida.

O ELO não pode:
- gerar uma SO;
- escolher uma SO;
- incrementar ou reservar a sequência;
- reiniciar a sequência anual;
- substituir uma SO recebida por outra;
- corrigir silenciosamente uma SO inválida para outra identidade.

A regra anual de NNN (001–999) e AA não cria responsabilidade de numeração para o ELO. O reinício da sequência é uma convenção da atribuição externa.

Se a SO estiver ausente, o ELO deve solicitar a SO atribuída. Se estiver inválida, deve bloquear a operação e solicitar correção da identidade original.

**Regra de identidade:** o ELO pode normalizar a representação de uma SO; não pode normalizar a identidade para outra SO.

## 4. Compatibilidade

O parser aceita também o payload JSON original (retrocompatível):

<!-- elo-request-payload
{"so_id": "...", "chatgpt_analysis": "..."}
-->

Se a issue tiver esse bloco, ele tem prioridade sobre a linguagem natural.

## 5. Vigência

Entra em vigor na aprovação da PR 10. Alterações exigem ADR.
