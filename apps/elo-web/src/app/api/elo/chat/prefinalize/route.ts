import { NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";
import { ObjectiveContinuityError, runObjectiveCycle } from "@/lib/elo-objective-continuity";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const CANONICAL_REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative";

function bearer(request: Request) {
  const header = request.headers.get("authorization")?.trim() ?? "";
  return header.startsWith("Bearer ") ? header.slice(7).trim() : "";
}

function text(value: unknown) {
  return typeof value === "string" ? value.trim() : "";
}

function stringArray(value: unknown) {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string").map((item) => item.trim()).filter(Boolean) : [];
}

export async function POST(request: Request) {
  const accessToken = bearer(request);
  const publicUrl = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const publicKey = (process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)?.trim();
  if (!accessToken || !publicUrl || !publicKey) {
    return NextResponse.json({ code: "UNAUTHORIZED", message: "Sessão autenticada do ELO não foi apresentada." }, { status: 401 });
  }

  const supabase = createClient(publicUrl, publicKey, { auth: { persistSession: false, autoRefreshToken: false } });
  const { data: userData, error: userError } = await supabase.auth.getUser(accessToken);
  if (userError || !userData.user) {
    return NextResponse.json({ code: "UNAUTHORIZED", message: "Sessão Supabase inválida ou expirada." }, { status: 401 });
  }

  let body: Record<string, unknown>;
  try {
    body = await request.json() as Record<string, unknown>;
  } catch {
    return NextResponse.json({ code: "INVALID_REQUEST", message: "JSON inválido." }, { status: 400 });
  }

  const tenantId = text(body.tenant_id);
  const objectiveId = text(body.objective_id);
  const objectiveTitle = text(body.objective_title) || objectiveId;
  const workstreamId = text(body.workstream_id);
  const progressToken = text(body.progress_token);
  const proposedNextAction = text(body.proposed_next_action);
  const evidenceRefs = stringArray(body.evidence_refs);
  const expectedCheckpointVersion = typeof body.expected_checkpoint_version === "number" && Number.isInteger(body.expected_checkpoint_version)
    ? body.expected_checkpoint_version
    : null;

  if (!tenantId || !objectiveId || !workstreamId || !progressToken || !proposedNextAction || evidenceRefs.length === 0) {
    return NextResponse.json({ code: "INVALID_REQUEST", message: "tenant_id, objective_id, workstream_id, progress_token, proposed_next_action e evidence_refs são obrigatórios." }, { status: 400 });
  }

  const authzUrl = (process.env.ELO_FORGE_SUPABASE_URL ?? publicUrl).trim();
  const requestId = request.headers.get("x-elo-request-id")?.trim() || crypto.randomUUID();
  const authzResponse = await fetch(`${authzUrl}/functions/v1/elo-authz`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
      "x-elo-request-id": requestId,
    },
    body: JSON.stringify({
      action: "continue_objective",
      capability: "OBJECTIVE_CONTINUE",
      repository: CANONICAL_REPOSITORY,
      resource_id: objectiveId,
    }),
    cache: "no-store",
  });
  const authz = await authzResponse.json().catch(() => ({ authorized: false, reason: "invalid_authorization_response" })) as Record<string, unknown>;
  if (!authzResponse.ok || authz.authorized !== true) {
    return NextResponse.json({
      code: "FORBIDDEN",
      message: "O elo-authz não autorizou a continuidade autônoma deste objetivo.",
      reason: authz.reason ?? "authorization_denied",
      request_id: requestId,
    }, { status: authzResponse.status >= 400 ? authzResponse.status : 403 });
  }

  const authorizationIdentityId = text(authz.identity_id);
  const authorizationEvidenceRef = text(authz.evidence_ref) || `elo-authz:${requestId}`;
  if (!authorizationIdentityId) {
    return NextResponse.json({ code: "AUTHORIZATION_EVIDENCE_INVALID", message: "elo-authz não retornou identidade autorizada." }, { status: 503 });
  }

  try {
    const result = await runObjectiveCycle({
      tenantId,
      objectiveId,
      objectiveTitle,
      workstreamId,
      expectedCheckpointVersion,
      progressToken,
      evidenceRefs,
      proposedNextAction,
      authorizationEvidenceRef,
      authorizationIdentityId,
      objectiveSatisfied: body.objective_satisfied === true,
      withinScope: body.within_scope !== false,
      authorityAvailable: body.authority_available !== false,
      riskLevel: text(body.risk_level) || "LOW",
      maxCycles: typeof body.max_cycles === "number" && Number.isInteger(body.max_cycles) && body.max_cycles > 0 ? body.max_cycles : 12,
    });
    return NextResponse.json({
      ...result,
      authorization_authority: "elo-authz",
      authorization_evidence_ref: authorizationEvidenceRef,
      request_id: requestId,
    }, { status: 200, headers: { "Cache-Control": "no-store" } });
  } catch (error) {
    if (error instanceof ObjectiveContinuityError) {
      return NextResponse.json({ code: error.code, message: error.message, request_id: requestId }, { status: error.status });
    }
    return NextResponse.json({ code: "PREFINALIZATION_FAILED", message: "Falha ao executar a prefinalização governada do ELO.", request_id: requestId }, { status: 500 });
  }
}
