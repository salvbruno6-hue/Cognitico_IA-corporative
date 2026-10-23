# ELO MT models M14/M15 validation — 2026-10-23

## Escopo

Resolver somente os gaps de modelo M14 e M15 usando evidência operacional já persistida em `mt_ordens_reparo`.

## Evidência M14

- 24 reparos / 21 unidades distintas;
- 22 linhas com `tipo_modulo` preenchido;
- exatamente 1 nome não nulo distinto: `Módulo Habitacional 20pés Sanitário 7 Vasos`;
- 0 nomes conflitantes.

Resultado: modelo ativo `MLT.M14` criado e 21 unidades físicas materializadas.

## Evidência M15

- 5 reparos / 5 unidades distintas;
- 3 linhas com `tipo_modulo` preenchido;
- exatamente 1 nome não nulo distinto: `Módulo Habitacional 20pés Sanitário 9 Mictórios`;
- 0 nomes conflitantes.

Resultado: modelo ativo `MLT.M15` criado e 5 unidades físicas materializadas.

## Resultado operacional

Após a reconciliação:

- 123 unidades Multiteiner em `mt_unidades_modulares`;
- 132/133 reparos ligados a unidade física;
- 133/133 reparos ligados ao tenant `MULTITEINER`;
- apenas M16 permanece sem modelo/unidade canônica.

## M16

`MLTM 160082` não possui `tipo_modulo`; a única observação disponível é `Status fonte: Pátio de ok`. Isso não comprova nome ou configuração do modelo. M16 permanece fail-closed.

## Não ações

Não foram inferidos:

- BOM;
- tempos padrão;
- capacidade;
- custo;
- dimensão;
- ordem de produção;
- pedido de venda;
- localização;
- disponibilidade de montagem ou expedição;
- proveniência histórica.

## Status

`VALIDADO_PARCIAL / M14_M15_RESOLVIDOS / M16_PENDENTE`
