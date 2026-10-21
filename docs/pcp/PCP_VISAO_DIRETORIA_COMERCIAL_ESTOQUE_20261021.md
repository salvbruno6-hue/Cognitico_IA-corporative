# PCP — Visão Diretiva Comercial, Demanda e Estoque

**Data:** 2026-10-21  
**Fonte primária desta baseline:** `Cópia de Relatório Comercial (1).csv`  
**SHA-256:** `181cba3132f844e855fa8f846ef25b7f1b41d6d147bc33acda5bda59e4daf59a`  
**Regra:** `DIRETORIA_COMERCIAL_ESTOQUE_V1`  
**Status:** BASELINE ANALÍTICA / NÃO OPERACIONAL

## Objetivo

Disponibilizar uma única leitura para Diretoria e PCP, filtrável por:

- nível `FAMILIA` ou `MODELO`;
- família `MODULO` ou `CONTEINER`;
- ano e mês;
- histórico ou previsão-base.

A camada não cria uma nova autoridade comercial. O CSV é preservado como evidência de origem e a tabela privada guarda somente agregados derivados. Quando os dados canônicos estiverem carregados e reconciliados, a view integra `v_elo_pcp_cobertura_demanda_externa`.

## Objetos

- `elo_private.pcp_diretoria_comercial_mensal`: snapshot analítico derivado.
- `public.v_elo_diretoria_comercial_estoque`: read-model executivo.

## Métricas comerciais

Para cada família/modelo/mês:

- demanda total;
- SPOT = linhas de `LOCAÇÃO`;
- EVENTO = linhas de `EVENTO`;
- venda;
- transferências separadas da demanda comercial;
- participação percentual SPOT/EVENTO/VENDA;
- participação do mês no ano;
- índice de sazonalidade = demanda do mês / média mensal do mesmo ano × 100;
- crescimento MoM;
- crescimento YoY;
- crescimento YoY SPOT;
- crescimento YoY EVENTO;
- natureza dominante;
- retorno previsto derivável.

`EVENTO` não é automaticamente promovido a `SAZONALIDADE`. Sazonalidade é medida pelo comportamento relativo do mês ao histórico; EVENTO permanece natureza observada da fonte.

## Política de estoque

Base estatística: anos completos 2021–2025, por mesmo mês-calendário.

- **Estoque mínimo SPOT** = teto do P75 da demanda SPOT.
- **Estoque de segurança SPOT** = teto(P90) − teto(P75).
- **Estoque alvo SPOT** = teto do P90.
- **Reserva EVENTO de referência** = teto do P75 histórico de EVENTO.
- **Proteção comercial de referência** = estoque alvo SPOT + reserva EVENTO.
- Venda permanece exposta separadamente como pressão de reposição; não é misturada automaticamente ao estoque de locação.

A reserva P90−P75 é uma proteção empírica. Ela deverá evoluir para método por nível de serviço/lead time quando esses parâmetros forem comprovados.

## Previsão-base

Horizonte inicial: outubro/2026 a setembro/2027.

Por componente SPOT/EVENTO/VENDA:

1. se existir base no mesmo mês do ano anterior e ao menos duas taxas YoY válidas, usar mediana das últimas três variações YoY;
2. caso contrário, com três ou mais anos ativos, usar a mediana histórica do mesmo mês-calendário;
3. sem evidência suficiente, manter `SEM_BASE`.

A previsão-base não substitui `mt_previsoes_demanda`; ela serve como referência analítica até o Comercial inserir uma previsão governada.

## Retornos

`retornos_previstos` usa somente linhas de `LOCAÇÃO` em que:

- `Data Prevista da Saída` é válida;
- `Período` é inteiro positivo;
- `Data Prevista de Retorno = Data Prevista da Saída + Período em meses`.

EVENTO não entra nessa derivação enquanto a unidade de `Período` para eventos não estiver validada.

## GAPs preservados

- a planilha não contém quantidade física explícita por linha;
- o catálogo canônico ainda não contém a família de modelos de contêiner necessária para reconciliar todos os modelos da fonte;
- `mt_tenants`, demanda histórica, previsões e pedidos comerciais ainda não fornecem o estado operacional necessário à reconciliação;
- a cobertura de data prevista de saída/período é incompleta.

Por isso, os agregados carregados nesta etapa usam `REGISTRO_EQUIVALENTE`; a view deixa `saldo_vs_estoque_minimo` e `saldo_vs_protecao_comercial` nulos até existir unidade física reconciliada.

## Cognição ELO

A view nunca afirma uma causa externa sem evidência. Quando houver alta/queda, orienta validar:

- perdas de contrato;
- renovações frágeis ou confirmadas;
- campanhas de novos clientes;
- eventos confirmados/cancelados;
- concorrência;
- preços;
- mudanças de mercado.

Variações relevantes direcionam análise `SWOT + 5W2H`; a decisão operacional permanece governada.