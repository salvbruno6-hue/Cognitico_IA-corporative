# ELO — Status da Auditoria de Consolidação

## Data
2026-08-19

## Estado
`IN_PROGRESS — STRUCTURAL GATE`

## Concluído

- ponto primário de modificação definido;
- registro canônico de identidade materializado como contrato documental;
- distinção entre identidade lógica e endereço físico formalizada;
- regra de preservação de proveniência definida;
- matriz de classificação criada;
- impacto de mudança de endereço documentado;
- protocolo de evidência de CI formalizado;
- terminologia de `workflow run` versus evento `workflow_run` corrigida;
- branch de auditoria criada;
- testes de invariantes de governança adicionados;
- `src/elo/` preservado sem alteração nesta fase.

## Em execução

- inventário físico completo das famílias PT/EN;
- comparação semântica arquivo-a-arquivo;
- atribuição de identidade somente após evidência de conteúdo;
- levantamento de referências e consumidores;
- classificação EQ/CP/CF/EX/HI/NR;
- materialização do mapa de referências;
- validação dos gates T01–T10.

## Evidência atual

O CI do SHA anterior `9b1e2fd967c0a3df3854f1c338f0cf667e3ff258` passou no ELO Evolution Gate #728.

As alterações documentais posteriores a esse run exigem nova execução do CI para o novo HEAD antes de qualquer decisão de merge.

## Bloqueios deliberados

A consolidação física e a remoção de árvores históricas permanecem bloqueadas até que:

1. todos os arquivos relevantes sejam classificados;
2. conflitos tenham decisão explícita;
3. conteúdo exclusivo seja preservado;
4. referências e consumidores sejam mapeados e atualizados quando necessário;
5. identidade e proveniência sejam materializadas;
6. testes passem;
7. CI esteja verde no HEAD atual;
8. nenhum consumidor crítico permaneça dependente do endereço histórico;
9. T01–T10 estejam efetivamente demonstrados, e não apenas descritos em checklist.

## Decisão arquitetural

Não criar um segundo Core, segundo SourceResolver ou segunda autoridade runtime de conhecimento. O registro/índice canônico deve complementar a infraestrutura de resolução existente.

## Próxima ação primária

Auditar as famílias estruturais `00`, `01`, `05`, `07`, `11`, `12`, `13`, `14` e `15` arquivo-a-arquivo, preencher o registro sem inferência nominal e materializar o mapa de referências antes de qualquer depreciação ou remoção.
