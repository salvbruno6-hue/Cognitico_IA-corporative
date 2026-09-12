import { NextResponse } from "next/server";
import { ELO_CANONICAL_SUPABASE_URL, getCanonicalSupabaseConfig } from "@/lib/supabase/config";

const ALLOWED_ACTIONS = new Set(["establish_session", "revoke_session", "read", "consult", "search", "inspect"]);

type AuthorizationBody = {
  action?: unknown;
  capability?: unknown;
  repository?: unknown;
};

function json(data: unknown, status = 200) {
  return NextResponse.json(data, {
    status,
    headers: { "Cache-Control": "no-store" },
  });
}

export async function POST(request: Request) {
  const authorization = request.headers.get("authorization")?.trim() ?? "";
  if (!authorization.startsWith("Bearer ")) {
    return json({ authorized: false, reason: "missing_bearer" }, 401);
  }

  try {
    getCanonicalSupabaseConfig();
  } catch (error) {
    return json({
      authorized: false,
      reason: error instanceof Error ? error.message : "supabase_canonical_project_mismatch",
    }, 500);
  }

  let body: AuthorizationBody = {};
  try {
    body = (await request.json()) as AuthorizationBody;
  } catch {
    return json({ authorized: false, reason: "invalid_json" }, 400);
  }

  const action = typeof body.action === "string" && body.action.trim() ? body.action.trim() : "establish_session";
  if (!ALLOWED_ACTIONS.has(action)) {
    return json({ authorized: false, reason: "action_not_allowed_at_elo_web_boundary" }, 403);
  }

  const upstream = await fetch(`${ELO_CANONICAL_SUPABASE_URL}/functions/v1/elo-authz`, {
    method: "POST",
    headers: {
      Authorization: authorization,
      "Content-Type": "application/json",
      "x-elo-request-id": request.headers.get("x-elo-request-id")?.trim() || crypto.randomUUID(),
    },
    body: JSON.stringify({
      action,
      capability: typeof body.capability === "string" ? body.capability.trim() : undefined,
      repository: typeof body.repository === "string" ? body.repository.trim() : undefined,
    }),
    cache: "no-store",
  });

  const payload = await upstream.json().catch(() => ({
    authorized: false,
    reason: "invalid_authorization_response",
  }));

  return json(payload, upstream.status);
}
