import { NextResponse } from "next/server";
import { ELOCognitiveError, executeCognitiveMission } from "@/lib/elo-cognitive";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  try {
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

    const result = await executeCognitiveMission({
      message,
      tenantId,
      principalId: typeof body.principal_id === "string" ? body.principal_id : undefined,
      userId: typeof body.user_id === "string" ? body.user_id : undefined,
      domain,
      sessionId: typeof body.session_id === "string" ? body.session_id : undefined,
      context: body.context && typeof body.context === "object" && !Array.isArray(body.context) ? body.context as Record<string, unknown> : {},
    });

    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    if (error instanceof ELOCognitiveError) return NextResponse.json({ code: error.code, message: error.message }, { status: error.status });
    return NextResponse.json({ code: "COGNITIVE_PROCESSING_FAILED", message: "Falha ao processar a missão cognitiva." }, { status: 500 });
  }
}
