import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
const supabaseAdmin = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
  auth: { autoRefreshToken: false, persistSession: false },
});

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, content-type, x-elo-request-id",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Cache-Control": "no-store",
  "Content-Type": "application/json",
};

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: corsHeaders });
}

function bearer(req: Request) {
  const header = req.headers.get("Authorization") ?? "";
  return header.startsWith("Bearer ") ? header.slice(7).trim() : "";
}

function providerSubject(user: any) {
  const identity = Array.isArray(user.identities) ? user.identities[0] : null;
  const provider = typeof identity?.provider === "string" ? identity.provider : "";
  const subject = typeof identity?.identity_data?.sub === "string"
    ? identity.identity_data.sub
    : typeof identity?.identity_data?.provider_id === "string"
      ? identity.identity_data.provider_id
      : "";
  return { provider, subject };
}

async function authenticate(req: Request) {
  const token = bearer(req);
  if (!token) return { ok: false as const, status: 401, reason: "missing_bearer" };
  const { data, error } = await supabaseAdmin.auth.getUser(token);
  if (error || !data.user) return { ok: false as const, status: 401, reason: "invalid_token" };
  return { ok: true as const, token, user: data.user };
}

async function bindIdentity(user: any) {
  const existing = await supabaseAdmin
    .from("elo_identity_registry")
    .select("identity_id,auth_user_id,provider,provider_subject,display_name,enterprise_context,active")
    .eq("auth_user_id", user.id)
    .eq("active", true)
    .maybeSingle();
  if (existing.error) return { ok: false as const, status: 503, reason: "identity_lookup_failed" };
  if (existing.data) return { ok: true as const, identity: existing.data, bound: false };

  const { provider, subject } = providerSubject(user);
  if (!provider || !subject) return { ok: false as const, status: 403, reason: "provider_binding_missing" };

  const candidate = await supabaseAdmin
    .from("elo_identity_registry")
    .select("identity_id,auth_user_id,provider,provider_subject,display_name,enterprise_context,active")
    .eq("provider", provider)
    .eq("provider_subject", subject)
    .eq("active", true)
    .maybeSingle();
  if (candidate.error) return { ok: false as const, status: 503, reason: "provider_identity_lookup_failed" };
  if (!candidate.data) return { ok: false as const, status: 403, reason: "operator_binding_missing" };
  if (candidate.data.auth_user_id && candidate.data.auth_user_id !== user.id) {
    return { ok: false as const, status: 403, reason: "identity_already_bound" };
  }

  const updated = await supabaseAdmin
    .from("elo_identity_registry")
    .update({ auth_user_id: user.id })
    .eq("identity_id", candidate.data.identity_id)
    .is("auth_user_id", null)
    .select("identity_id,auth_user_id,provider,provider_subject,display_name,enterprise_context,active")
    .maybeSingle();
  if (updated.error) return { ok: false as const, status: 503, reason: "identity_binding_failed" };
  if (!updated.data) return { ok: false as const, status: 409, reason: "identity_binding_race" };
  return { ok: true as const, identity: updated.data, bound: true };
}

