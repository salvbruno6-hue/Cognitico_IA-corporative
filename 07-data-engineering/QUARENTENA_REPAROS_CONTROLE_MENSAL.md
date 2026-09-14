# ELO — Controle Mensal de Reparos na Quarentena de Containers

**Status:** PROPOSTA GOVERNADA — aguardando validação do schema Supabase antes de migration

## 1. Finalidade

Controlar o fluxo de containers que entram em quarentena para inspeção/reparo e gerar indicadores mensais de entrada, conclusão e backlog.

Fluxo operacional:

`RETORNO → INSPEÇÃO → AVARIA → REPARO → ESTOQUE`

A contagem mensal deve ser derivada das datas transacionais, sem armazenar manualmente mês/ano.

## 2. Evidência histórica — agosto/2026

Fonte: `RL - PO - 13 - CONTROLE DE MANUTENÇÃO DE CONTAINERS - Preenchida.xlsx`.

Registros com início de reparo em agosto/2026:

| Container | Tipo | Data início reparo |
|---|---|---|
| MLTM 020201 | Módulo Habitacional 20 pés — Escritório Suíte | 21/08/2026 |
| MLTM 020183 | Módulo Habitacional 20 pés — Escritório Suíte | 24/08/2026 |
| MLTM 020202 | Módulo Habitacional 20 pés — Escritório Suíte | 24/08/2026 |
| MLTM 020203 | Módulo Habitacional 20 pés — Escritório Suíte | 24/08/2026 |
| MLTM 020214 | Módulo Habitacional 20 pés — Escritório Suíte | 24/08/2026 |
| MLTM 140234 | Módulo Habitacional 20 pés — Sanitário 7 Vasos | 26/08/2026 |
| MLTM 140224 | Módulo Habitacional 20 pés — Sanitário 7 Vasos | 26/08/2026 |
| MLTM 140210 | Módulo Habitacional 20 pés — Sanitário 7 Vasos | 26/08/2026 |

**Total de entradas em reparo em agosto/2026: 8.**

Distribuição:
- Escritório Suíte: 5
- Sanitário 7 Vasos: 3

Por data:
- 21/08: 1
- 24/08: 4
- 26/08: 3

A evidência disponível não possui data final para esses 8 registros. Portanto, agosto comprova **entrada/início de reparo**, não conclusão/liberação.

## 3. Entidade transacional proposta

Nome de trabalho: `quarentena_reparos`.

Campos mínimos:

- `id`
- `container_id`
- `tipo_container`
- `data_entrada_quarentena`
- `data_inicio_reparo`
- `data_fim_reparo`
- `status_reparo`
- `motivo_entrada`
- `origem`
- `observacao`
- `created_at`
- `updated_at`

### Status sugeridos

`AGUARDANDO_INSPECAO`
`AGUARDANDO_REPARO`
`EM_REPARO`
`AGUARDANDO_INSPECAO_FINAL`
`LIBERADO`
`BLOQUEADO`

Os valores finais devem ser compatibilizados com o domínio já existente antes da migration.

## 4. Indicadores mensais

- **Reparos iniciados:** `COUNT(*)` agrupado pelo mês de `data_inicio_reparo`.
- **Reparos concluídos:** `COUNT(*)` agrupado pelo mês de `data_fim_reparo`.
- **Backlog de quarentena:** registros sem conclusão/liberação.
- **Tempo médio de reparo:** média de `data_fim_reparo - data_inicio_reparo` para concluídos.
- **Dimensões:** tipo, motivo, status, período, origem e responsável/unidade quando houver domínio oficial.

## 5. Regra temporal

Não criar `mes_reparo` ou `ano_reparo` como fonte de verdade. O mês deve ser derivado da data transacional correspondente ao KPI.

## 6. Rastreabilidade

Todo histórico importado deve preservar origem do arquivo, data de importação e identificador do registro de origem quando disponível.

## 7. Governança

Antes da criação física no banco:

1. consultar o schema Supabase;
2. verificar entidade equivalente;
3. classificar `REUSE | EXTEND | NEW | DUPLICATE | CONFLICT`;
4. preservar relações e chaves oficiais;
5. criar migration;
6. importar agosto/2026;
7. reconciliar os 8 registros com a planilha;
8. testar indicadores mensais;
9. passar pelo Evolution Gate;
10. integrar somente após validação.

## 8. Critério de aceite inicial

Para agosto/2026:
- entradas iniciadas = **8**;
- Escritório Suíte = **5**;
- Sanitário 7 Vasos = **3**;
- concluídos comprovados = **0**, pois não há data final registrada para os 8 casos históricos analisados.
