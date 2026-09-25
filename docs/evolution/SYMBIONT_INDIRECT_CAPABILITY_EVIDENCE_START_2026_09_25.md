---
artifact_id: ELO-SYMBIONT-INDIRECT-CAPABILITY-EVIDENCE-START
owner: ELO Governance / Symbiont
version: 1.0.0
phase: START
canonical_mutation: false
---

# START — Evidência indireta de capacidade

## Objetivo

Permitir que EVOLUÇÃO_DE_CAPACIDADES reconheça evidência corroborada por uma capacidade downstream já validada, sem exigir que a capacidade avaliada seja a própria fonte de tráfego operacional.

## Reutilização canônica

- EVOLUÇÃO_DE_CAPACIDADES continua em `src/elo/cognitive/symbiont_capability_evolution.py`.
- PerformanceEvidence continua sendo a autoridade de evidência.
- SymbiontLabObservation / SymbiontLabAdapter continuam sendo o handoff laboratorial.
- EvolutionGate continua sendo a autoridade de evolução.
- Nenhum novo router, registry, memória, dashboard ou promotion gate é criado.

## Contrato de evidência

A origem indireta precisa declarar explicitamente:

1. capacidade avaliada;
2. baseline/current;
3. direção da métrica;
4. período;
5. referências de evidência;
6. capacidade observadora validada;
7. referência da experiência observadora.

Ausência de qualquer elemento obrigatório não é convertida em ganho, zero ou inferência.

## Exemplo arquitetural

Progressive Tool Schema Disclosure → ExecutionRouter / experiência validada → PerformanceEvidence → EVOLUÇÃO_DE_CAPACIDADES → diagnóstico/ação → fluxo laboratorial existente → Evolution Gate.

O vínculo é corroborativo; não constitui inferência causal automática.

## Limites

- read-only;
- canonical_mutation=false;
- sem promoção automática;
- sem execução de ferramenta;
- sem declaração de benefício de produção apenas pela existência da evidência indireta.
