# Symbiont Skill Approval Loop

## Finalidade

Criar um ciclo repetível para transformar uma habilidade observada em uma capacidade documentada e testável, sem confundir:

- habilidade definida;
- execução operacional;
- evidência;
- candidato;
- aprovação;
- decisão de implementação;
- promoção canônica.

## Loop

`DISCOVERED`
→ identificar a habilidade e sua origem

`SPECIFIED`
→ criar/atualizar o arquivo `SKILL-*.md`

`TESTING`
→ executar testes positivos, negativos, regressão, segurança e limites

`EVIDENCE_READY`
→ consolidar evidências, commits, runs e outcomes

`REVIEW`
→ revisar arquitetura, segurança, tenant, proveniência e Evolution Gate

`APPROVED`
→ registrar aprovação explícita do candidato

ou

`REJECTED / BLOCKED`
→ registrar causa objetiva e manter o candidato fora do fluxo de promoção

## Pós-aprovação e implementação

Um candidato **já aprovado** não precisa voltar para descoberta ou aprovação. Ele entra em um fluxo controlado quando existir uma decisão explícita de implementação:

`APPROVED → IMPLEMENTATION_DECIDED → DEPLOYED/USED → OBSERVING → OUTCOME → REVIEW`

A decisão `APPROVE` de implementação dispara automaticamente a transição para implantação controlada.

`HOLD` ou `REJECT` interrompe o fluxo e resulta em `BLOCKED`.

Uma implantação com falha também resulta em `BLOCKED`.

O executor do loop não concede aprovação, não altera o Evolution Gate e não promove conhecimento por conta própria. Ele apenas executa uma decisão de implementação já autorizada.

Implementação canônica do loop:
`src/elo/core/skill_approval_deployment_loop.py`

Testes:
`tests/core/test_skill_approval_deployment_loop.py`

## Relação com a cadeia de ações

A documentação de uma skill deve permitir responder:

1. Quem iniciou a ação?
2. Qual intenção originou a ação?
3. Qual contrato autorizou?
4. Qual skill foi utilizada?
5. Qual executor foi chamado?
6. Qual evidência foi produzida?
7. Qual outcome ocorreu?
8. Qual observação entrou no laboratório?
9. Qual candidato foi criado?
10. Quais testes foram executados?
11. Qual decisão de revisão ocorreu?
12. Qual Evolution Gate foi aplicado?
13. Houve aprovação humana?
14. O candidato permaneceu candidato ou tornou-se elegível para promoção?
15. Qual decisão de implementação foi tomada?
16. Qual resultado pós-aprovação foi observado?

## Regra de auditoria

A auditoria deve poder navegar nos dois sentidos:

**ação → skill → evidência → candidato → aprovação → implementação → outcome**

e:

**candidato → evidência → skill → ação → outcome → revisão**

## Separação das pastas

### `docs/symbiont-skills/`

Define o comportamento esperado da habilidade.

### `docs/symbiont-candidates/`

Registra instâncias concretas de candidatos e sua aprovação.

### `tests/`

Contém a verificação executável.

### `src/elo/`

Contém a implementação canônica.

Nenhuma dessas camadas substitui as autoridades existentes.

## Gate de aprovação

A aprovação deve falhar fechado quando faltar:

- identidade;
- tenant/scope;
- proveniência;
- evidência;
- teste de limite;
- teste de regressão;
- classificação de evolução quando aplicável;
- revisão exigida.

## Regra de segurança

Somente candidatos com estado explícito `APPROVED`, referência de aprovação e evidência podem receber uma decisão de implementação.

A automação não transforma `GREEN`, `READY_FOR_APPROVAL` ou `PROMOTION_ELIGIBLE` em `APPROVED`.

Também não transforma `APPROVED` diretamente em promoção canônica.

## Pós-aprovação

Depois de aprovado, o candidato continua sendo rastreado até seu outcome pós-aprovação. Uma aprovação não encerra o ciclo; ela abre a etapa de implementação e observação.

O resultado pós-aprovação deve alimentar os mecanismos canônicos existentes de outcome/learning, não uma memória paralela.
