# ELO-ORG — Protocolo de Validação e Merge

## Objetivo

Estabelecer o protocolo obrigatório para validar a estrutura empresarial ELO-ORG antes de qualquer merge em `main`.

A implementação deve permanecer uma capacidade delimitada do ELO. Ela não cria um segundo Cognitive Core, uma memória paralela ou uma fonte de verdade específica de domínio.

## 1. Gates obrigatórios

### G1 — Integridade estrutural
- pacote Python deve possuir nome importável;
- nenhum caminho duplicado deve representar a mesma capacidade;
- a localização da capacidade deve ser coerente com `members/ELO_ORG`;
- imports dos testes devem apontar para a localização canônica.

### G2 — Integridade técnica
- instalação `.[test]` deve passar;
- `python -m compileall src` deve passar;
- suíte completa `python -m pytest -q` deve passar;
- não aceitar erro de coleta, import ou teste ignorado como sucesso.

### G3 — Integridade semântica
A validação deve comprovar:
- `SUPPORTED` somente quando todas as relações necessárias estiverem presentes;
- `INCONCLUSIVE` quando houver relação empresarial ausente ou insuficientemente demonstrada;
- `BLOCKED` quando faltar contexto mínimo de execução;
- `CONFLICTING` não deve ser inferido sem evidência de conflito real.

### G4 — Evidência e proveniência
Toda relação cross-domain deve possuir `evidence_ref`.
Nenhuma relação pode ser tratada como fato apenas porque aparece na sequência de um fluxo.

### G5 — Isolamento organizacional
Fluxos devem preservar `tenant_id` e `principal_id`.
Falha de contexto deve bloquear a análise em vez de produzir uma conclusão.

### G6 — Temporalidade
Relações devem preservar `valid_from` e, quando aplicável, `valid_until`.
Alterações futuras não podem ser tratadas como válidas fora do período declarado.

### G7 — Compatibilidade arquitetural
Antes do merge, o ELO deve verificar:
1. reutilização de contratos existentes;
2. ausência de duplicação de Cognitive Core;
3. ausência de memória paralela;
4. ausência de fonte de verdade empresarial fora dos contratos canônicos;
5. ausência de lógica de decisão humana sendo substituída silenciosamente por heurística de IA.

### G8 — Evidência de CI
A decisão de merge somente pode ocorrer após nova execução do conjunto de gates sobre o commit final da PR.
Execução anterior ao último ajuste não é evidência suficiente.

## 2. Matriz mínima de testes

| Caso | Resultado esperado |
|---|---|
| cadeia empresarial completa com evidência | `SUPPORTED` |
| relação entre domínios ausente | `INCONCLUSIVE` |
| tenant ausente | `BLOCKED` |
| principal ausente | `BLOCKED` |
| relação sem evidência | rejeitada |
| domínio inexistente | rejeitado/`INCONCLUSIVE`, sem falsa confirmação |
| fluxo vazio | `BLOCKED` |
| evidência preservada | refs retornadas na análise |

## 3. Protocolo de ajuste

Quando um gate falhar:

1. classificar a falha como técnica, estrutural, semântica, de evidência ou arquitetural;
2. corrigir a menor superfície necessária;
3. não alterar contratos canônicos para fazer um teste passar;
4. adicionar ou ajustar teste que reproduza a falha;
5. executar novamente os gates;
6. registrar o resultado no PR;
7. somente então reavaliar o merge.

## 4. Critério de decisão

- **MERGE:** todos os gates G1–G8 aprovados e nenhuma incompatibilidade arquitetural aberta.
- **ADJUST:** falha corrigível sem alteração de arquitetura canônica.
- **BLOCK:** conflito arquitetural, ausência de evidência ou risco de duplicação de núcleo/fonte de verdade.
- **HUMAN DECISION:** mudança que altere identidade, Soul, Cognitive Core, governança fundamental ou contrato canônico.

## 5. Regra final

`CI verde` é condição necessária, mas não suficiente para o merge.

O merge representa a aprovação simultânea da integridade técnica, semântica, evidencial e arquitetural da capacidade ELO-ORG.
