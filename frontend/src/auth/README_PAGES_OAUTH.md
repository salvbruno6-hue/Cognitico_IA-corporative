# ELO OAuth on GitHub Pages

The project is hosted under `/Cognitico_IA-corporative/`.

OAuth callback must therefore use:

`https://salvbruno6-hue.github.io/Cognitico_IA-corporative/auth/callback`

Use `import.meta.env.BASE_URL` or the shared `ELO_BASE_PATH` helper for client-side redirects. Do not redirect to `/` because that leaves the project path.
