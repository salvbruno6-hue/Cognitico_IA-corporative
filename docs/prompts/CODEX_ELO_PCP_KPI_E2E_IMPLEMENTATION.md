# Prompt Codex — Fechamento E2E PCP → Indicadores → KPI → API → MCP

Trabalhe no repositório `salvbruno6-hue/Cognitico_IA-corporative`, na branch `audit/e2e-pcp-kpi-mcp`.

Não altere `main` diretamente e não faça merge.

Antes de editar, leia:

- `docs/audits/ELO_PCP_KPI_MCP_E2E_AUDIT_20261009.md`
- `docs/audits/ELO_PCP_KPI_E2E_STATUS_MATRIX.md`
- `docs/implementation/ELO_PCP_INDICATORS_KPI_E2E_IMPLEMENTATION_CONTRACT.md`
- `docs/MULTITEINER_KPIs_MASTER.md`
- `06-knowledge-engineering/SKILL_PLANEJAMENTO_MULTITEINER.md`
- `05-cognitive-platform/MCP_CANONICAL_MAP.md`
- `supabase/functions/elo-mcp/README.md`

## Objetivo

Fechar somente os gaps E2E comprovados pela auditoria, reutilizando a arquitetura existente:

`Supabase → read-model governado → indicador → evidência → CognitiveResponse → MCP → resposta ELO`.

Não promova indicador a KPI formal enquanto `mt_definicoes_kpi`/`mt_snapshots_kpi` não possuírem definição e evidência válidas.

## Implementação

1. Crie uma nova migration pelo fluxo oficial Supabase CLI (`supabase migration new ...`). Não edite migration histórica.
2. Governe em `elo_aprendizado_fontes`, como read-only e preservando proveniência:
   - `v_elo_pcp_carga_capacidade_periodo`
   - `v_elo_pcp_indicadores_montagem_externa`
3. Atualize `elo-virtual-core/integracoes/supabase_elo_forge.py`:
   - termos de descoberta para capacidade/carga/utilização/indicadores/KPI;
   - inclua somente as duas views read-only no escopo global seguro;
   - retorne capacity/external indicator records sem inventar valores;
   - não calcule ICAC no adapter;
   - mantenha `elo_aprendizado_fontes` como única autoridade de source discovery.
4. Atualize `src/elo/cognitive/runtime/humanization/humanizer.py` para narrar:
   - capacidade/carga/folga/utilização/excesso quando observados;
   - indicadores de montagem externa quando observados;
   - ausência explícita quando os dados não existirem;
   - distinção textual entre indicador observado e KPI formal registrado.
5. Preserve o endpoint canônico `POST /cognitive` e `CognitiveResponse`; não crie API paralela se desnecessário.
6. No `supabase/functions/elo-mcp/index.ts`, implemente tool read-only `elo_pcp_indicadores_status` usando o mesmo `authenticate`, `authorizeRead` e `audit` existentes.
7. A tool deve consultar apenas read-models/tabelas explicitamente necessários e retornar fontes, estado, `read_only=true`, `guessed=false`.
8. O estado do registro KPI deve ser consultado sem transformar ausência em valor zero operacional.
9. Não amplie genericamente `elo_read` para tabelas operacionais brutas.
10. Atualize documentação somente se o runtime final divergir do contrato já registrado.

## Testes obrigatórios

Adicione/ajuste testes para provar:

- source discovery de capacidade;
- source discovery de indicadores externos;
- views não governadas continuam bloqueadas;
- ausência de registros não produz indicador inventado;
- unidade incompatível não produz folga/utilização falsa;
- humanizer inclui indicadores observados quando existem;
- humanizer informa ausência quando não existem;
- não chama indicador de KPI sem definição/snapshot formal;
- evidence refs são preservados;
- consulta sem modelo continua funcionando;
- `tools/list` inclui `elo_pcp_indicadores_status`;
- MCP mantém 401/403 corretos;
- tool é read-only e auditada;
- KPI registry vazio retorna ausência/indeterminação;
- nenhuma autoridade paralela foi criada.

Execute a suíte relevante e reporte comandos/resultados. CI não substitui prova operacional.

## Regras de governança

- sem autoautorização;
- sem escrita operacional via MCP;
- sem aprendizado automático por simples consulta;
- sem nova autoridade de Evidence, Memory, Router, DecisionLifecycle ou Evolution Gate;
- ausência de evidência = `INDETERMINADO`, `PARCIAL` ou `BLOQUEADO_POR_DADOS` conforme o contrato;
- não inferir capacidade, headcount, disponibilidade, demanda ou KPI.

Ao terminar:

1. apresente arquivos alterados;
2. apresente testes executados e resultados;
3. apresente gaps ainda bloqueados por dados;
4. deixe a branch pronta para revisão/PR;
5. não faça merge.
