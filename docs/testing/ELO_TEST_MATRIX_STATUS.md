# ELO — Matriz Executável de Cobertura de Testes

## Finalidade

Transformar a Cadeira de Testes em uma medição objetiva. Um caso somente conta como **PASS** quando existe execução automatizada e evidência do resultado. `DEFINED`, `UNKNOWN` e `BLOCKED` não contam como positivo.

## Estados

- `PASS`: executado e aprovado.
- `FAIL`: executado e reprovado.
- `UNKNOWN`: não há evidência suficiente de execução/resultado.
- `BLOCKED`: existe impedimento conhecido que invalida a execução.
- `DEFINED`: caso especificado, ainda não executado.

## Fórmulas

- **Positivos executados** = `PASS / (PASS + FAIL)`.
- **Cobertura executada** = `(PASS + FAIL) / casos totais`.
- `UNKNOWN`, `BLOCKED` e `DEFINED` ficam fora do denominador de positivos, mas permanecem no denominador de cobertura total.

## Matriz inicial

| ID | Área | Cenário | Estado | Evidência |
|---|---|---|---|---|
| CTX-001 | Context | consulta identifica entidade | PASS | PR #70 / behavioral validation |
| CTX-002 | Context | consulta preserva tenant | PASS | PR #70 / behavioral validation |
| CTX-003 | Context | consulta preserva unidade | PASS | PR #70 / behavioral validation |
| CTX-004 | Context | escopo incompatível bloqueia especialista | PASS | PR #70 / behavioral validation |
| CTX-005 | Context | metadado confiável completa escopo ausente | DEFINED | — |
| CTX-006 | Context | conflito entre contexto explícito e fonte bloqueia | DEFINED | — |
| SRC-001 | Discovery | fonte é descoberta sem caminho manual | PASS | PR #70 / behavioral validation |
| SRC-002 | Discovery | precedência determinística | DEFINED | — |
| SRC-003 | Discovery | intenção específica vence termo genérico | DEFINED | — |
| SRC-004 | Discovery | fonte indisponível é reportada | DEFINED | — |
| GPT-001 | Handoff | especialista exige contexto válido | PASS | PR #70 / behavioral validation |
| GPT-002 | Handoff | especialista exige evidência suficiente | PASS | PR #70 / behavioral validation |
| GPT-003 | Handoff | provider não autorizado é bloqueado | DEFINED | — |
| GPT-004 | Handoff | provider indisponível não vira invenção | DEFINED | — |
| DIAG-001 | Diagnostic | baseline é analisável | PASS | PR #70 / behavioral validation |
| DIAG-002 | Diagnostic | stress é analisável | PASS | PR #70 / behavioral validation |
| DIAG-003 | Diagnostic | failure é analisável | PASS | PR #70 / behavioral validation |
| DIAG-004 | Diagnostic | counterfactual preserva estado canônico | DEFINED | — |
| DIAG-005 | Diagnostic | sensitivity registra dependências | DEFINED | — |
| DIAG-006 | Diagnostic | conflito bloqueia consolidação | DEFINED | — |
| DIAG-007 | Diagnostic | baixa confiança permanece explícita | DEFINED | — |
| PROD-001 | Production | ciclo mínimo completo | DEFINED | — |
| PROD-002 | Production | desvio é identificado | DEFINED | — |
| PROD-003 | Production | tenant incorreto não contamina fluxo | DEFINED | — |
| PROD-004 | Production | unidade incorreta não contamina fluxo | DEFINED | — |
| PROD-005 | Production | fluxo incompleto não é declarado completo | DEFINED | — |
| MEM-001 | Memory | observação autorizada entra no temporal | DEFINED | — |
| MEM-002 | Memory | observação não autorizada é rejeitada | DEFINED | — |
| MEM-003 | Memory | promoção para evolução é explícita | DEFINED | — |
| MEM-004 | Memory | proveniência é preservada | DEFINED | — |
| MEM-005 | Memory | tenant/domain permanecem isolados | DEFINED | — |
| ADV-001 | Adversarial | tenant correto + unidade errada | DEFINED | — |
| ADV-002 | Adversarial | unidade correta + tenant errado | DEFINED | — |
| ADV-003 | Adversarial | confiança alta + escopo errado | DEFINED | — |
| ADV-004 | Adversarial | fonte autorizada + evidência contraditória | DEFINED | — |
| ADV-005 | Adversarial | discovery válido + evidência insuficiente | DEFINED | — |
| ADV-006 | Adversarial | provider disponível sem autorização | DEFINED | — |
| ADV-007 | Adversarial | componente experimental tratado como canônico | DEFINED | — |
| GOV-001 | Governance | Evolution Gate classifica mudança | PASS | PR #70 / Evolution Gate |
| GOV-002 | Governance | UNKNOWN não vira PASS | DEFINED | — |
| GOV-003 | Governance | merge exige gates verdes | PASS | PR #70 / PR1 validation |
| GOV-004 | Governance | diff final é revisado contra baseline | DEFINED | — |

## Medição atual

Casos totais: **44**

- PASS: **14**
- FAIL: **0**
- DEFINED: **30**
- UNKNOWN: **0**
- BLOCKED: **0**

**Positivos executados: 100% (14/14).**

**Cobertura automatizada comprovada: 31,8% (14/44).**

A diferença entre os dois números é intencional: os 14 casos PASS são evidência real; os 30 restantes ainda precisam de execução automatizada.

## Próximo gate

Priorizar a execução de `CTX`, `SRC`, `GPT`, `DIAG`, `PROD`, `MEM` e `ADV` na ordem acima. Não aumentar o percentual por reclassificação documental. Um caso só muda para `PASS` com evidência de execução.
