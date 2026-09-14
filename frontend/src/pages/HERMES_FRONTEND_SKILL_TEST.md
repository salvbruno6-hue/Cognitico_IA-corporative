# Hermes Frontend Engineering — ELO Core Application

## Canonical skill input

`salvbruno6-hue/ELO-Hermes-Agent/skills/software-development/elo-frontend-engineering/SKILL.md`

Pinned source commit: `45ac26a217cc93603d19db8e4b9b064ca57d6806`.

## Applied to the existing ELO Pages interface

The change is applied to the existing authenticated ELO core surface, not a separate demo page.

- Preserve the shared ELO shell and existing authentication boundary.
- Recompose the core as shared shell + mission surface + workspace + evidence + governance.
- Keep browser responsibility limited to presentation, interaction and navigation.
- Keep governance, authorization, canonical knowledge and learning authority in ELO.
- Treat Hermes as an execution runtime reached through a governed ELO request contract.
- Use feature-oriented composition and explicit one-directional boundaries.
- Replace hard-coded operational telemetry claims with explicit evidence/state placeholders.
- Use semantic design tokens and preserve the existing ELO visual identity.
- Provide visible keyboard focus and accessible names for interactive controls.
- Provide responsive/mobile-safe composition.
- Keep local preferences separate from server authority.
- Never place Hermes credentials, Supabase service credentials or governance secrets in the client.

## Verification boundary

This frontend change does **not** claim live Hermes execution. A live execution path requires the governed ELO server contract and evidence path already defined by the ELO architecture.

## Review evidence required before merge

1. Type checking passes.
2. Production build passes.
3. GitHub Pages build produces `dist/index.html` and the repository's SPA fallback strategy remains valid.
4. No secret/provider credential crosses the browser boundary.
5. Feature boundaries remain explicit and no parallel governance authority is introduced.
6. Published ELO Pages UI is visually/functionally verified after approved merge.
