# Auditoria E2E — PCP, Indicadores, KPI, API e MCP

Data: 2026-10-09  
Branch: `audit/e2e-pcp-kpi-mcp`  
Escopo: somente leitura da arquitetura operacional e documentação, com correções documentais isoladas nesta branch.

## 1. Objetivo

Comprovar a cadeia:

`dado Supabase → relacionamento → read-model → indicador → KPI → interpretação → evidência/proveniência → API → MCP → resposta ELO`

E a rastreabilidade inversa:

`resposta ELO → interpretação/decisão → KPI/indicador → cálculo → view/função → tabela/campo → evidência`.

Ausência de evidência não autoriza inferência operacional. Estados válidos da auditoria: `COMPROVADO`, `PARCIAL`, `NÃO_COMPROVADO`, `BLOQUEADO_POR_DADOS`, `SUPERADO`.

## 2. Achados principais

### 2.1 Documentação MCP estava divergente do runtime

`05-cognitive-platform/MCP_CANONICAL_MAP.md` e `supabase/functions/elo-mcp/README.md` documentavam uma superfície menor que a realmente presente em `supabase/functions/elo-mcp/index.ts`.

O runtime atual expõe:

- `elo_status`
- `elo_read`
- `elo_pcp_demanda_crossing_status`
- `elo_pcp_comunicacao_melhoria`
- `elo_pcp_orquestrador_dialogo`
- `elo_pcp_dados_pendentes`
- `elo_pcp_decisao_externa_status`
- `elo_dol_read`
- `elo_calibration_read`
- `elo_precedent_search`

Correção documental aplicada nesta branch. Nenhuma autoridade do MCP foi ampliada.

### 2.2 Indicadores/read-models PCP existem

Foram comprovadas no Supabase, entre outras:

- `v_elo_pcp_carga_capacidade_periodo`
- `v_elo_pcp_cobertura_demanda_externa`
- `v_elo_pcp_decisao_externa_detalhe`
- `v_elo_pcp_decisao_externa_resumo`
- `v_elo_pcp_dados_pendentes`
- `v_elo_pcp_dialogo_regras`
- `v_elo_pcp_capacidade_rh_montagem`
- `v_elo_pcp_indicadores_montagem_externa`
- `v_elo_pcp_montagem_externa_integrada`

Esses read-models já conectam demanda, estoque, reparo, produção programada, operação externa, demanda humana, cobertura, gaps e próximas informações necessárias.

### 2.3 Registro operacional de KPI existe, mas está vazio

Estruturas existentes:

`mt_definicoes_kpi`

- `id`
- `codigo_kpi`
- `nome`
- `dominio`
- `unidade`
- `formula`
- `ativo`

`mt_snapshots_kpi`

- `id`
- `kpi_id`
- `data_referencia`
- `valor`
- `numerador`
- `denominador`
- `contexto`
- `calculado_em`

FK comprovada:

`mt_snapshots_kpi.kpi_id → mt_definicoes_kpi.id`

Estado observado em 2026-10-09:

- `mt_definicoes_kpi`: 0 registros
- `mt_snapshots_kpi`: 0 registros

Portanto, a arquitetura de armazenamento de KPI existe, porém a camada operacional de definição/snapshot ainda está `BLOQUEADO_POR_DADOS`/não materializada.

### 2.4 Arquitetura mestre de KPI existe em Markdown

`docs/MULTITEINER_KPIs_MASTER.md` define a cadeia corporativa:

`Demanda → Capacidade → Atendimento → Execução → Entrega → Ativo → Resultado → Aprendizado`

Inclui, entre outros:

- ICAC;
- capacidade comercial disponível;
- produção para estoque;
- recuperação por reparo;
- taxa de recuperação;
- disponibilidade comercial;
- lead time de recuperação;
- gap comercial;
- gargalo operacional;
- espera/aguardando;
- retrabalho;
- FPY;
- prontidão de expedição;
- OTD;
- compras/OTIF;
- acuracidade de estoque;
- excedentes;
- aprovação G2;
- previsão de demanda/MAPE.

O documento é arquitetura semântica; não é, por si só, prova de execução dos KPIs.

## 3. Matriz E2E atual

