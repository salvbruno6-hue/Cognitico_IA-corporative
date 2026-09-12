import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { createClient } from "@supabase/supabase-js";
import { ELOCognitiveError, executeCognitiveMission } from "@/lib/elo-cognitive";
import { createCognitiveSessionId, ELO_COGNITIVE_SESSION_COOKIE, isValidCognitiveSessionId } from "@/lib/elo-cognitive-session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function getBearerToken(request: Request) {
  const header = request.headers.get("authorization") ?? "";
  return header.startsWith("Bearer ") ? header.slice("Bearer ".length).trim() : "";
}

export async function POST(request: Request) {
  try {
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
    const supabaseKey = (process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)?.trim();
    const accessToken = getBearerToken(request);
    if (!supabaseUrl || !supabaseKey || !accessToken) {
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
      session_id?: unknown;
      context?: unknown;
    };

    const message = typeof body.message === "string" ? body.message.trim() : "";
    const tenantId = typeof body.tenant_id === "string" ? body.tenant_id.trim() : "";
    const domain = typeof body.domain === "string" ? body.domain.trim() : "";
    if (!message || !tenantId || !domain) {
      return NextResponse.json({ code: "INVALID_REQUEST", message: "message, tenant_id e domain são obrigatórios." }, { status: 400 });
    }

    // The authenticated Supabase identity is the canonical principal. Never allow
    // a browser payload to impersonate another principal in the cognitive layer.
    if (typeof body.principal_id === "string" && body.principal_id.trim() && body.principal_id.trim() !== userData.user.id) {
      return NextResponse.json({ code: "FORBIDDEN", message: "principal_id não corresponde à identidade autenticada do ELO." }, { status: 403 });
    }

    const requestCookies = await cookies();
    const suppliedSessionId = typeof body.session_id === "string" ? body.session_id.trim() : "";
    const cookieSessionId = requestCookies.get(ELO_COGNITIVE_SESSION_COOKIE)?.value;
    const sessionId = isValidCognitiveSessionId(suppliedSessionId)
      ? suppliedSessionId
      : typeof cookieSessionId === "string" && isValidCognitiveSessionId(cookieSessionId)
        ? cookieSessionId
        : createCognitiveSessionId();

    const result = await executeCognitiveMission({
      message,
      tenantId,
      // Identity comes from the verified Supabase access token, not from the client body.
      principalId: userData.user.id,
      userId: userData.user.id,
      domain,
      sessionId,
      context: body.context && typeof body.context === "object" && !Array.isArray(body.context) ? body.context as Record<string, unknown> : {},
    });

    const response = NextResponse.json(result, { status: 200 });
    response.cookies.set({
      name: ELO_COGNITIVE_SESSION_COOKIE,
      value: sessionId,
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60 * 8,
    });
    return response;
  } catch (error) {
    if (error instanceof ELOCognitiveError) return NextResponse.json({ code: error.code, message: error.message }, { status: error.status });
    return NextResponse.json({ code: "COGNITIVE_PROCESSING_FAILED", message: "Falha ao processar a missão cognitiva." }, { status: 500 });
  }
}
