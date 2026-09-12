import { NextResponse } from "next/server";
import { executeHermesInVercelSandbox, type HermesExecutionRequest } from "@/lib/elo-hermes-sandbox";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function authorized(request: Request): boolean {
  const expected = process.env.ELO_HERMES_RUNTIME_TOKEN?.trim();
  const supplied = request.headers.get("authorization") ?? "";
  return Boolean(expected && supplied === `Bearer ${expected}`);
}

export async function POST(request: Request) {
  if (!authorized(request)) {
    return NextResponse.json({ code: "UNAUTHORIZED", message: "Hermes runtime boundary rejected the request." }, { status: 401 });
  }

  try {
    const body = await request.json() as Partial<HermesExecutionRequest>;
    if (
      typeof body.request_id !== "string" ||
      typeof body.intent !== "string" ||
      typeof body.tenant_scope !== "string" ||
      typeof body.mission_class !== "string" ||
      !Array.isArray(body.authorized_capabilities) ||
      body.authorized_capabilities.length === 0
    ) {
      return NextResponse.json({ code: "INVALID_REQUEST", message: "A valid ELO HermesExecutionRequest is required." }, { status: 400 });
    }

    const result = await executeHermesInVercelSandbox({
      request_id: body.request_id,
      intent: body.intent,
      context: body.context ?? {},
      tenant_scope: body.tenant_scope,
      mission_class: body.mission_class,
      authorized_capabilities: body.authorized_capabilities,
      method: body.method ?? null,
      constraints: body.constraints ?? {},
      evidence_requirements: body.evidence_requirements ?? [],
      execution_policy: body.execution_policy ?? {},
      contract_version: body.contract_version ?? "1.0",
    });

    return NextResponse.json(result, { status: result.status === "completed" ? 200 : 502 });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Hermes execution failed.";
    return NextResponse.json({ code: "HERMES_EXECUTION_FAILED", message }, { status: 500 });
  }
}