| Conceito | Markdown | Tabela/campo | Read-model/cálculo | API | MCP | Estado | Gap |
|---|---|---|---|---|---|---|---|
| Demanda comercial | comprovado | `mt_pedidos_venda*` | `v_elo_pcp_demanda_comercial` | parcial | `elo_pcp_decisao_externa_status` | PARCIAL | dados operacionais vazios |
| Histórico/previsão | comprovado | `mt_demanda_historico`, `mt_previsoes_demanda` | `v_elo_pcp_referencia_demanda_comparavel` | parcial | PCP tools | BLOQUEADO_POR_DADOS | tabelas sem registros |
| Cobertura | comprovado | estoque/unidades/reparo/OP | `v_elo_pcp_cobertura_demanda_externa` | parcial | cockpit PCP | PARCIAL | reparos sem genealogia e fontes vazias |
| Capacidade fabril | comprovado | `mt_capacidade_diaria`, `mt_operacoes_roteiro`, `mt_linhas_plano_pcp` | `v_elo_pcp_carga_capacidade_periodo` | não comprovado E2E | não específico | BLOQUEADO_POR_DADOS | estruturas operacionais vazias |
| Operação externa | comprovado | `mt_ordens_montagem_externa`, equipe/função | views de montagem externa | parcial | cockpit PCP | BLOQUEADO_POR_DADOS | tabelas operacionais vazias |
| Reparo | comprovado | `mt_ordens_reparo` | cobertura PCP | parcial | cockpit PCP | PARCIAL | ordens sem `unidade_modular_id` |
| Indicadores montagem externa | parcial | tabelas externas | `v_elo_pcp_indicadores_montagem_externa` | não comprovado E2E | não específico | PARCIAL | falta exposição/contrato explícito |
| KPI corporativo | `MULTITEINER_KPIs_MASTER.md` | `mt_definicoes_kpi`, `mt_snapshots_kpi` | não há catálogo materializado comprovado | não comprovado | não comprovado | NÃO_COMPROVADO | 0 definições e 0 snapshots |
| Proveniência API | contrato comprovado | `Provenance.evidence_refs` | `CognitiveResponse` | comprovado estruturalmente | parcial | PARCIAL | falta prova por KPI/indicador |
| MCP PCP | documentação corrigida | read-models governados | tools PCP | n/a | runtime comprovado | COMPROVADO para leitura PCP existente | não cobre catálogo KPI completo |

## 4. Relações comprovadas relevantes

### Capacidade fabril

`mt_linhas_plano_pcp.modelo_id`
→ `mt_operacoes_roteiro.modelo_id`
→ `mt_operacoes_roteiro.centro_trabalho_id`
→ `mt_capacidade_diaria.centro_trabalho_id`
→ `v_elo_pcp_carga_capacidade_periodo`
→ `carga_horas_planejada / capacidade_disponivel / folga_horas / utilizacao_pct / excesso_carga`

A view calcula métricas de horas somente quando `unidade_capacidade` é compatível com hora; caso contrário preserva `NULL`, evitando conversão inventada.

### Cobertura de demanda

`mt_previsoes_demanda`
+
`mt_unidades_modulares`
+
`mt_ordens_reparo`
+
`mt_ordens_producao`
→ `v_elo_pcp_cobertura_demanda_externa`
→ cobertura/necessidade adicional/estado de gap.

### Decisão externa governada

`v_elo_pcp_demanda_comercial`
+
`v_elo_pcp_referencia_demanda_comparavel`
+
`v_elo_pcp_demanda_humana_historica_externa`
+
`v_elo_pcp_demanda_humana_projetada_externa`
+
`v_elo_pcp_cobertura_demanda_externa`
→ `v_elo_pcp_decisao_externa_detalhe`
→ `v_elo_pcp_decisao_externa_resumo`
→ `v_elo_pcp_dados_pendentes`
→ tools PCP do ELO-MCP.

## 5. API cognitiva

`src/elo/interface/contracts.py` possui `CognitiveResponse` canônico com:

- `request_id`;
- `correlation_id`;
- `tenant_id`;
- `response`;
- `sources`;
- `confidence`;
- `provenance`;
- `suggestions`.

`Provenance` possui `evidence_refs`, `policy_decision`, `validation_status` e `metadata`.

Conclusão: existe espaço contratual para transportar rastreabilidade. Ainda é necessário provar que cada resultado PCP/KPI usa esses campos ponta a ponta.

## 6. Gaps reais remanescentes

1. Mapear cada KPI de `MULTITEINER_KPIs_MASTER.md` para fonte, fórmula executável, unidade, janela temporal e read-model.
2. Diferenciar `indicador disponível em view` de `KPI corporativo governado`.
3. Definir/popular `mt_definicoes_kpi` sem duplicar semântica já existente.
4. Definir política de geração de `mt_snapshots_kpi` somente com evidência suficiente.
5. Comprovar transporte de proveniência do indicador/KPI pela API cognitiva.
6. Expor via MCP apenas KPIs/read-models governados; não ampliar `elo_read` indiscriminadamente.
7. Criar testes diretos e reversos de rastreabilidade.
8. Não classificar dados simulados como prova operacional.

## 7. Critério de fechamento

A auditoria só será considerada E2E concluída quando existir teste demonstrando:

`registro → tabela → view/cálculo → indicador → definição KPI → snapshot → CognitiveResponse/proveniência → MCP → resposta ELO`

E o caminho inverso até os registros/evidências de origem.

## 8. Regra de implementação

Não criar nova autoridade para KPI, evidência, decisão, memória ou aprendizagem. Reutilizar:

- `mt_definicoes_kpi` / `mt_snapshots_kpi` para persistência operacional de KPI quando aplicável;
- read-models `v_elo_*` para derivação;
- `CognitiveResponse` / `Provenance` para transporte;
- ELO-MCP como boundary `READ`;
- gates e governança canônicos existentes.
