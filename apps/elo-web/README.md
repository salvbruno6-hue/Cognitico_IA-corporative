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
- Sector-specific dashboard model for Planning, Commercial, Finance, HR, Operations, PCP, and IT.
- Mission input surface.
- KPI cards, chart surface, quick actions, and governance footer.
- Tailwind CSS v4.
- Next.js App Router.

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
3. Add mission lifecycle states and evidence panels.
4. Add reusable ELO design-system primitives.
5. Connect Hermes through the ELO server boundary; never directly from the browser.
6. Add Playwright coverage for the shared shell and critical missions.
