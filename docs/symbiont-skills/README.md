# Symbiont Skills — Governança, Testes e Aprovação

## Objetivo

Esta árvore documenta cada habilidade operacional/cognitiva que pode ser executada pela cadeia Symbiont e define sua posição na cadeia de ações, seus limites, evidências, testes e critérios de aprovação.

Ela é documentação governada da arquitetura existente. Não cria uma nova autoridade de execução, memória, autorização ou Evolution Gate.

## Cadeia canônica

`intenção → ELO Cognitive → autorização → Symbiont/Hermes → execução governada → evidência → outcome → DOL → laboratório → candidato → avaliação → Evolution Gate → aprovação → promoção canônica`

Uma habilidade deve declarar explicitamente:

1. qual problema resolve;
2. qual entrada recebe;
3. quem autoriza;
4. qual componente executa;
5. quais operações são permitidas;
6. quais operações são proibidas;
7. quais evidências produz;
8. qual outcome precisa ser observado;
9. quais testes comprovam seu comportamento;
10. quais condições bloqueiam sua aprovação;
11. qual é seu próximo elo na cadeia;
12. se o resultado é apenas operacional, evidência de laboratório, candidato ou conhecimento canônico.

## Regra de separação

- **Skill definition**: `docs/symbiont-skills/`
- **Candidate approval/audit**: `docs/symbiont-candidates/`
- **Código canônico**: `src/elo/`
- **Testes executáveis**: `tests/`

A pasta de candidatos não concede autoridade. Ela registra evidências e decisões de aprovação/reprovação para auditoria.

## Estados do loop de aprovação

`DISCOVERED → SPECIFIED → TESTING → EVIDENCE_READY → REVIEW → APPROVED | REJECTED | BLOCKED → PROMOTION_ELIGIBLE`

`PROMOTION_ELIGIBLE` não significa promoção automática. A materialização continua subordinada aos contratos canônicos.

## Critério mínimo de aprovação

Uma habilidade só pode ser marcada como aprovada quando houver:

- identidade e escopo definidos;
- tenant/scope validado;
- autorização explícita;
- operações permitidas e bloqueadas;
- evidência de execução;
- teste positivo;
- teste negativo dos limites;
- regressão sem falha;
- proveniência preservada;
- ausência de segredo/infraestrutura indevida;
- Evolution Gate aplicável e resultado registrado quando houver evolução;
- responsável/revisor registrado.

## Auditoria

Cada candidato aprovado deve apontar para:

- skill_id;
- candidate_id;
- source_ref/source_commit;
- evidências;
- testes;
- decisão de revisão;
- classificação do Evolution Gate;
- eventual aprovação humana;
- resultado pós-aprovação.

Nunca registrar credenciais, chaves, secrets ou identificadores de infraestrutura sensíveis nesses documentos.
