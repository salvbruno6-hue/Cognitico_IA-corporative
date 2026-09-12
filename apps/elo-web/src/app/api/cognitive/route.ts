import { NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";
import { ELOCognitiveError, executeCognitiveMission } from "@/lib/elo-cognitive";
import { getCanonicalSupabaseConfig } from "@/lib/supabase/config";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

type AuthorizationResponse = {
  authorized?: boolean;
  reason?: string;
  message?: string;
  session_id?: string;
  authorization_authority?: string;
};

function getBearerToken(request: Request) {
  const header = request.headers.get("authorization") ?? "";
  return header.startsWith("Bearer ") ? header.slice("Bearer ".length).trim() : "";
}

function authorizationMessage(payload: unknown) {
  if (typeof payload === "object" && payload !== null && "reason" in payload && typeof (payload as AuthorizationResponse).reason === "string") return (payload as AuthorizationResponse).reason;
  if (typeof payload === "object" && payload !== null && "message" in payload && typeof (payload as AuthorizationResponse).message === "string") return (payload as AuthorizationResponse).message;
  return "ELO Authorization recusou a missão.";
}

async function establishAuthorizedContext(request: Request, accessToken: string) {
  const response = await fetch(new URL("/api/authorization", request.url), {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
      "x-elo-request-id": request.headers.get("x-elo-request-id")?.trim() || crypto.randomUUID(),
    },
    body: JSON.stringify({ action: "consult" }),
    cache: "no-store",
  });
  const payload: unknown = await response.json().catch(() => null);
  if (!response.ok || typeof payload !== "object" || payload === null || (payload as AuthorizationResponse).authorized !== true) {
    throw new ELOCognitiveError(authorizationMessage(payload), response.status >= 400 ? response.status : 403, "AUTHORIZATION_DENIED");
  }
  const authorization = payload as AuthorizationResponse;
  if (!authorization.session_id || authorization.authorization_authority !== "elo-authz") {
    throw new ELOCognitiveError("A sessão autorizada do ELO não foi confirmada pela autoridade elo-authz.", 403, "AUTHORIZATION_CONTEXT_INVALID");
  }
  return authorization;
}

export async function POST(request: Request) {
  try {
    const { url: supabaseUrl, key: supabaseKey } = getCanonicalSupabaseConfig();
    const accessToken = getBearerToken(request);
    if (!accessToken) {
      return NextResponse.json({ code: "UNAUTHORIZED", message: "Sessão autenticada do ELO não foi apresentada." }, { status: 401 });
    }

    const supabase = createClient(supabaseUrl, supabaseKey, { auth: { persistSession: false, autoRefreshToken: false } });
    const { data: userData, error: userError } = await supabase.auth.getUser(accessToken);
    if (userError || !userData.user) {
      return NextResponse.json({ code: "UNAUTHORIZED", message: "Sessão Supabase inválida ou expirada." }, { status: 401 });
    }

    const body = await request.json() as {
      message?: unknown;
      tenant_id?: unknown;
      principal_id?: unknown;
      user_id?: unknown;
      domain?: unknown;
      context?: unknown;
    };

    const message = typeof body.message === "string" ? body.message.trim() : "";
    const tenantId = typeof body.tenant_id === "string" ? body.tenant_id.trim() : "";
    const domain = typeof body.domain === "string" ? body.domain.trim() : "";
    if (!message || !tenantId || !domain) {
      return NextResponse.json({ code: "INVALID_REQUEST", message: "message, tenant_id e domain são obrigatórios." }, { status: 400 });
    }

    if (typeof body.principal_id === "string" && body.principal_id.trim() && body.principal_id.trim() !== userData.user.id) {
      return NextResponse.json({ code: "FORBIDDEN", message: "principal_id não corresponde à identidade autenticada do ELO." }, { status: 403 });
    }

    const authorization = await establishAuthorizedContext(request, accessToken);
    const sessionId = authorization.session_id!;

    const result = await executeCognitiveMission({
      message,
      tenantId,
      principalId: userData.user.id,
      userId: userData.user.id,
      domain,
      sessionId,
      context: body.context && typeof body.context === "object" && !Array.isArray(body.context) ? body.context as Record<string, unknown> : {},
    });

    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    if (error instanceof ELOCognitiveError) return NextResponse.json({ code: error.code, message: error.message }, { status: error.status });
    return NextResponse.json({ code: "COGNITIVE_PROCESSING_FAILED", message: "Falha ao processar a missão cognitiva." }, { status: 500 });
  }
}
