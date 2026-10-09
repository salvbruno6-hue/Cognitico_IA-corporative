# Gate de Execução — Fechamento E2E PCP/KPI/MCP

## Estado

A auditoria e a reconciliação documental foram concluídas na branch `audit/e2e-pcp-kpi-mcp`.

O próximo estágio exige implementação e execução de testes no ambiente de desenvolvimento/Codex porque envolve:

- criação de migration pelo fluxo oficial Supabase CLI;
- alteração coordenada do adapter Forge;
- alteração do Humanizer;
- alteração da Edge Function `elo-mcp`;
- testes Python/TypeScript/integration;
- validação de migration e lint/typecheck.

## Autorização já concedida

Está autorizado:

- continuar a implementação na branch;
- criar/atualizar PR;
- executar testes;
- corrigir gaps comprovados.

Não está autorizado automaticamente:

- merge em `main`;
- alteração direta de `main`;
- promoção de indicador parcial a KPI formal;
- preenchimento inventado de dados operacionais;
- mudança de Vercel nesta etapa.

## Entrada para Codex

Usar `docs/prompts/CODEX_ELO_PCP_KPI_E2E_IMPLEMENTATION.md` como contrato de execução.

## Saída obrigatória do estágio

- migration nova;
- catálogo governado atualizado;
- adapter Forge atualizado;
- Humanizer atualizado;
- tool MCP `elo_pcp_indicadores_status`;
- testes E2E relevantes passando;
- proveniência preservada;
- PR revisável;
- merge pendente de autorização humana explícita.
