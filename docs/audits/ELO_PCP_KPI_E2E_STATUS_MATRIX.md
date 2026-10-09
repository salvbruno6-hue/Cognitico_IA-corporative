# Matriz de Estado E2E — PCP / Indicadores / KPI / API / MCP

| Elo | Artefato | Estado | Evidência / bloqueio |
|---|---|---|---|
| Demanda comercial | `mt_pedidos_venda*` → `v_elo_pcp_demanda_comercial` | PARCIAL | estrutura/read-model existem; dados operacionais principais vazios |
| Histórico de demanda | `mt_demanda_historico` | BLOQUEADO_POR_DADOS | 0 registros no levantamento atual |
| Previsão de demanda | `mt_previsoes_demanda` | BLOQUEADO_POR_DADOS | sem base suficiente para cobertura operacional |
| Cobertura | `v_elo_pcp_cobertura_demanda_externa` | COMPROVADO_ESTRUTURAL | governada; depende de dados de previsão/unidade/reparo/produção |
| Reparo | `mt_ordens_reparo` | PARCIAL | há ordens, mas genealogia com unidade modular é incompleta |
| Produção planejada | `mt_linhas_plano_pcp`, `mt_ordens_producao` | BLOQUEADO_POR_DADOS | estruturas existentes; carga operacional vazia |
| Carga × capacidade | `v_elo_pcp_carga_capacidade_periodo` | COMPROVADO_ESTRUTURAL | cálculo existe; ainda não governada no catálogo cognitivo |
| Montagem externa | views `v_elo_pcp_*montagem_externa*` | COMPROVADO_ESTRUTURAL | relações/read-models existem; dados operacionais vazios |
| Indicadores externos | `v_elo_pcp_indicadores_montagem_externa` | COMPROVADO_ESTRUTURAL | view existe; ainda não governada no catálogo cognitivo |
| Decisão/gaps | `v_elo_pcp_decisao_externa_*`, `v_elo_pcp_dados_pendentes` | COMPROVADO | governado e consumido pelo MCP atual |
| Catálogo KPI | `mt_definicoes_kpi` | NÃO_MATERIALIZADO | 0 registros |
| Snapshot KPI | `mt_snapshots_kpi` | NÃO_MATERIALIZADO | 0 registros |
| KPI master | `docs/MULTITEINER_KPIs_MASTER.md` | COMPROVADO_SEMÂNTICO | fórmulas/semântica documentadas, não prova runtime |
| Evidence Repository | `EvidenceRepository` + Forge evidence | COMPROVADO | orquestrador salva evidência de fontes consultadas |
| CognitiveResponse | `/cognitive`, `CognitiveResponse`, `Provenance` | COMPROVADO_ESTRUTURAL | contrato possui `evidence_refs`; falta prova completa por KPI |
| ELO-MCP PCP | `supabase/functions/elo-mcp/index.ts` | COMPROVADO_PARCIAL | tools PCP existem; docs corrigidas nesta branch |
| MCP indicadores | `elo_pcp_indicadores_status` | PENDENTE_IMPLEMENTAÇÃO | especificado, ainda não codificado |
| Rastreabilidade direta | dado → resposta | PARCIAL | existe para consulta Forge/PCP; não para KPI formal |
| Rastreabilidade reversa | resposta → registro | PARCIAL | evidence refs existem; não há KPI snapshot formal para fechar cadeia |

## Definição de pronto

Somente considerar a cadeia pronta quando um teste provar:

`registro real → relação → read-model → indicador → definição KPI/snapshot (quando aplicável) → evidence_ref → CognitiveResponse → MCP → resposta ELO`

E a partir da resposta for possível retornar às fontes sem inferir campos ausentes.
