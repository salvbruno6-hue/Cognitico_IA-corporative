# ELO — Protocolo de Manutenção Lógica e Autocoordenação

## Finalidade

Estabelecer a regra canônica para que o ELO mantenha coerência semântica, ownership documental, fluidez arquitetural e ausência de duplicidades durante evolução, migração, consolidação e remoção de artefatos.

## Princípio

O repositório é tratado como um sistema de conhecimento. Um arquivo não deve ser avaliado isoladamente: sua função, conteúdo, consumidores, referências, aliases e posição na cadeia lógica devem ser considerados em conjunto.

## Ciclo obrigatório

`Descobrir → Classificar → Comparar → Reconciliar → Canonicalizar → Redirecionar referências → Validar consumidores → Testar resolução → Atualizar documentação → Depreciar → Remover → Validar novamente`

## Regras

1. **Owner primeiro** — antes de criar ou manter um artefato, determinar qual é o owner canônico de sua responsabilidade.
2. **Responsabilidade única** — cada artefato deve possuir uma função semântica identificável.
3. **Complementação antes da remoção** — conteúdo válido de uma variante deve ser incorporado ao owner canônico antes da remoção da variante.
4. **Não duplicar para preservar conteúdo** — conteúdo complementar deve ser integrado, não mantido em owners paralelos.
5. **Proveniência obrigatória** — toda migração relevante deve registrar origem e destino.
6. **Consumidores e referências** — nenhum caminho legado pode ser removido enquanto referências ou consumidores relevantes permanecerem sem resolução.
7. **Aliases explícitos** — quando necessário, aliases devem apontar para o owner canônico e não criar autoridade concorrente.
8. **Gates separados** — conteúdo, referências, consumidores, runtime e remoção física devem ser validados separadamente.
9. **Loop de resolução** — se qualquer gate falhar, o ELO retorna à etapa correspondente, corrige e executa novamente até fechamento.
10. **README como índice vivo** — a documentação de navegação deve refletir a árvore efetivamente canônica.
11. **Coerência transversal** — uma mudança em uma família deve ser avaliada quanto aos impactos em famílias consumidoras.
12. **Bloqueio preventivo** — conflito semântico não resolvido impede consolidação ou remoção definitiva.

## Ordem de decisão semântica

Quando dois artefatos possuem nomes ou funções semelhantes, aplicar:

`mesma responsabilidade? → complementar? → conflito? → histórico? → owner canônico?`

- Se **mesma responsabilidade**: consolidar.
- Se **complementar**: incorporar ao owner.
- Se **conflito**: registrar decisão antes de remover.
- Se **histórico**: preservar apenas como evidência quando houver valor justificável.
- Se **sem valor**: depreciar e remover após os gates.

## Aplicação à Família 00

A Família 00 é a referência inicial do modelo. Sua cadeia canônica é:

`Missão → Objetivos → Capacidades → Cadeia de Valor → Modelo Operacional → Stakeholders → Regras Estratégicas`

O `ENTERPRISE_MANIFEST.md` atua como agregador e não como segundo owner de conteúdo.

## Estado esperado

Uma família consolidada deve possuir:

- um owner canônico por responsabilidade;
- ausência de duplicidade semântica não justificada;
- referências resolvidas;
- consumidores reconciliados;
- documentação atualizada;
- testes de resolução aprovados;
- remoção física somente após os gates anteriores.

## Regra de evolução do próprio protocolo

Qualquer nova experiência de consolidação que revele uma falha recorrente deve resultar em atualização deste protocolo ou de uma regra especializada, evitando que o mesmo problema seja resolvido manualmente de forma repetitiva.
