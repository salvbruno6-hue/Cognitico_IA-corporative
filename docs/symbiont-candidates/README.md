# Symbiont Candidates — Aprovação e Auditoria

Esta árvore é o registro organizado dos candidatos produzidos pelo laboratório/Symbiont. Ela é deliberadamente separada de `docs/symbiont-skills/`.

## Regra

Um candidato não é uma habilidade canônica.

O candidato deve permanecer rastreável até sua origem:

`candidate_id → skill_id → observation_id → decision_id → evidence → tests → Evolution Gate → review → outcome`

## Estrutura

Cada candidato deve ter um diretório:

`docs/symbiont-candidates/<candidate_id>/`

com:

- `CANDIDATE.md` — identidade, origem e escopo;
- `TESTS.md` — testes executados e evidências;
- `APPROVAL.md` — decisão de aprovação, rejeição ou bloqueio;
- `POST_APPROVAL.md` — somente quando aprovado, resultado pós-aprovação.

## Estados

`CANDIDATE → TESTING → EVIDENCE_READY → REVIEW → APPROVED | REJECTED | BLOCKED`

Somente após `APPROVED` o candidato pode entrar no fluxo de elegibilidade de promoção. Mesmo assim, promoção canônica exige os gates já existentes.

## Proibições

Esta árvore não pode:

- conceder autorização;
- substituir Evolution Gate;
- substituir GovernedLearningService;
- criar memória paralela;
- declarar promoção canônica apenas por edição de Markdown;
- armazenar secrets ou credenciais.

## Auditoria

Uma auditoria pode partir de um candidato e percorrer toda a cadeia até o código e os testes, sem misturar candidatos entre si.
