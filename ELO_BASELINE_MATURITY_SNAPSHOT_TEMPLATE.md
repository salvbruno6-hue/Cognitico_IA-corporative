# ELO — Baseline Maturity Snapshot

> **Tipo:** snapshot de auditoria
> **ID:** ELO-GOV-SNAPSHOT-001
> **Status:** template
> **Autoridade:** derived from ELO-GOV-MAT-001
> **Versão:** 0.1.0
> **Data da auditoria:** <YYYY-MM-DD>
> **Commit de referência:** <SHA>
> **Auditor/revisor:** <responsável>

## 1. Objetivo

Registrar uma fotografia factual do estado do ELO em um commit específico.

Este arquivo não deve ser usado para declarar capacidades sem evidência. Ele deve apontar para artefatos, commits, testes, workflows, ADRs ou outras evidências verificáveis.

## 2. Resumo executivo

| Indicador | Valor |
|---|---:|
| Capacidades inventariadas | <n> |
| Nível 0 | <n> |
| Nível 1 | <n> |
| Nível 2 | <n> |
| Nível 3 | <n> |
| Nível 4 | <n> |
| Nível 5 | <n> |
| Nível 6 | <n> |
| Nível 7 | <n> |
| Bloqueadores críticos | <n> |
| Gaps altos | <n> |
| Capacidades verificadas | <n> |

## 3. Matriz principal

| ID | Capacidade | Owner | Maturidade | Evidência principal | Gaps | Próxima ação |
|---|---|---|---:|---|---|---|
| ELO-CAP-XXX | <nome> | <owner> | 0 | <evidência> | <gap> | <ação> |

## 4. Rastreabilidade de requisitos

| Requirement | Capability | Contract | Implementation | Test | Evidence | Status |
|---|---|---|---|---|---|---|
| ELO-REQ-XXX | ELO-CAP-XXX | <path> | <path> | <path> | <ref> | <status> |

## 5. Rastreabilidade de contratos

| Contract | Owner | Consumers | Implementation | Tests | Evidence | Status |
|---|---|---|---|---|---|---|
| <contract> | <owner> | <consumers> | <path> | <tests> | <evidence> | <status> |

## 6. Rastreabilidade de ADRs

| ADR | Decisão | Capacidades afetadas | Implementação relacionada | Estado |
|---|---|---|---|---|
| ADR-XXX | <decisão> | <IDs> | <paths> | <status> |

## 7. Gaps

| Gap | Severidade | Capacidade | Impacto | Owner | Próxima ação | Estado |
|---|---|---|---|---|---|---|
| ELO-GAP-XXX | blocker | ELO-CAP-XXX | <impacto> | <owner> | <ação> | open |

## 8. Riscos arquiteturais

Registrar somente riscos sustentados por evidência ou claramente identificados como hipótese.

| Risco | Evidência | Probabilidade | Impacto | Mitigação | Estado |
|---|---|---|---|---|---|
| <risco> | <ref> | <low/medium/high> | <low/medium/high> | <ação> | <status> |

## 9. Duplicidades

| Conceito | Artefato A | Artefato B | Classificação | Decisão |
|---|---|---|---|---|
| <conceito> | <path> | <path> | DUPLICATE/CONFLICT | <ação> |

## 10. Testes

| Área | Testes encontrados | Última execução | Resultado | Limitação |
|---|---:|---|---|---|
| Cognitive Interface | <n> | <timestamp> | pass/partial/fail | <limitação> |

## 11. Segurança e governança

Verificar quando aplicável:

- tenant isolation;
- authorization;
- provenance;
- auditability;
- sensitive data handling;
- human decision boundaries;
- autonomous action controls.

| Controle | Evidência | Resultado | Gap |
|---|---|---|---|
| <controle> | <ref> | pass/partial/fail | <gap> |

## 12. Production readiness

| Controle | Evidência | Resultado |
|---|---|---|
| Reproducible execution | <ref> | <status> |
| Test suite | <ref> | <status> |
| Error handling | <ref> | <status> |
| Observability | <ref> | <status> |
| Security | <ref> | <status> |
| Provenance | <ref> | <status> |
| Documentation | <ref> | <status> |

## 13. Declarações de fato

Registrar somente afirmações sustentadas por evidência.

- FACT: <afirmação> — Evidence: <ref>

## 14. Hipóteses

- HYPOTHESIS: <hipótese> — Evidence/Context: <ref>

## 15. Próximas fases

| Prioridade | Ação | Capacidade | Dependência | Risco | Critério de conclusão |
|---|---|---|---|---|---|
| 1 | <ação> | <capability> | <dependency> | <risk> | <DoD> |

## 16. Declaração de baseline

> Este snapshot representa o estado observado no commit `<SHA>` em `<data>`. Não deve ser interpretado como garantia de funcionamento além das evidências registradas.

## 17. Aprovação

- Arquitetura: <pending/approved>
- Governança: <pending/approved>
- Segurança: <pending/approved/not applicable>
- Qualidade: <pending/approved>
- Baseline: <pending/frozen>
