# Findings — PCP / KPI / MCP E2E

1. O runtime ELO-MCP já possuía tools PCP que não estavam refletidas na documentação canônica. A documentação foi reconciliada nesta branch.
2. O Supabase já possui read-models para cobertura, decisão, capacidade e indicadores de montagem externa.
3. `v_elo_pcp_carga_capacidade_periodo` e `v_elo_pcp_indicadores_montagem_externa` ainda não estavam governadas em `elo_aprendizado_fontes` no levantamento atual.
4. `mt_definicoes_kpi` e `mt_snapshots_kpi` existem, possuem relação FK, mas estavam vazias no levantamento atual.
5. O contrato `CognitiveResponse` já suporta proveniência/evidence refs; não há necessidade comprovada de criar uma API paralela.
6. O Forge cross-domain e o Humanizer ainda não consomem os read-models de capacidade/indicadores externos no caminho conversacional atual.
7. O fechamento E2E restante exige migration + adapter + humanizer + MCP tool + testes.
8. ICAC e demais KPIs do master Markdown continuam sem promoção automática: definição semântica não equivale a execução operacional.
