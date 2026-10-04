# Simbionte — Diagnóstico de Status de Capacidade

**Status:** implementação de diagnóstico read-only  
**Owner:** ELO Cognitive / Symbiont  
**Autoridade:** nenhuma nova; reutiliza contratos, evidências, runtime owner e Evolution Gate existentes.

## Objetivo

Permitir que a Simbionte responda, para uma capability específica:

- qual é o status atual;
- quais condições estão satisfeitas;
- quais condições estão ausentes ou sem evidência;
- quais bloqueios existem;
- quais evidências sustentam cada condição;
- se existe integração no runtime real;
- se existe evidência operacional;
- se existe resultado de produção explicitamente comprovado;
- qual é o próximo passo exato.

## Condições avaliadas

1. CONTRACT
2. IMPLEMENTATION
3. TESTS
4. EVIDENCE
5. RUNTIME_INTEGRATION
6. OPERATIONAL_EVIDENCE
7. PRODUCTION_OUTCOME
8. GOVERNANCE_APPROVAL

Uma condição só é **VERIFIED** quando possui referência explícita de evidência. A ausência de referência não é convertida em sucesso.

## Status possíveis

| Status | Significado |
|---|---|
| NOT_IMPLEMENTED | implementação não comprovada |
| IMPLEMENTED_NOT_TESTED | implementação presente, teste não comprovado |
| TESTED_NOT_EVIDENCED | testes presentes, evidência não comprovada |
| EVIDENCED_NOT_RUNTIME | evidência existe, mas runtime real não está conectado |
| RUNTIME_INTEGRATED | runtime integrado, ainda sem evidência operacional |
| OPERATIONALLY_EVIDENCED | há evidência operacional, mas produção ainda não está comprovada |
| READY_FOR_EVOLUTION_GATE | resultado de produção explícito existe, mas governança ainda não autorizou |
| PRODUCTION_PROVEN | resultado de produção e evidência de governança explicitamente comprovados |
| BLOCKED | existe bloqueio explícito |

## Regras de segurança

- Não inferir produção a partir de testes.
- Não inferir runtime a partir da existência de código.
- Não inferir evidência a partir de documentação.
- Não transformar COMPLETED em aprendizado.
- Não autorizar promoção.
- Não executar deploy.
- Não alterar memória canônica.
- Não criar outro Evolution Gate.
- Não criar outro owner.
- canonical_mutation permanece false.

## Execução

A interface executável é:
scripts/run_symbiont_capability_status.py

Ela recebe um JSON com os estados explicitamente observados e retorna um relatório determinístico.

A saída pode alimentar o loop existente da Simbionte para decidir onde investigar ou intervir, sem substituir o owner responsável pela decisão final.
