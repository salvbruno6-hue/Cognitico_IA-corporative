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

## Current implementation

- Shared ELO shell with sector navigation.
- Existing ELO/Supabase authentication boundary.
- Configurações for dark mode, sound and connector preferences.
- Mission input and sector actions routed to the ELO Cognitive API through the Next.js server boundary.
- Evidence/provenance surface for cognitive responses.
- Static KPI values removed where no governed telemetry exists.
- No browser exposure of Hermes/Supabase infrastructure secrets.

## Vercel project settings

Use this repository with the Vercel project root set to:

`apps/elo-web`

Framework: **Next.js** (auto-detected).

Build command: default (`next build`).

Install command: default package-manager detection.

Required server-side environment variable:

`ELO_COGNITIVE_API_URL=https://<governed-elo-cognitive-endpoint>`

Optional public tenant identifier:

`NEXT_PUBLIC_ELO_TENANT_ID=multiteiner`

Public Supabase values remain limited to the existing authentication/session boundary. Hermes credentials must remain server-side and are not accepted by the browser.

Vercel Preview deployments should be used for every feature branch before production merge.

## Hermes integration rule

The Web layer must never call Hermes directly. The supported path is:

`GPT → ELO Cognitive → Simbionte Contract → Hermes → Evidence → Governed Learning → Evolution Gate`

The canonical Hermes contract explicitly keeps Hermes as an execution/orchestration provider and prevents it from becoming ELO Core, Memory, Router, authority, or Evolution Gate.
