# OPERAÇÃO 05 — PRODUÇÃO

## Papel no fluxo

Executa a fabricação e montagem. O fluxograma deve ser interpretado como fluxo de produção, não como simples lista de tarefas.

## Linhas de execução que o ELO deve distinguir

1. fabricação linear;
2. fabricação personalizada;
3. montagem de componentes;
4. operações que podem ocorrer em paralelo quando documentadas;
5. inspeção/teste e retorno para correção.

## Tabelas primárias

- `fluxo_produtivo_modular`
- `fluxo_produtivo_modular_etapas`
- `mt_ordens_producao`
- `mt_operacoes_roteiro`
- `mt_operacoes_roteiro_personalizado`
- `mt_operacoes_ordem_producao`
- `mt_capacidade_diaria`
- `mt_eventos_fluxo_modular`
- `mt_ordens_montagem`
- `mt_unidades_modulares`
- `mt_inspecoes`
- `mt_nao_conformidades`

## O que o especialista deve ensinar

- significado de cada etapa;
- recurso/centro de trabalho;
- tempos padrão e setup;
- capacidade real;
- dependências;
- paralelismo;
- critérios de conclusão;
- critérios de teste;
- retorno para retrabalho/reparo.

## Regra de planejado × realizado

Planejado: `mt_ordens_producao`, `mt_operacoes_ordem_producao`, roteiro e capacidade.

Realizado: eventos e campos reais de execução, quantidade produzida/concluída, início/fim real e inspeção.

## Regra de qualidade

`produção → teste/inspeção → OK → liberação`

ou

`produção → teste/inspeção → falha → não conformidade/reparo → retorno`

O ELO não deve inventar o critério de aprovação.

## Saída

Unidade produzida, inspecionada e liberada; ou desvio rastreável para recuperação.
