# Inteligência de Demanda

## Objetivo

Definir a Inteligência de Demanda como um domínio central da EIP do ELO, responsável por transformar sinais de negócio, dados históricos e restrições de capacidade em previsões, cenários e recomendações para planejamento e execução.

## Papel na EIP

A Inteligência de Demanda é a porta de entrada analítica do ELO. Ela deve receber informações de múltiplas fontes, consolidá-las em contexto governado e alimentar outros domínios e agentes com recomendações rastreáveis.

Essa capacidade pode ser utilizada por diferentes empresas do setor industrial, desde que seus sistemas especialistas, fontes de dados e regras locais sejam integrados ao ELO por contratos explícitos.

## Entradas

- SO
- Orçamentos
- AF históricas
- Calendário
- Histórico de produção
- Tendências do mercado
- Sazonalidade
- Crescimento esperado
- Capacidade produtiva

## Análises

- Forecast
- Cenários
- Simulações
- Riscos
- Tendências

## Saídas

- Plano Mestre de Produção
- Plano de Compras
- Plano de Capacidade
- Alertas
- Recomendações

## Domínios que consomem o resultado

1. Inteligência de Demanda
2. Engenharia e Produtos
3. Planejamento Estratégico
4. Planejamento Operacional (PCP)
5. Suprimentos
6. Produção
7. Logística
8. Operação Externa
9. Manutenção
10. Inteligência Operacional
11. Conhecimento
12. Analytics
13. IA
14. Governança

## Perguntas que o ELO deve responder

### Planejamento

- Quais modelos terão maior demanda nos próximos meses?
- Qual família de produtos tende a crescer?
- Quais instalações terão maior consumo?
- Qual capacidade produtiva será necessária?
- Quando será necessário ampliar compras?

### Engenharia

- Quais modelos apresentam maior número de revisões?
- Quais componentes geram mais alterações?
- Quais listas BOM possuem maior impacto financeiro?
- Quais projetos geram maior retrabalho?

### Almoxarifado

- Quais itens da Lista Mãe terão ruptura?
- Quais itens Curva A precisam ser comprados antecipadamente?
- Quais materiais possuem baixa rotatividade?
- Qual estoque cobre a demanda prevista?

### Produção

- Qual recurso será o gargalo?
- Qual instalação concentrará maior carga?
- Quais modelos gerarão maior consumo de horas?
- Qual sequência reduz setup?

### Manutenção

- Quais modelos apresentam maior reincidência?
- Quais componentes falham com maior frequência?
- Qual fornecedor está associado às maiores ocorrências?
- Como essas falhas impactam futuras decisões de engenharia?

### Gestão

- Qual será a necessidade de investimento?
- A fábrica possui capacidade para a carteira prevista?
- Quais riscos existem para os próximos meses?
- Onde estão os maiores gargalos?

## Fluxo de decisão

```text
Entradas
  ↓
Inteligência de Demanda
  ↓
Forecast / Cenários / Simulações / Riscos / Tendências
  ↓
Conhecimento e recomendações
  ↓
Plano Mestre de Produção / Compras / Capacidade / Alertas
  ↓
Decisão
  ↓
Execução e retroalimentação
```

## Regras arquiteturais

- nenhuma previsão deve ser tratada como fato sem identificação de horizonte, fonte e nível de confiança
- recomendações devem ser rastreáveis às entradas e análises que as produziram
- capacidade produtiva deve participar da análise de demanda para evitar planos inexequíveis
- resultados devem alimentar planejamento estratégico, PCP e suprimentos sem duplicar sistemas especialistas
- histórico de execução deve retroalimentar os modelos de previsão
- decisões humanas relevantes devem permanecer auditáveis

## Integração cognitiva

A Inteligência de Demanda deve fornecer objetos de conhecimento estruturados para Analytics, RAG e agentes de IA. A IA não deve depender diretamente de tabelas físicas para formar decisões; deve consumir contexto governado e rastreável.

## Indicadores sugeridos

- acurácia do forecast
- erro absoluto e percentual da previsão
- aderência do Plano Mestre de Produção
- utilização prevista versus capacidade disponível
- risco de ruptura
- cobertura de estoque projetada
- percentual de recomendações aceitas
- divergência entre cenário previsto e realizado

## Rastreabilidade

Este documento deve permanecer alinhado ao Modelo Conceitual, Entidades, Relacionamentos, Modelo Lógico, Recursos Estratégicos, Knowledge Model, RAG e regras de governança do ELO.
