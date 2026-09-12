# ELO Web

Next.js frontend for the ELO experience layer and the primary acceptance surface for the current ELO integration program.

## Integrated development focus

ELO Web is the product integration surface. It does not become a new authority; it exercises the existing governed architecture end to end.

```text
Browser
  -> ELO Web (Vercel / Next.js)
  -> ELO Cognitive API
  -> Cognitive / Core governed services
  -> Simbionte
  -> governed Hermes execution boundary
  -> Hermes runtime
  -> Evidence / Outcome
  -> Governed Learning / Evolution Gate
  -> canonical ELO knowledge
```

The browser is not an authority for governance, canonical knowledge, infrastructure credentials, or Hermes execution. Hermes remains an external execution runtime; ELO Cognitive owns authorization, routing, provenance and learning governance.

## Development priority

1. Build/deployment determinism and production Vercel path.
2. Existing authentication/session boundary.
3. ELO Web → ELO Cognitive server boundary.
4. Cognitive-backed workspace and ProcessView integration.
5. Evidence, provenance and CURRENT/DEVIATION/UNKNOWN presentation.
6. Cognitive → Simbionte integration.
7. Governed Simbionte → Hermes execution.
8. Evidence/Outcome → Governed Learning → Evolution Gate.
9. External capabilities through Hermes, including MCP, only after the integrated path is functional.
10. Legacy frontend removal only after production and end-to-end gates pass.

## Current implementation

- Shared ELO shell with sector navigation.
- Existing ELO/Supabase authentication boundary.
- Configurações for dark mode, sound and connector preferences.
- Mission input and sector actions routed to the ELO Cognitive API through the Next.js server boundary.
- Evidence/provenance surface for cognitive responses.
- Static KPI values removed where no governed telemetry exists.
- No browser exposure of Hermes/Supabase infrastructure secrets.

## Integration rule

Every new change must identify its canonical owner, reuse existing implementation where possible, define its ELO Web integration point, preserve upstream/downstream contracts, and include evidence, provenance, tenant/authentication, governance and regression coverage as applicable.

If a capability cannot yet be integrated through the governed path, register the GAP rather than creating a parallel implementation.

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

`ELO Web → ELO Cognitive → Simbionte Contract → Hermes → Evidence → Governed Learning → Evolution Gate`

MCP remains an external mechanism available to Hermes; it does not replace or redefine Symbionte and does not grant native ELO capability or automatic promotion.

## Definition of integrated

ELO Web is considered integrated only when production, authentication, Cognitive, ProcessView where applicable, evidence/provenance, governed Symbionte/Hermes execution and Evolution Gate are demonstrably connected without creating a parallel authority or secret-bearing browser path.
