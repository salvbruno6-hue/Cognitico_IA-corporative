# OPERAÇÃO 05 — PRODUÇÃO

## Papel no fluxo

Executa a fabricação e montagem. O fluxograma deve ser interpretado como fluxo de produção, não como simples lista de tarefas.

## Três caminhos produtivos que o ELO deve distinguir

### 1. Fabricação linear

É a fabricação que segue o fluxo produtivo padrão, com sequência previamente definida.

Base principal:

- `fluxo_produtivo_modular`
- `fluxo_produtivo_modular_etapas`
- `mt_operacoes_roteiro`
- `mt_ordens_producao`
- `mt_operacoes_ordem_producao`
- `mt_eventos_fluxo_modular`

### 2. Fabricação customizada / personalizada

**É uma operação própria dentro da produção e não pode ser absorvida pela fabricação linear.**

Ela começa quando a análise da AF/projeto identifica que o módulo não pode seguir integralmente o roteiro padrão.

A cadeia deve ser preservada:

`AF / projeto → identificação da customização → roteiro personalizado → aprovação → fabricação → execução real → inspeção`

Base principal:

- `mt_pedidos_venda_itens.personalizado`
- `mt_pedidos_venda_itens.status_personalizacao`
- `mt_versoes_roteiro_personalizado`
- `mt_operacoes_roteiro_personalizado`
- `mt_ordens_producao`
- `mt_operacoes_ordem_producao`
- `mt_eventos_fluxo_modular`
- `mt_inspecoes`
- `mt_nao_conformidades`

### O que precisa ser aprendido com o especialista da fabricação customizada

O ELO deve perguntar:

1. O que torna uma fabricação customizada diferente da fabricação padrão?
2. Qual é a origem da customização: AF, projeto, cliente ou alteração técnica?
3. Como a necessidade é formalizada?
4. Quem aprova a alteração?
5. Como é criada a versão do roteiro personalizado?
6. Quais operações padrão permanecem?
7. Quais operações são incluídas, removidas ou alteradas?
8. Como os tempos são definidos?
9. Como os materiais adicionais são identificados?
10. Como a capacidade necessária é calculada/registrada?
11. Como a execução real é apontada?
12. Como a qualidade é verificada?
13. O que acontece quando a customização gera falha ou retrabalho?

O ELO **não deve presumir** que uma alteração seja customização apenas porque parece diferente. Deve existir evidência no pedido/projeto ou regra operacional validada.

### 3. Montagem de componentes

A montagem ocorre sobre a unidade produzida e pode possuir ordem específica de montagem.

Base principal:

- `mt_ordens_montagem`
- `mt_unidades_modulares`
- `mt_eventos_fluxo_modular`

## Estrutura de decisão

`Pedido/AF`
→ `Padrão ou customizado?`

**Padrão**

`roteiro padrão → OP → operações → execução → inspeção`

**Customizado**

`projeto/customização → roteiro personalizado → aprovação → OP → operações personalizadas → execução → inspeção`

O caminho customizado deve permanecer identificável na rastreabilidade da ordem e das operações.

## Tabelas primárias da produção

- `fluxo_produtivo_modular`
- `fluxo_produtivo_modular_etapas`
- `mt_pedidos_venda_itens`
- `mt_versoes_roteiro_personalizado`
- `mt_operacoes_roteiro_personalizado`
- `mt_ordens_producao`
- `mt_operacoes_roteiro`
- `mt_operacoes_ordem_producao`
- `mt_capacidade_diaria`
- `mt_eventos_fluxo_modular`
- `mt_ordens_montagem`
- `mt_unidades_modulares`
- `mt_inspecoes`
- `mt_nao_conformidades`

## Regra de planejado × realizado

**Planejado:**

- pedido/configuração;
- roteiro;
- versão do roteiro personalizado;
- operações;
- OP;
- quantidade;
- capacidade;
- datas.

**Realizado:**

- eventos de execução;
- quantidade produzida/concluída;
- início/fim real;
- materiais efetivamente movimentados;
- inspeção;
- retrabalho/reparo quando comprovado.

O ELO nunca deve transformar o roteiro personalizado em evidência de que a operação ocorreu. Roteiro é planejamento; evento de execução é evidência do realizado.

## Regra de qualidade

`produção → teste/inspeção → OK → liberação`

ou

`produção → teste/inspeção → falha → não conformidade/reparo → retorno`

O ELO não deve inventar o critério de aprovação.

## Saída

Unidade produzida, inspecionada e liberada; ou desvio rastreável para recuperação.
