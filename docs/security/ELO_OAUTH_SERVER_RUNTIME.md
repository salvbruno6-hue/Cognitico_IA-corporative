# ELO OAuth Server Runtime

## Objetivo

Usar o Supabase Auth existente como servidor OAuth 2.1 para clientes MCP/ChatGPT, preservando o Google já configurado como método de autenticação do operador ELO.

## Contrato canônico

- identidade do usuário: Supabase Auth existente;
- login interativo: Google já habilitado no projeto;
- servidor OAuth: Supabase Auth OAuth 2.1;
- consentimento: `/Cognitico_IA-corporative/oauth/consent` no frontend canônico;
- cliente MCP: registro dinâmico habilitado;
- protected resource: `https://fxbpevjrkwhbicpmecow.supabase.co/functions/v1/elo-mcp`;
- autorização de dados/ações: `elo-authz`, nunca apenas presença de token.

## Fail-closed

O discovery OAuth pode ser público. Toda chamada POST do MCP continua exigindo token de usuário válido, identidade ELO ativa e decisão ALLOW de `elo-authz`. Habilitar OAuth Server ou dynamic registration não concede `PCP_UPDATE`, escrita, schema mutation ou bypass de RLS.

## Configuração esperada

```toml
[auth]
site_url = "https://salvbruno6-hue.github.io"

[auth.oauth_server]
enabled = true
authorization_url_path = "/Cognitico_IA-corporative/oauth/consent"
allow_dynamic_registration = true
```

O estado remoto do dashboard deve corresponder a este contrato antes de considerar o login ChatGPT/MCP operacional.
