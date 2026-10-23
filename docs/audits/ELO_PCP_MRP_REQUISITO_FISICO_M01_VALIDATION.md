# ELO PCP — Validação do MRP bruto para requisito físico M01

## Objeto afetado

`public.v_elo_pcp_mrp_requisito_fisico_m01`.

## Estado anterior

A referência `vw_pcp_bom_almox_pedido_compras_m01_120` estava vinculada a 120 módulos e não existia read-model que ligasse o requisito físico persistido de M01 ao consumo unitário existente.

## Evidência

- requisito físico vivo: 300 M01 restantes, prazo 31/01/2027;
- read-model M01/120: 37 linhas com consumo unitário localizado em quatro processos;
- 6 linhas sem `cod_produt`, já tratadas como GAP na fonte;
- `mt_lotes_estoque`, reservas e pedidos operacionais necessários ao MRP líquido permanecem sem evidência suficiente.

## Alteração

Criada view derivada, `security_invoker=true`, que reutiliza os consumos unitários do read-model existente e recalcula somente:

`necessidade_bruta_requisito = consumo_unitario × quantidade_restante`.

A view não calcula necessidade líquida e não autoriza compra.

## Testes

- 37 linhas retornadas;
- 37/37 com necessidade bruta calculável;
- 37/37 permanecem fail-closed em `BLOQUEADO_GAP_TENANT_E_ESTOQUE`;
- 6 itens preservados como `GAP_COD_PRODUTO`;
- `security_invoker=true` confirmado;
- `anon` e `authenticated` não possuem SELECT direto na nova view;
- PIR40: 14 × 300 = 4.200 un;
- PIR32: 5 × 300 = 1.500 un;
- manta de fibra: 20,69 × 300 = 6.207 kg;
- resina: 45,517 × 300 = 13.655,1 kg.

## Cadastro mestre / aliases

Os GAPs foram confrontados com a Lista Mãe. Cinco itens possuem correspondência canônica por `cod_item`, porém continuam sem `cod_produt`; nenhum código novo foi inventado. Para `PORTA SALOMÃO 800X2100MM` não existe correspondência textual canônica comprovada; itens semelhantes não foram mapeados por aproximação.

## Resultado

`VALIDADO_TECNICAMENTE / MRP_BRUTO_PARCIAL`.

## Risco residual

- cobertura atual restrita a `ESTRUTURA_METALICA`, `MONTAGEM_M01`, `PISO_VINILICO` e `TELHA_FIBRA`;
- elétrica e demais processos ainda precisam ser integrados por reuso de fontes vigentes;
- tenant, estoque utilizável, reservas, saldo técnico, pedidos abertos e lead time ainda bloqueiam o MRP líquido;
- valores calculados são necessidade bruta, não quantidade a comprar.
