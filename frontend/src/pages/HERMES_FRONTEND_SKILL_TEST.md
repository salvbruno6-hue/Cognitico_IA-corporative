# Hermes Frontend Skill — ELO Pages Test

## Canonical skill input

`salvbruno6-hue/ELO-Hermes-Agent/skills/software-development/elo-frontend-engineering/SKILL.md`

Pinned source commit: `45ac26a217cc93603d19db8e4b9b064ca57d6806`.

## Applied requirements

- Inspect the existing ELO frontend before changing architecture.
- Keep browser responsibility limited to presentation, interaction and navigation.
- Keep governance, authorization, canonical knowledge and learning authority in ELO.
- Treat Hermes as an execution boundary reached through a governed request contract.
- Use feature-oriented composition and explicit boundaries.
- Exercise the shared shell, mission surface, workspace blocks and governance surface.
- Use semantic design tokens and preserve ELO visual identity.
- Provide keyboard-visible focus and accessible names.
- Provide responsive/mobile-safe composition.
- Provide explicit interaction/loading/success states.
- Never place Hermes credentials, Supabase service credentials or governance secrets in the client.

## Test limitation

The page executes a deterministic local interaction to validate frontend behavior. It does **not** claim a live Hermes provider execution. A live Hermes integration test requires the governed ELO server contract and evidence path.

## Expected review evidence

1. Type checking passes.
2. Production build passes.
3. GitHub Pages build produces `dist/index.html` and SPA fallback.
4. No secret/provider credential crosses the browser boundary.
5. The PR records the skill lineage and architectural boundary.
6. UI behavior is verified in the published ELO Pages environment after an approved merge.
