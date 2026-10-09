# ELO MCP

Remote MCP boundary for ELO.

Authentication: Supabase Auth OAuth 2.1 / Bearer JWT.
Authorization: `elo-authz` plus an active identity in `elo_identity_registry`.
Operations: read-only.

Protected Resource Metadata is exposed under `/oauth-protected-resource` for MCP OAuth discovery.

---

## Contrato de Autoridade

A autoridade de qualquer IA externa que acesse este MCP é definida em:

- [`09-governance/contracts/policies/ELO_EXTERNAL_AI_AUTHORITY_CONTRACT.md`](../../../09-governance/contracts/policies/ELO_EXTERNAL_AI_AUTHORITY_CONTRACT.md)
- [`10-adr/ADR-0013-external-ai-authority-contract.md`](../../../10-adr/ADR-0013-external-ai-authority-contract.md)

Tiers: `READ`, `ANALYZE`, `PROPOSE`, `OPERATE`.
Este MCP opera no tier `READ` e não recebe autoridade canônica para escrita, mutação de regras, decisões, aprendizagem ou schema.

---

## Mapa canônico

O ELO possui três superfícies MCP documentadas em:

- [`05-cognitive-platform/MCP_CANONICAL_MAP.md`](../../../05-cognitive-platform/MCP_CANONICAL_MAP.md)

Este é o MCP canônico de leitura empresarial. HERMES-MCP (`ANALYZE`) e SYMBIONT-MCP (`PROPOSE`) mantêm papéis separados.

---

## Tools expostas pelo runtime

A lista normativa deve acompanhar `TOOLS` em `index.ts`.

| Tool | Finalidade | Fonte / boundary |
|---|---|---|
| `elo_status` | Estado autenticado do operador e do boundary | `elo-authz`, `elo_identity_registry` |
| `elo_read` | Leitura de tabelas explicitamente allowlisted | allowlist em `index.ts` |
| `elo_pcp_demanda_crossing_status` | Estado governado do cruzamento de demanda PCP | read-models PCP governados |
| `elo_pcp_comunicacao_melhoria` | Comunicação dos gaps e pontos de melhoria sem mutação canônica | `v_elo_pcp_comunicacao_melhoria` / gaps governados |
| `elo_pcp_orquestrador_dialogo` | Diálogo controlado de coleta/validação de dados faltantes | regras e sessões do diálogo PCP |
| `elo_pcp_dados_pendentes` | Solicitações canônicas de dados faltantes | `v_elo_pcp_dados_pendentes` |
| `elo_pcp_decisao_externa_status` | Cockpit read-only de decisão/impacto PCP | `v_elo_pcp_decisao_externa_resumo` e detalhe relacionado |
| `elo_dol_read` | Leitura do Decision Outcome Loop | projeção DOL |
| `elo_calibration_read` | Leitura de calibração/confiança | projeção de calibração |
| `elo_precedent_search` | Busca de precedentes de decisão | índice de precedentes |

Todas as tools passam pelo mesmo caminho de autenticação/autorização e são auditadas em `elo_audit_log`. Nenhuma tool deste boundary autoriza escrita operacional.

---

## Limite atual de cobertura PCP/KPI

O runtime já expõe leitura governada de demanda, cobertura, gaps e decisão externa. Isso não significa que toda a arquitetura corporativa de KPIs esteja materializada no MCP.

Em particular:

- `docs/MULTITEINER_KPIs_MASTER.md` define KPIs corporativos, inclusive ICAC, disponibilidade, fabricação, reparo, gargalos, qualidade, expedição e outros;
- `mt_definicoes_kpi` e `mt_snapshots_kpi` existem como estruturas operacionais, mas sua população e vínculo E2E precisam ser comprovados antes de declarar KPI executável;
- views como `v_elo_pcp_carga_capacidade_periodo`, `v_elo_pcp_indicadores_montagem_externa`, `v_elo_pcp_cobertura_demanda_externa` e `v_elo_pcp_decisao_externa_resumo` produzem indicadores/read-models específicos;
- o MCP não deve converter um indicador existente em KPI corporativo sem fórmula, unidade, janela, baseline/target quando aplicável e proveniência comprovadas.

A regra é fail-closed: na ausência de evidência suficiente, retornar gap/estado de indeterminação em vez de inferir valor operacional.

---

## Referências

- `supabase/functions/elo-mcp/index.ts`
- `05-cognitive-platform/MCP_CANONICAL_MAP.md`
- `docs/MULTITEINER_KPIs_MASTER.md`
- `06-knowledge-engineering/SKILL_PLANEJAMENTO_MULTITEINER.md`
- `10-adr/ADR-0014-cognitive-runtime-loop.md`