async function establishSession(identityId: string) {
  const active = await supabaseAdmin
    .from("elo_identity_sessions")
    .select("session_id,identity_id,issued_at,expires_at,revoked_at,last_seen_at")
    .eq("identity_id", identityId)
    .is("revoked_at", null)
    .order("last_seen_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (active.error) return { ok: false as const, status: 503, reason: "session_lookup_failed" };

  const now = Date.now();
  if (active.data && Date.parse(String(active.data.expires_at)) > now) {
    const touched = await supabaseAdmin
      .from("elo_identity_sessions")
      .update({ last_seen_at: new Date().toISOString() })
      .eq("session_id", active.data.session_id);
    if (touched.error) return { ok: false as const, status: 503, reason: "session_touch_failed" };
    return { ok: true as const, session: active.data, reused: true };
  }

  if (active.data) {
    await supabaseAdmin
      .from("elo_identity_sessions")
      .update({ revoked_at: new Date().toISOString(), last_seen_at: new Date().toISOString() })
      .eq("session_id", active.data.session_id)
      .is("revoked_at", null);
  }

  const issuedAt = new Date();
  const expiresAt = new Date(issuedAt.getTime() + 8 * 60 * 60 * 1000);
  const created = await supabaseAdmin
    .from("elo_identity_sessions")
    .insert({
      session_id: crypto.randomUUID(),
      identity_id: identityId,
      issued_at: issuedAt.toISOString(),
      expires_at: expiresAt.toISOString(),
      revoked_at: null,
      last_seen_at: issuedAt.toISOString(),
    })
    .select("session_id,identity_id,issued_at,expires_at,revoked_at,last_seen_at")
    .single();
  if (created.error) return { ok: false as const, status: 503, reason: "session_create_failed" };
  return { ok: true as const, session: created.data, reused: false };
}

async function authorize(token: string, requestId: string) {
  const response = await fetch(`${SUPABASE_URL}/functions/v1/elo-authz`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      "x-elo-request-id": requestId,
    },
    body: JSON.stringify({ action: "read" }),
  });
  const payload = await response.json().catch(() => null);
  return { ok: response.ok, status: response.status, payload };
}

async function revokeSessions(identityId: string) {
  const now = new Date().toISOString();
  const result = await supabaseAdmin
    .from("elo_identity_sessions")
    .update({ revoked_at: now, last_seen_at: now })
    .eq("identity_id", identityId)
    .is("revoked_at", null);
  if (result.error) return { ok: false as const, status: 503, reason: "session_revoke_failed" };
  return { ok: true as const };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: corsHeaders });
  if (req.method !== "POST") return json({ ok: false, reason: "method_not_allowed" }, 405);

  const requestId = req.headers.get("x-elo-request-id")?.trim() || crypto.randomUUID();
  const auth = await authenticate(req);
  if (!auth.ok) return json({ ok: false, reason: auth.reason, request_id: requestId }, auth.status);

  let body: any = {};
  try { body = await req.json(); } catch { return json({ ok: false, reason: "invalid_json", request_id: requestId }, 400); }
  const operation = typeof body.operation === "string" ? body.operation.trim().toLowerCase() : "establish";

  const binding = await bindIdentity(auth.user);
  if (!binding.ok) return json({ ok: false, reason: binding.reason, request_id: requestId }, binding.status);

  if (operation === "revoke") {
    const revoked = await revokeSessions(binding.identity.identity_id);
    if (!revoked.ok) return json({ ok: false, reason: revoked.reason, request_id: requestId }, revoked.status);
    return json({ ok: true, operation, identity_id: binding.identity.identity_id, request_id: requestId, authorization_authority: "elo-authz" });
  }

  if (operation !== "establish") return json({ ok: false, reason: "unsupported_operation", request_id: requestId }, 400);

  const session = await establishSession(binding.identity.identity_id);
  if (!session.ok) return json({ ok: false, reason: session.reason, request_id: requestId }, session.status);

  const authorization = await authorize(auth.token, requestId);
  if (!authorization.ok || !authorization.payload?.authorized) {
    return json({
      ok: false,
      reason: authorization.payload?.reason ?? "authorization_denied",
      authorization: authorization.payload,
      identity_id: binding.identity.identity_id,
      session_id: session.session.session_id,
      request_id: requestId,
    }, authorization.status >= 400 ? authorization.status : 403);
  }

  return json({
    ok: true,
    operation,
    identity_id: binding.identity.identity_id,
    session_id: session.session.session_id,
    expires_at: session.session.expires_at,
    reused: session.reused,
    bound: binding.bound,
    authorization: authorization.payload,
    request_id: requestId,
    authorization_authority: "elo-authz",
  });
});
