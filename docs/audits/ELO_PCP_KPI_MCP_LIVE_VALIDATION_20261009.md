# ELO PCP/KPI/MCP — validação live — 2026-10-09

## Escopo

Validação pós-migration e pós-deploy da cadeia E2E de indicadores PCP/KPI/MCP no projeto Supabase `Elo-forge` (`fxbpevjrkwhbicpmecow`).

## Migration aplicada

Migration registrada no Supabase live:

- `20261009101456_govern_forge_pcp_indicator_kpi_sources`

Fontes governadas em `elo_aprendizado_fontes`:

1. `v_elo_pcp_carga_capacidade_periodo`
2. `v_elo_pcp_indicadores_montagem_externa`
3. `mt_definicoes_kpi`
4. `mt_snapshots_kpi`

Todas foram verificadas com `enabled=true` e `extracao_ativa=true`.

## Estado operacional observado

- `v_elo_pcp_carga_capacidade_periodo`: `0` linhas → `SEM_DADO_OPERACIONAL`.
- `v_elo_pcp_indicadores_montagem_externa`: linha estrutural com atividade zero e `aderencia_horas_pct = null` → `SEM_ATIVIDADE_OPERACIONAL`.
- `mt_definicoes_kpi`: `0` registros → `SEM_KPI_FORMAL_REGISTRADO`.
- `mt_snapshots_kpi`: `0` registros.

Regra preservada: ausência de dado não é convertida em zero operacional e indicador não é promovido automaticamente a KPI.

## ELO-MCP live

Edge Function:

- slug: `elo-mcp`
- status: `ACTIVE`
- versão live validada: `15`
- `verify_jwt=true`
- `import_map=true`

Tools anteriores permanecem declaradas e a nova tool está presente:

- `elo_status`
- `elo_read`
- `elo_pcp_demanda_crossing_status`
- `elo_pcp_comunicacao_melhoria`
- `elo_pcp_orquestrador_dialogo`
- `elo_pcp_dados_pendentes`
- `elo_pcp_decisao_externa_status`
- `elo_pcp_indicadores_status`
- `elo_dol_read`
- `elo_calibration_read`
- `elo_precedent_search`

`elo_pcp_indicadores_status` exige catálogo governado antes da leitura e mantém `automatic_kpi_promotion=false`.

## Segurança / autoridade

- MCP permanece read-only.
- autorização continua delegada a `elo-authz`.
- nenhum KPI foi criado pela migration/deploy.
- nenhuma autoridade paralela foi criada para autorização, learning, lifecycle, memory ou router.
- `mt_definicoes_kpi` permanece a autoridade para classificar um indicador como KPI formal.

## Advisor pós-migration

O advisor não apontou vulnerabilidade específica causada pela migration. Permanecem findings preexistentes, incluindo tabelas com RLS habilitado sem policy e leaked-password protection desabilitada. Esses itens são escopo separado desta implementação.

## Limite da prova live

Foi comprovado no ambiente live:

- migration aplicada e registrada;
- catálogo governado com as quatro fontes;
- estados operacionais das views/tabelas consultados diretamente;
- Edge Function `elo-mcp` ativa na versão 15;
- código live contém a nova tool e mantém as tools anteriores;
- JWT obrigatório e autoridade `elo-authz` preservados.

Ainda não foi executada nesta sessão uma chamada MCP autenticada com bearer de usuário real para `tools/call: elo_pcp_indicadores_status`. Portanto essa etapa permanece como `NÃO COMPROVADO EM CHAMADA AUTENTICADA LIVE`, embora o handler live e seus dados-fonte estejam comprovados e os contratos estejam cobertos por testes de CI.

## Estado para PR #959

A migration e o MCP live foram implantados e verificados. O PR deve permanecer sem merge até a revisão final de CI, rastreabilidade e autorização explícita de merge.
