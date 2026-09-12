export const ELO_CANONICAL_SUPABASE_PROJECT_REF = "fxbpevjrkwhbicpmecow";
export const ELO_CANONICAL_SUPABASE_URL = `https://${ELO_CANONICAL_SUPABASE_PROJECT_REF}.supabase.co`;

export function getCanonicalSupabaseConfig() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const key = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)?.trim();

  if (!url || !key) {
    throw new Error("ELO Web: configure NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY (or NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY).");
  }

  let hostname = "";
  try {
    hostname = new URL(url).hostname.toLowerCase();
  } catch {
    throw new Error("ELO Web: NEXT_PUBLIC_SUPABASE_URL is invalid.");
  }

  const canonicalHostname = `${ELO_CANONICAL_SUPABASE_PROJECT_REF}.supabase.co`;
  if (hostname !== canonicalHostname) {
    throw new Error(`ELO Web: Supabase project mismatch. Expected ${ELO_CANONICAL_SUPABASE_PROJECT_REF}, received ${hostname}.`);
  }

  return { url: ELO_CANONICAL_SUPABASE_URL, key };
}
