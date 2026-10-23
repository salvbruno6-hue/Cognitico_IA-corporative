# ELO PCP — Handoff de versionamento do fluxo produtivo modular

## Estado

- fluxo histórico preservado: `MLT.PROD.PADRAO` v1.0, `ativo=false`;
- fluxo operacional atual: `MLT.PROD.PADRAO.V2` v2.0, `ativo=true`;
- etapas v1 preservadas como `INATIVO`;
- etapas v2: 17 registros `ATIVO`;
- readiness continua contabilizando 17 etapas, sem duplicação.

## Sequência v2

1. TRIAGEM
2. CORTE_DOBRA
3. CHASSI
4. ESCOVACAO
5. PINTURA_TRATAMENTO
6. ACABAMENTO_BRANCO
7. ESTOQUE_ESTRUTURAS
8. MOVIMENTACAO
9. PISO
10. TETO
11. COLUNAS
12. PAREDES
13. ESQUADRIAS
14. INSTALACOES
15. ACABAMENTOS
16. TESTES
17. LIBERACAO

`TRILHO` e `PINTURA_MODULAR` permanecem somente na v1.0 histórica.

## Governança

- nenhuma tabela/view paralela foi criada;
- tempos e capacidades permanecem `NULL` até evidência operacional validada;
- conclusão da pintura não implica automaticamente entrada no EL;
- cura/qualidade/liberação dependem de evento/evidência real;
- ordem das etapas representa a referência operacional confirmada, mas `dependencias`, `materiais` e `criterios_qualidade` não foram inventados e permanecem vazios até contratos específicos validados.

## Validação no Supabase

- v1.0: 0 etapas ativas / 17 inativas;
- v2.0: 17 etapas ativas / 0 inativas;
- `v_elo_pcp_requisito_fisico_planejamento.etapas_fluxo_referencia = 17`;
- `etapas_com_tempo = 0`;
- `etapas_com_capacidade = 0`;
- requisito M01 permanece `GAP_TENANT`, sem avanço artificial de programação.

## Próximo gap operacional

Depois do versionamento do fluxo, o bloqueio seguinte continua sendo evidência operacional: tenant, roteiro produtivo, tempos, capacidade por etapa, eventos reais de liberação/EL, estoque e ordens de compra.
