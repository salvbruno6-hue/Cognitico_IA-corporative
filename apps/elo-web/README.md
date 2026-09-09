# ELO Web

Next.js frontend for the ELO experience layer.

## Boundary

```text
Browser
  -> ELO Web (Vercel / Next.js)
  -> ELO Cognitive API
  -> governed Hermes execution boundary
  -> Hermes runtime
```

The browser is not an authority for governance, canonical knowledge, infrastructure credentials, or Hermes execution.

## Current scaffold

- Shared ELO shell.
- Sector selector.
- Sector-specific workspace model for Planning, Commercial, Finance, HR, Operations, PCP, and IT.
- Mission input surface.
- KPI cards, chart surface, quick actions, and governance footer.
- Process navigation for the Planning workspace, grounded in the canonical Multiteiner process reference.
- Tailwind CSS v4.
- Next.js App Router.

## Process navigation principle

The frontend does not create a parallel business-process architecture. It presents the existing ELO process knowledge as an experience/navigation layer.

The first supported navigation is:

```text
ELO
  -> Planejamento
     -> Fluxo de Demanda
     -> Fluxo Modular
```

The process representation preserves the distinction between documented/reference structure and current operational state. Current state, evidence, deviation, and live metrics must come from governed ELO API contracts when that integration is implemented.

Canonical process source:

`ELO-PROC-MULTITEINER-001`

Ingestion and retrieval protocol:

`docs/ELO-012_MULTITEINER_FLOW_MODULAR_PROTOCOL.md`

## Vercel project settings

Use this repository with the Vercel project root set to:

`apps/elo-web`

Framework: **Next.js** (auto-detected).

Build command: default (`next build`).

Install command: default package-manager detection.

Production should receive only server-side ELO API configuration through project-scoped environment variables. Public values use the `NEXT_PUBLIC_` prefix only when intentionally exposed to the browser.

Vercel Preview deployments should be used for every feature branch before production merge.

## Next implementation stages

1. Replace static sector metrics with governed ELO API contracts.
2. Add authentication and role/sector authorization.
3. Connect process navigation to governed ELO process/view contracts instead of the current reference projection.
4. Add mission lifecycle states and evidence panels.
5. Add reusable ELO design-system primitives.
6. Connect Hermes through the ELO server boundary; never directly from the browser.
7. Add Playwright coverage for the shared shell, process navigation, and critical missions.
