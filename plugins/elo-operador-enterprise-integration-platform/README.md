# ELO Operador — Enterprise Integration Platform

Plugin privado que conecta o ChatGPT ao ELO-MCP existente.

## Escopo do MVP

- leitura autenticada e auditável;
- consulta de dados canônicos permitidos, estado PCP, indicadores, Decision Outcome Loop, calibração e precedentes;
- sem gravação operacional, alteração de schema, promoção de conhecimento ou bypass de gates.

## Fonte de verdade

- ELO Cognitivo: orquestração e decisão;
- GitHub: evidência operacional e ledger de versionamento;
- Supabase/ELO-MCP: memória consultiva e fronteira segura de leitura.

## Autenticação

O servidor usa Supabase Auth OAuth 2.1 e autorização delegada ao `elo-authz`. Após instalar, autentique o MCP `elo_mcp`; o operador precisa de identidade ativa e autorização de leitura no ELO.
