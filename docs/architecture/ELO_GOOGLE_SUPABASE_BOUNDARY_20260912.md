# ELO Web — Google/Supabase boundary

## Canonical authority

ELO Web uses the canonical Supabase project `fxbpevjrkwhbicpmecow` (Elo-forge).

## OAuth boundary

Google OAuth is handled by Supabase Auth. The browser must never receive the Google Client Secret. The OAuth callback is:

`https://fxbpevjrkwhbicpmecow.supabase.co/auth/v1/callback`

The existing Google OAuth Client ID is retained; no replacement credential is required.

## Runtime boundary

Browser → ELO Web server boundary → canonical Supabase/Auth → ELO Cognitive/Core → Symbiont → Hermes.

Hermes endpoint, runtime token, and secrets remain server-side.

## Change control

Google Cloud credential configuration must not modify GitHub source, migrations, or the ELO cognitive authority. Any application change must be represented by a reviewed GitHub commit and validated through Vercel before production.
