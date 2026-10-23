# ELO PCP — BOM referencial M16 — 2026-10-23

## Regra de negócio

O M16 foi confirmado como equivalente ao M01 em configuração base, porém não alterável / não customizável e sem fabricação de CHASSI / estrutura metálica.

## Decisão de modelagem

A BOM referencial do M16 reutiliza evidência já existente do M01 apenas para componentes não estruturais e elétrica.

Fonte principal:
- `vw_pcp_bom_almox_pedido_compras_m01_120`

Exclusão obrigatória:
- `processo = ESTRUTURA_METALICA`

Fonte elétrica:
- `vw_kit_eletrico_m01_completo`

A view criada é:
- `v_elo_pcp_bom_referencia_m16`

Ela usa `security_invoker=true`.

## Estado validado

A view contém 57 linhas aplicáveis:

| Processo | Linhas | Definitivas | Não definitivas |
|---|---:|---:|---:|
| ELETRICA_M01 | 30 | 25 | 5 |
| MONTAGEM_M01 | 19 | 13 | 6 |
| PISO_VINILICO | 3 | 3 | 0 |
| TELHA_FIBRA | 5 | 5 | 0 |
| **Total** | **57** | **46** | **11** |

Linhas `ESTRUTURA_METALICA` no M16: **0**.

Os gaps de cadastro, dúvidas e conflitos da fonte M01 são preservados. A herança não transforma evidência parcial em evidência definitiva.

## Governança

Esta é uma BOM **unitária de referência**. Ela não:
- cria demanda M16;
- gera ordem de produção;
- reserva estoque;
- calcula necessidade líquida;
- emite necessidade de compra;
- afirma de onde vem a estrutura física/chassi usado pelo M16.

A origem física do chassi/estrutura do M16 permanece separada da regra de que ele não é fabricado na etapa CHASSI.

Status: `M16_REFERENCE_BOM_NON_STRUCTURAL_VALIDATED`.
