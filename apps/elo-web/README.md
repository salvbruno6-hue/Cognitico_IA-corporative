# ELO Web

Next.js frontend for the ELO experience layer.

## Boundary

```text
Browser
  -> ELO Web (Vercel / Next.js)
  -> ELO Cognitive API
  -> Simbionte
  -> governed Hermes execution boundary
  -> Hermes runtime
  -> Evidence / Outcome
  -> Governed Learning / Evolution Gate
```

The browser is not an authority for governance, canonical knowledge, infrastructure credentials, or Hermes execution. Hermes remains an external execution runtime; ELO Cognitive owns authorization, routing, provenance and learning governance.

## Current experience implementation

PR #955 prepares the twelve areas from the corporate workspace reference: Orquestrador, Dashboard Comercial, Comercial, Almoxarifado, Compras, Produção, Planejamento/PCP, Expedição, Catálogo, Chat, Notificações and Configurações.

Catalog reads reuse the nine-table `elo-data-gateway` allowlist. Existing `elo-mcp` tools supply PCP gaps, improvement communication, demand crossing, external decision state, own operator status and PCP data collection dialogue. No generic operational table access or new permission authority is added.

Other reference functions are displayed with their identified sources and unresolved integration requirements. General cognitive requests currently use a local echo implementation; the UI does not present responses with no source/evidence reference as an evidenced analysis. Team messaging, operational writes, stock movements, kanban mutations, read receipts, global backup and directory access are not implemented by these screens.

See [workspace reconciliation](../../docs/evolution/ELO_WEB_WORKSPACE_REFERENCE_RECONCILIATION_2026-10-08.md) for the complete requirement/source/GAP/validation mapping. Full production equivalence remains unverified.

## Vercel project settings

Use this repository with the Vercel project root set to:

`apps/elo-web`

Framework: **Next.js** (auto-detected).

Build command: default (`next build`).

Install command: default package-manager detection.

Required server-side environment variable:

O ELO Web não depende de `ELO_COGNITIVE_API_URL`. O endpoint `/api/cognitive` está nesta aplicação; a implementação local comum ainda devolve o texto de entrada sem consultar evidências. Sua existência não comprova execução do Core canônico.

Optional public tenant identifier:

`NEXT_PUBLIC_ELO_TENANT_ID=multiteiner`

Public Supabase values are used for authentication and existing authenticated gateway/MCP calls; they never include a service-role key. Hermes credentials must remain server-side and are not accepted by the browser.

Vercel Preview deployments should be used for every feature branch before production merge.

## Hermes integration rule

The Web layer must never call Hermes directly. The supported path is:

`GPT → ELO Cognitive → Simbionte Contract → Hermes → Evidence → Governed Learning → Evolution Gate`

The canonical Hermes contract explicitly keeps Hermes as an execution/orchestration provider and prevents it from becoming ELO Core, Memory, Router, authority, or Evolution Gate.
