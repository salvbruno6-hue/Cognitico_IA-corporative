# Deploy de Edge Functions

Este documento descreve o processo oficial de deploy das
Edge Functions do ELO.

A decisão arquitetural está em:
`10-adr/ADR-0019-edge-functions-deploy.md`

## Visão geral

O ELO possui três Edge Functions em produção no Supabase:

| Função | Propósito |
|---|---|
| `elo-data-gateway` | Gateway de dados (read + lista_mae_insert) |
| `elo-authz` | Autorização (capabilities, scopes) |
| `elo-mcp` | Servidor MCP (tools cognitivas) |

Todas vivem em `supabase/functions/<nome>/` no GitHub.

## Fonte canônica

O código-fonte vive exclusivamente em `main` no GitHub.

Nenhum deploy pode partir de código que não esteja em `main`.

## Método oficial

O deploy é feito via GitHub Actions, usando a CLI do
Supabase com a flag `--use-api` (que dispensa Docker
local).

## Workflow

O workflow oficial é:

`.github/workflows/elo-deploy-functions.yml`

### Como disparar

1. Abra:
   `https://github.com/salvbruno6-hue/Cognitico_IA-corporative/actions/workflows/elo-deploy-functions.yml`

2. Clique em **Run workflow** (botão à direita)

3. Escolha a função:
   - `elo-data-gateway`
   - `elo-authz`
   - `elo-mcp`
   - `all` (deploya as três)

4. No campo **confirm**, digite exatamente:
   `DEPLOY`

5. Clique em **Run workflow**

### O que acontece

- GitHub Actions roda em runner Ubuntu
- Instala Supabase CLI via `supabase/setup-cli`
- Executa `supabase functions deploy <nome> --use-api`
- Reporta o resultado no sumário do run

## Secret obrigatório

O workflow requer o secret `SUPABASE_ACCESS_TOKEN`.

### Como criar

1. Abra:
   `https://supabase.com/dashboard/account/tokens`

2. Clique em **Generate new token**

3. Nome sugerido: `ELO GitHub Deploy`

4. Copie o token (aparece só uma vez)

### Como adicionar ao GitHub

1. Abra:
   `https://github.com/salvbruno6-hue/Cognitico_IA-corporative/settings/secrets/actions`

2. Clique em **New repository secret**

3. Nome: `SUPABASE_ACCESS_TOKEN`

4. Valor: cole o token

5. Clique em **Add secret**

## Rastreabilidade

Cada deploy registra:

- commit SHA em main (`github.sha`)
- operador (`github.actor`)
- função alvo
- run ID
- timestamp

Essas informações estão no log do workflow e no sumário
do run.

## Exceções

Deploys manuais via Dashboard Supabase só podem ocorrer
em emergência declarada, e devem ser seguidos de:

- registro em issue de governança
- sincronização do commit correspondente em main
- PR reconciliando o estado

## Rollback

Se um deploy causar problema:

1. Reverta o commit correspondente em main (PR)
2. Aguarde o CI verde
3. Rode o workflow novamente para deployar a versão
   anterior

O Supabase mantém versões anteriores da função, mas o
caminho canônico é via `main`.

## Referências

- `10-adr/ADR-0019-edge-functions-deploy.md`
- `10-adr/ADR-0018-multi-tenant-model.md`
- `AGENTS.md`