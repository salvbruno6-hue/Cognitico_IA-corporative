# Implementation Readiness — PCP/KPI/MCP

Estado atual: `READY_FOR_CODEX_IMPLEMENTATION`.

A investigação necessária para iniciar código foi concluída. Os gaps remanescentes são concretos e têm arquivos-alvo definidos.

## Arquivos-alvo

- `supabase/migrations/<nova_migration>.sql`
- `elo-virtual-core/integracoes/supabase_elo_forge.py`
- `src/elo/cognitive/runtime/humanization/humanizer.py`
- `supabase/functions/elo-mcp/index.ts`
- testes Forge/cognitivos/MCP correspondentes

## Não alterar por conveniência

- contratos de autoridade existentes;
- Evolution Gate;
- DecisionLifecycle;
- Memory;
- Router;
- mecanismos de learning;
- `main` diretamente.

## Fonte de execução

`docs/prompts/CODEX_ELO_PCP_KPI_E2E_IMPLEMENTATION.md`
