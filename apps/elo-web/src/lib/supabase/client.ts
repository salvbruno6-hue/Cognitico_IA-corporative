import { createBrowserClient } from "@supabase/ssr";
import { getCanonicalSupabaseConfig } from "@/lib/supabase/config";

let client: ReturnType<typeof createBrowserClient> | undefined;

export function createClient() {
  if (client) return client;

  const { url, key } = getCanonicalSupabaseConfig();
  client = createBrowserClient(url, key);
  return client;
}
