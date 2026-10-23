# ELO PCP — capacidade por rota do modelo M16 — 2026-10-23

## Regra de negócio confirmada

O modelo M16 é uma variante fixa do conceito M01:

- configuração base equivalente ao M01;
- não alterável / não customizável;
- não gera fabricação de CHASSI / estrutura metálica;
- continua sujeito às demais etapas do fluxo enquanto não houver evidência específica em contrário.

## Autoridade do fluxo

A autoridade de rota permanece em `fluxo_produtivo_modular` e `fluxo_produtivo_modular_etapas`.

O fluxo específico já existente do M16 é:

`MLT.PROD.M16.NAO_CUSTOMIZAVEL.V1`

Ele possui 16 etapas ativas e não contém `CHASSI`.

O fluxo padrão `MLT.PROD.PADRAO.V2` possui 17 etapas e contém `CHASSI`.

## Nova leitura governada

A view `v_elo_pcp_modelo_etapa_aplicavel` resolve, para cada modelo ativo:

1. fluxo específico, quando existir;
2. caso contrário, fluxo padrão V2;
3. somente etapas ativas do fluxo resolvido.

A view é `security_invoker=true` e não cria nova autoridade de fluxo.

Validação live:

- M01 → `MLT.PROD.PADRAO.V2` → 17 etapas → CHASSI = 1;
- M16 → `MLT.PROD.M16.NAO_CUSTOMIZAVEL.V1` → 16 etapas → CHASSI = 0.

## Normalização cognitiva do mix

`pcp_route_demand.route_mix_demand_by_constraint` recebe demanda por modelo e o mapa governado de etapas aplicáveis e produz demanda por restrição.

Exemplo:

- demanda M01 = 10;
- demanda M16 = 5;
- CHASSI aplicável apenas ao M01;
- MONTAGEM aplicável a ambos.

Resultado esperado:

- demanda CHASSI = 10;
- demanda MONTAGEM = 15.

Se um modelo demandado não tiver rota governada fornecida, o cálculo falha fechado em vez de assumir o fluxo padrão.

## Limite deliberado

Esta mudança corrige o consumo de **capacidade de CHASSI** pelo mix. Ela não remove automaticamente itens de estrutura metálica de uma BOM/MRP, porque isso exige classificação explícita dos componentes estruturais e sua origem (fabricação nova versus estrutura existente). Nenhuma baixa ou compra é inferida sem esse contrato.

Status: `M16_ROUTE_AWARE_CAPACITY_VALIDATED`.
