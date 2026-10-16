# ELO — Orquestração de fontes da estrutura metálica modular 20 pés

## Objetivo

Fazer o `KnowledgeOrchestrator` orientar qual fonte consultar e qual destino de persistência usar para dados da estrutura metálica modular 20 pés, sem criar uma segunda autoridade de recuperação ou memória.

A arquitetura existente permanece válida:

- `public.elo_conhecimento_regras_routing` decide para onde a intenção deve ser encaminhada;
- `public.elo_conhecimento_fontes` registra quais tabelas são fontes e qual papel exercem;
- tabelas operacionais continuam sendo as autoridades dos dados físicos;
- VWs são superfícies de leitura derivada;
- `public.elo_orcamento_memoria` hospeda memória de cálculo validada;
- `public.lista_mae` hospeda identidade e valor canônico de itens;
- `public.kit_itens` hospeda aplicação concreta em composições.

## Mapa de autoridade

| Intenção | Fonte de consulta | Persistência correta | Regra |
|---|---|---|---|
| Peças, componentes, COD_PRODUT, peso utilizado, grupo de material | `public.estrutura_metalica_20_componentes` | `public.estrutura_metalica_20_componentes` após validação | A VW não é fonte de edição |
| Perda, sobra, diferença, peso comprado/utilizado, percentual e impacto | `public.vw_perda_estrutura_metalica_20` | corrigir a fonte física ou a memória; nunca escrever na VW | A VW é derivada |
| Fórmula, origem, evidência e justificativa do cálculo | `public.elo_orcamento_memoria` | `public.elo_orcamento_memoria` | usar `conceito_key = PERDA_ESTRUTURA_METALICA_MODULAR_20_PES` |
| Cadastro do item `PERDA-EST-MET` | `public.lista_mae` | `public.lista_mae` sob governança | identidade, unidade, valor canônico, curva, obrigatoriedade, aplicabilidade |
| Em quais kits/modelos o item está efetivamente aplicado | `public.kit_itens` + `public.lista_mae` | `public.kit_itens` somente com evidência da composição | aplicabilidade geral não autoriza replicação automática |

## Regras específicas cadastradas

- `ROUTE-EST-MET-20-COMPONENTES`
- `ROUTE-EST-MET-20-PERDA`
- `ROUTE-EST-MET-20-MEMORIA`
- `ROUTE-EST-MET-20-CADASTRO`
- `ROUTE-EST-MET-20-COMPOSICAO`

As regras têm prioridade 31–35, antes dos roteamentos genéricos de material e orçamento, para que o orquestrador use primeiro a fonte especializada quando a intenção for claramente da estrutura metálica modular 20 pés.

## Regra de hospedagem

Não criar nova tabela universal de memória ou nova tabela de orquestração para este assunto.

O roteador deve morar em `elo_conhecimento_regras_routing`; o catálogo de fontes deve morar em `elo_conhecimento_fontes`. Cada dado deve permanecer hospedado no domínio que é sua autoridade operacional/cognitiva.

## Escopo

Este roteamento é transversal a **todos os módulos 20 pés que utilizam a estrutura metálica modular 20 pés**. Não é exclusivo do MLT.M01.

A planilha PCP pode consumir os mesmos pesos unitários para planejamento, mas não substitui a fonte física por componente. Para o conjunto de 120 MLT.M01, por exemplo, a planilha usa consumos como 141,52 kg de chapa 2,70 mm, 73,56 kg de UDC 6, 133,78 kg de UDC 5, 45,08 kg de UDC 3 e 91,15 kg de UDC 8 por estrutura; esses consumos são projeções de planejamento derivadas da base unitária da estrutura.

## Migração

`20261016182319_rotear_elo_fontes_estrutura_metalica_20.sql`
