---
artifact_id: ELO-COGNITIVE-HARNESS
title: Cognitive Harness
family: docs
layer: cognitive
type: contract
owner: cognitive-platform
authority: reference
status: defined
version: 0.1.0
related:
  - ADR-0014-cognitive-runtime-loop
  - ADR-0015-crl-learn-policy
  - ELO_HUMAN_RESPONSE_PROTOCOL
---

# Cognitive Harness

## 1. Propósito

Permitir rodar o CRL completo (10 estágios) em ambiente
isolado, com fixture controlada, para validar comportamento
integrado antes de mergear mudanças em produção.

O harness ORQUESTRA o CRL existente
(`src/elo/cognitive/runtime/crl.py`). Não cria novo CRL.

## 2. Não faz

- Não cria segundo CRL
- Não substitui harnesses existentes (hook, checkpoint, MCP)
- Não acessa Supabase
- Não acessa MCP
- Não acessa rede
- Não escreve em memória canônica
- Não promove aprendizado
- Não é autoridade de governança

Medições produzidas são evidência para Evolution Gate, não
decisão. Segue o mesmo princípio do
`SYMBIONT_MCP_TEST_HARNESS.md`:

> "Scores are measurements, not governance decisions."

## 3. Fluxo

```text
Controlled Fixture
      |
      v
CRLContext
      |
      v
CognitiveRuntimeLoop
      |
      +--> OBSERVE
      +--> CONTEXTUALIZE
      +--> ANALYZE
      +--> FORMULATE
      +--> DECIDE
      +--> EXECUTE
      +--> MONITOR
      +--> LEARN
      +--> FOLLOW_UP
      +--> REASSESS
      |
      v
Audit + Stage Results
      |
      +--> Delta
      +--> Directives
      +--> Human Response
      |
      v
Structured Cognitive Harness Report
```

O harness usa o `CognitiveRuntimeLoop` canônico para a
ordenação, auditoria e passagem de contexto. Os handlers usados
pela fixture são controlados e locais; eles não substituem os
handlers canônicos de produção.

## 4. Isolamento

A implementação do harness deve permanecer restrita a imports e
operações locais determinísticas.

Proibido:

- `supabase`
- MCP
- HTTP/HTTPS
- sockets
- transportes externos
- escrita em `memory/cognitive/`
- escrita em qualquer storage canônico

O ambiente de teste não deve depender de credenciais, variáveis
de rede ou serviços externos.

## 5. LEARN

O estágio LEARN é exercitado como estágio do CRL, mas o harness
não promove aprendizado.

O resultado laboratorial deve permanecer em estado
`candidate_only` / `promotion_not_attempted`.

Isso preserva ADR-0015: o harness mede o comportamento do ciclo;
não cria uma via alternativa de aprendizagem.

## 6. Report

O report estruturado deve conter, no mínimo:

- `request_id`
- ordem dos 10 estágios
- auditoria do CRL
- resultados dos estágios
- delta
- diretrizes
- `human_response`
- métricas de execução
- indicação explícita de isolamento
- indicação explícita de que nenhuma promoção foi tentada

## 7. Critérios de aceitação

Uma execução válida deve:

1. executar os 10 estágios;
2. registrar 10 entradas de auditoria;
3. não produzir estágio `skipped`;
4. não produzir erro;
5. produzir delta estruturado;
6. produzir diretrizes a partir do delta quando a fixture contiver
   lacunas;
7. produzir resposta humana;
8. registrar `network_access=false`,
   `supabase_access=false` e `mcp_access=false`;
9. registrar `promotion_attempted=false`;
10. permanecer determinística para a mesma fixture.

## 8. Fronteira de governança

O harness produz evidência laboratorial.

Ele não:

- aprova Evolution Gate;
- cria commit;
- faz merge;
- promove capacidade;
- altera Core;
- altera memória canônica.

A decisão de evolução permanece fora do harness.

## 9. Relação com os harnesses existentes

| Harness | Responsabilidade |
|---|---|
| Hook Loop Harness | Medição de guardrail |
| Checkpoint Loop Harness | Medição de replay guard |
| Symbiont MCP Test Harness | Benchmark de MCP autorizado |
| Cognitive Harness | Orquestração laboratorial do CRL de 10 estágios |

O Cognitive Harness não consolida nem substitui os três existentes.
