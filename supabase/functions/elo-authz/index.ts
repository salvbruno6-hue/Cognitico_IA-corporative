import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "authorization, content-type",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
    },
  });
}

async function authenticate(req: Request) {
  const header = req.headers.get("Authorization") ?? "";
  const token = header.startsWith("Bearer ") ? header.slice(7) : "";
  if (!token) return { ok: false as const, reason: "missing_bearer" };

  const { data, error } = await supabase.auth.getUser(token);
  if (error || !data.user) return { ok: false as const, reason: "invalid_token" };

  const { data: identity, error: identityError } = await supabase
    .from("elo_identity_registry")
    .select("identity_id,display_name,active")
    .eq("auth_user_id", data.user.id)
    .eq("active", true)
    .maybeSingle();
  if (identityError) return { ok: false as const, reason: "identity_lookup_failed" };
  if (!identity) return { ok: false as const, reason: "operator_binding_missing" };

  const { data: roleRows, error: roleError } = await supabase
    .from("elo_identity_roles")
    .select("role_id,elo_roles(code,active)")
    .eq("identity_id", identity.identity_id);
  if (roleError) return { ok: false as const, reason: "role_lookup_failed" };

  const isAdmin = (roleRows ?? []).some((row: any) =>
    row.elo_roles?.code === "ELO_ADMIN" && row.elo_roles?.active === true
  );
  if (!isAdmin) return { ok: false as const, reason: "elo_admin_required" };

  return { ok: true as const, user: data.user, identity };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "authorization, content-type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
  }});
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const auth = await authenticate(req);
  if (!auth.ok) {
    const status = auth.reason === "missing_bearer" || auth.reason === "invalid_token" ? 401 : 403;
    return json({ authorized: false, reason: auth.reason }, status);
  }

  return json({
    authorized: true,
    role: "ELO_ADMIN",
    identity_id: auth.identity.identity_id,
    display_name: auth.identity.display_name,
  });
});
