# ELO — Status da Auditoria de Consolidação

## Data
2026-08-19

## Estado
`IN_PROGRESS — STRUCTURAL GATE`

## Concluído

- ponto primário de modificação definido;
- identidade lógica definida;
- regra de preservação de proveniência definida;
- matriz de classificação criada;
- impacto de mudança de endereço documentado;
- branch de auditoria criada;
- testes de invariantes de governança adicionados;
- `src/elo/` preservado sem alteração nesta fase.

## Em execução

- inventário físico completo das famílias PT/EN;
- comparação semântica arquivo-a-arquivo;
- cálculo/registro de identidade e conteúdo;
- levantamento de referências;
- classificação EQ/CP/CF/EX/HI/NR.

## Bloqueios deliberados

A consolidação física e a remoção de árvores históricas permanecem bloqueadas até que:

1. todos os arquivos relevantes sejam classificados;
2. conflitos tenham decisão explícita;
3. conteúdo exclusivo seja preservado;
4. referências sejam atualizadas;
5. testes passem;
6. CI esteja verde;
7. nenhum consumidor crítico permaneça dependente do endereço histórico.

## Decisão arquitetural

Não criar um segundo Core, segundo SourceResolver ou segunda autoridade de conhecimento. O índice canônico deve complementar a infraestrutura de resolução existente.
