# ELO MT unit materialization readiness — 2026-10-23

## Objetivo

Governar a reconciliação dos identificadores físicos legados de `mt_ordens_reparo` com `mt_unidades_modulares` e registrar as regras canônicas de modelo/fluxo necessárias para o PCP.

## Regra de identidade confirmada

- `MLTM` identifica uma unidade modular física da Multiteiner;
- os dois primeiros dígitos após `MLTM` identificam o modelo (`01` = M01 Amplo, `02` = M02 Suíte etc.);
- os dígitos restantes identificam individualmente a unidade;
- a sequência individual pode ter comprimento variável.

## Estado live atual

- 133 ordens de reparo;
- 124 identificadores `MLTM...` distintos;
- 133/133 reparos vinculados ao tenant `MULTITEINER`;
- 124/124 unidades físicas materializadas em `mt_unidades_modulares`;
- 133/133 reparos ligados por `unidade_modular_id` à unidade física canônica;
- nenhum identificador permanece bloqueado por ausência de modelo canônico.

## Modelos reconciliados

M14 e M15 foram promovidos com base em evidência legada consistente e sem conflito:

- `MLT.M14` — Módulo Habitacional 20pés Sanitário 7 Vasos;
- `MLT.M15` — Módulo Habitacional 20pés Sanitário 9 Mictórios.

M16 foi confirmado por regra de negócio como:

- conceitualmente equivalente ao M01 em configuração base;
- **não alterável / não customizável**;
- não deve gerar fabricação de `CHASSI` / estrutura metálica;
- demais diferenças de processo não devem ser inferidas sem nova evidência.

O modelo ativo `MLT.M16` permanece com identidade própria e descrição explícita dessa restrição.

## Fluxo produtivo específico M16

Foi criado o fluxo:

`MLT.PROD.M16.NAO_CUSTOMIZAVEL.V1`

Ele deriva de `MLT.PROD.PADRAO.V2`, preserva as etapas ativas conhecidas e **exclui somente `CHASSI`**, conforme a regra confirmada. A exclusão de qualquer outra etapa exige evidência adicional.

Esse contrato impede que o PCP contabilize M16 como demanda de fabricação de chassi/estrutura metálica.

## Estado conservador

Nenhuma origem operacional histórica foi inventada. As unidades continuam fail-closed quando não há evidência de estado real:

- `disponivel_montagem = false`;
- `disponivel_expedicao = false`;
- OP, pedido e localização permanecem nulos quando não comprovados.

## Proveniência

A reconciliação de identidade física não fabrica linhagem histórica. O GAP de proveniência linha a linha permanece separado da identidade e do roteamento produtivo.

## Status

`IDENTIDADE_FISICA_RECONCILIADA / MODELOS_RECONCILIADOS / M16_NAO_CUSTOMIZAVEL_SEM_CHASSI`
