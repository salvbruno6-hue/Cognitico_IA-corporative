import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

const READ_ACTIONS = new Set(["read", "consult", "search", "inspect"]);
const CRITICAL_ACTIONS = new Set([
  "modify_cognitive_identity",
  "modify_core",
  "modify_canonical_memory",
  "modify_security_policy",
  "change_permissions",
  "promote_to_core",
  "merge_protected_change",
]);

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
    .select("identity_id,display_name,active,provider,provider_subject,enterprise_context")
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

  const roles = (roleRows ?? [])
    .map((row: any) => row.elo_roles)
    .filter((role: any) => role?.active === true)
    .map((role: any) => String(role.code));

  return { ok: true as const, user: data.user, identity, roles };
}

async function resolveActiveSession(identityId: string, requestId: string) {
  const { data: sessions, error } = await supabase
    .from("elo_identity_sessions")
    .select("session_id,issued_at,expires_at,revoked_at,last_seen_at")
    .eq("identity_id", identityId)
    .is("revoked_at", null)
    .order("issued_at", { ascending: false })
    .limit(1);
  if (error) return { ok: false as const, reason: "session_lookup_failed" };

  const now = Date.now();
  const session = (sessions ?? []).find((candidate: any) => {
    const expiresAt = Date.parse(String(candidate.expires_at));
    return Number.isFinite(expiresAt) && expiresAt > now;
  });
  if (!session) return { ok: false as const, reason: "active_elo_session_required" };

  return { ok: true as const, session, requestId };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "authorization, content-type, x-elo-request-id",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
  }});
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const auth = await authenticate(req);
  if (!auth.ok) {
    const status = auth.reason === "missing_bearer" || auth.reason === "invalid_token" ? 401 : 403;
    return json({ authorized: false, reason: auth.reason }, status);
  }

  const requestId = req.headers.get("x-elo-request-id")?.trim() || crypto.randomUUID();
  let body: any = {};
  try { body = await req.json(); } catch { return json({ authorized: false, reason: "invalid_json" }, 400); }

  const action = typeof body.action === "string" && body.action.trim() ? body.action.trim() : "read";
  const repository = typeof body.repository === "string" ? body.repository.trim() : "";

  const session = await resolveActiveSession(auth.identity.identity_id, requestId);
  if (!session.ok) {
    await supabase.from("elo_authorization_audit").insert({
      identity_id: auth.identity.identity_id,
      action,
      resource: repository || null,
      decision: "DENY",
      reason: session.reason,
      request_id: requestId,
    });
    return json({ authorized: false, reason: session.reason }, 403);
  }

  if (repository) {
    const { data: scopes, error: scopeError } = await supabase
      .from("elo_identity_scopes")
      .select("elo_scopes(scope_key,active)")
      .eq("identity_id", auth.identity.identity_id);
    if (scopeError) return json({ authorized: false, reason: "scope_lookup_failed" }, 403);

    const allowed = (scopes ?? []).some((row: any) =>
      row.elo_scopes?.active === true && row.elo_scopes?.scope_key === repository
    );
    if (!allowed) {
      await supabase.from("elo_authorization_audit").insert({
        identity_id: auth.identity.identity_id,
        session_id: session.session.session_id,
        action,
        resource: repository,
        decision: "DENY",
        reason: "repository_out_of_scope",
        request_id: requestId,
      });
      return json({ authorized: false, reason: "repository_out_of_scope" }, 403);
    }
  }

  const isCanonicalAdmin = auth.roles.includes("ELO_ADMIN") || auth.roles.includes("CANONICAL_ADMIN");
  if (CRITICAL_ACTIONS.has(action) && !isCanonicalAdmin) {
    await supabase.from("elo_authorization_audit").insert({
      identity_id: auth.identity.identity_id,
      session_id: session.session.session_id,
      action,
      resource: repository || null,
      decision: "DENY",
      reason: "canonical_authority_required",
      request_id: requestId,
    });
    return json({ authorized: false, reason: "canonical_authority_required" }, 403);
  }
  if (!READ_ACTIONS.has(action) && !CRITICAL_ACTIONS.has(action)) {
    await supabase.from("elo_authorization_audit").insert({
      identity_id: auth.identity.identity_id,
      session_id: session.session.session_id,
      action,
      resource: repository || null,
      decision: "DENY",
      reason: "action_not_granted",
      request_id: requestId,
    });
    return json({ authorized: false, reason: "action_not_granted" }, 403);
  }

  await supabase.from("elo_authorization_audit").insert({
    identity_id: auth.identity.identity_id,
    session_id: session.session.session_id,
    action,
    resource: repository || null,
    decision: "ALLOW",
    reason: "identity_session_role_and_scope_verified",
    request_id: requestId,
  });

  return json({
    authorized: true,
    role: auth.roles[0] ?? null,
    roles: auth.roles,
    identity_id: auth.identity.identity_id,
    session_id: session.session.session_id,
    display_name: auth.identity.display_name,
    provider: auth.identity.provider,
    enterprise_context: auth.identity.enterprise_context,
    action,
    repository: repository || null,
    request_id: requestId,
    authorization_authority: "elo-authz",
  });
});
