---
artifact_id: ADR-0015-crl-learn-policy
title: Política B — Symbiont Lab obrigatório para LEARN no CRL
family: 10-adr
status: accepted
owner: ELO Architecture Board
deciders:
  - ELO Governance
  - ELO Cognitive Platform
date: 2026-09-21
supersedes: null
superseded_by: null
related:
  - ADR-0014-cognitive-runtime-loop
  - src/elo/core/decision_outcome_loop.py
  - src/elo/cognitive/symbionte_lab.py
  - src/elo/core/learning_governance.py
---

# ADR-0015 — Política B: Symbiont Lab obrigatório para LEARN

## Contexto

O Cognitive Runtime Loop (CRL) precisa de um único caminho governado para transformar resultados de decisões em aprendizagem. O Core já mantém o ciclo de decisão e o Symbiont Lab já fornece a fronteira laboratorial entre observação, experiência e candidato de aprendizagem.

Permitir caminhos alternativos de aprendizagem no handler do CRL criaria diferenças de qualidade e dificultaria a auditoria.

## Decisão

O estágio LEARN do CRL deve usar obrigatoriamente o SymbiontLabAdapter por meio de DecisionLifecycle.handoff_to_symbiont().

Sem adapter e/ou observação laboratorial, o ciclo não entra em LEARNED; ele transita para ESCALATED com a razão symbiont_required_for_learning.

O handler não cria candidato de aprendizagem diretamente e não duplica attach_learning().

A política exige a presença do contexto laboratorial completo definido por SymbiontLabObservation. A validação estrutural e de governança permanece de responsabilidade do Symbiont Lab existente.

## Consequências diretas

- Toda aprendizagem passa pelo mesmo crivo do Symbiont Lab.
- Sem adapter acoplado, nenhuma decisão chega a LEARNED.
- Decisões sem contexto laboratorial completo não são promovidas pelo CRL e devem escalar.
- Escalonamento é um resultado governado, não uma falha operacional.

## Justificativa

1. Consistência de aprendizado: todo conhecimento que entra em PrecedentIndex deve ter passado pelo mesmo gate.
2. Governança forte: o ELO aprende com validação Symbiont; sem validação, escala para avaliação humana.
3. Alinhamento com o Evolution Gate: o Evolution Gate já filtra evolução; o Symbiont Lab é a fronteira cognitiva equivalente para aprendizagem.
4. Simplicidade do handler: um único caminho canônico evita ramificações de aprendizagem.

## Alternativas consideradas

### A. Symbiont quando disponível, attach_learning() caso contrário

Rejeitada: permitiria que o ELO aprendesse por duas vias distintas, com propriedades de governança diferentes.

### C. Aprendizado diferenciado por complexidade

Rejeitada: exigiria uma definição adicional de complexidade sem evidência ou contrato existente.

## Consequências

### Positivas

- Consistência do aprendizado.
- Auditoria simplificada.
- Alinhamento com o Symbiont Lab existente.

### Negativas

- Sem Symbiont, o ciclo pode parar em ESCALATED.
- O runtime precisa receber GovernedLearningService + SymbiontLabAdapter para habilitar LEARNED.
- Decisões sem contexto laboratorial suficiente não são promovidas.

### Neutras

- O bootstrap registra os handlers canônicos; a disponibilidade do adapter é avaliada no estágio LEARN.
- Escalonamentos do LEARN são persistidos em memory/cognitive/.

## Conformidade

- Regra de duplicidade: NEW (política nova; não existia como contrato).
- Camada: Governança.
- Princípio fundador: preservado — o ELO aprende com validação; sem validação, escala para humano.

## Status

Aceito. Implementação no CRL runtime.
