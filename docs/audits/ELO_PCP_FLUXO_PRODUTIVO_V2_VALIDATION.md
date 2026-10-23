# ELO PCP — Validação do fluxo produtivo modular v2

## Objeto afetado

`public.fluxo_produtivo_modular` e `public.fluxo_produtivo_modular_etapas`.

## Estado anterior

- fluxo `MLT.PROD.PADRAO` v1.0 ativo;
- 17 etapas ativas;
- sequência ainda continha `TRILHO` e `PINTURA_MODULAR`;
- não continha `CORTE_DOBRA` nem `ESQUADRIAS`.

## Evidência

Contrato operacional confirmado pelo usuário em 2026-10-23 e confrontado com o estado vivo do Supabase.

## Alteração

Versionamento preservativo:

- v1.0 mantida como histórica e inativa;
- v2.0 criada como referência ativa;
- etapas v1 mantidas como inativas;
- 17 etapas v2 registradas na sequência atual.

## Testes executados

1. Verificação de unicidade de `fluxo_produtivo_modular.codigo`.
2. Verificação de FK `fluxo_produtivo_modular_etapas.fluxo_id -> fluxo_produtivo_modular.id`.
3. Verificação de ausência de FKs externas ao fluxo além das próprias etapas.
4. Validação pós-migração:
   - v1: `ativo=false`, 0 etapas ativas, 17 inativas;
   - v2: `ativo=true`, 17 etapas ativas, 0 inativas;
   - `v_elo_pcp_requisito_fisico_planejamento.etapas_fluxo_referencia = 17`;
   - readiness não duplicado.

## Resultado

`VALIDADO_TECNICAMENTE` para versionamento do fluxo.

## Risco residual

- tempos por etapa não validados;
- capacidades por etapa não validadas;
- dependências detalhadas não persistidas;
- critérios de qualidade específicos não persistidos;
- eventos reais de cura/liberação/EL ainda ausentes;
- requisito M01 permanece bloqueado por `GAP_TENANT` e gaps subsequentes de roteiro/tempo/capacidade.

## Evolution Gate

A alteração preserva as autoridades existentes, evita sobrescrita histórica, não cria schema paralelo e não promove capacidade não comprovada. Elegível para integração em `main` após checks do PR.
