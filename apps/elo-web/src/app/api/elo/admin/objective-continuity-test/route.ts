import { NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const CANONICAL_REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative";
const TEST_TENANT_ID = "multiteiner";
const TEST_OBJECTIVE_ID = "ELO-DIALOGUE-HANDOFF-1079";
const TEST_WORKSTREAM_ID = "dialogue-handoff-real-test";
const TEST_OPERATION = `continue_objective:${TEST_OBJECTIVE_ID}`;
const TEST_GRANT_SECONDS = 300;

type Stage = "request" | "session" | "store" | "identity" | "binding" | "grant" | "checkpoint" | "cycle";

function bearer(request: Request) {
  const header = request.headers.get("authorization")?.trim() ?? "";
  return header.startsWith("Bearer ") ? header.slice(7).trim() : "";
}

function json(data: unknown, status = 200) {
  return NextResponse.json(data, { status, headers: { "Cache-Control": "no-store" } });
}

function fail(stage: Stage, code: string, status: number, extra: Record<string, unknown> = {}) {
  console.info("elo_objective_continuity_test", { stage, code, status });
  return json({ stage, code, ...extra }, status);
}

export async function POST(request: Request) {
  const accessToken = bearer(request);
  const publicUrl = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
  const publicKey = (process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)?.trim();
  const serviceUrl = (process.env.ELO_FORGE_SUPABASE_URL ?? publicUrl ?? "").trim();
  const serviceKey = (process.env.ELO_FORGE_SUPABASE_SERVICE_ROLE_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY ?? "").trim();

  console.info("elo_objective_continuity_test", { stage: "request", code: "RECEIVED" });

  if (!accessToken || !publicUrl || !publicKey) {
    return fail("session", "UNAUTHORIZED", 401, { message: "Sessão autenticada do ELO não foi apresentada." });
  }
  if (!serviceUrl || !serviceKey) {
    return fail("store", "STORE_UNAVAILABLE", 503, { message: "Persistência governada do ELO não está configurada." });
  }

  const userClient = createClient(publicUrl, publicKey, { auth: { persistSession: false, autoRefreshToken: false } });
  const { data: userData, error: userError } = await userClient.auth.getUser(accessToken);
  if (userError || !userData.user) {
    return fail("session", "UNAUTHORIZED", 401, { message: "Sessão Supabase inválida ou expirada." });
  }
  console.info("elo_objective_continuity_test", { stage: "session", code: "SESSION_VERIFIED" });

  const admin = createClient(serviceUrl, serviceKey, { auth: { persistSession: false, autoRefreshToken: false } });
  const { data: identity, error: identityError } = await admin
    .from("elo_identity_registry")
    .select("identity_id")
    .eq("auth_user_id", userData.user.id)
    .eq("active", true)
    .maybeSingle();
  if (identityError) return fail("identity", "IDENTITY_LOOKUP_FAILED", 503);
  if (!identity?.identity_id) return fail("identity", "IDENTITY_NOT_REGISTERED", 403);
  console.info("elo_objective_continuity_test", { stage: "identity", code: "IDENTITY_RESOLVED" });

  const { data: bindings, error: bindingError } = await admin
    .from("elo_operator_github_bindings")
    .select("binding_id,identity_id,repository_full_name,operation_class,active")
    .eq("identity_id", identity.identity_id)
    .eq("repository_full_name", CANONICAL_REPOSITORY)
    .eq("active", true)
    .limit(2);
  if (bindingError) return fail("binding", "BINDING_LOOKUP_FAILED", 503);
  if ((bindings ?? []).length !== 1) {
    return fail("binding", "UNIQUE_ACTIVE_BINDING_REQUIRED", 409, { count: bindings?.length ?? 0 });
  }

  const binding = bindings![0];
  console.info("elo_objective_continuity_test", { stage: "binding", code: "BINDING_RESOLVED", operation_class: binding.operation_class });

  const requestId = crypto.randomUUID();
  const authzResponse = await fetch(`${serviceUrl}/functions/v1/elo-authz`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
      "x-elo-request-id": requestId,
    },
    body: JSON.stringify({
      action: "issue_authorization_grant",
      binding_id: binding.binding_id,
      authorization_state: "elo-execution-authorized",
      operation: TEST_OPERATION,
      repository: CANONICAL_REPOSITORY,
      resource_id: TEST_OBJECTIVE_ID,
      expires_in_seconds: TEST_GRANT_SECONDS,
    }),
    cache: "no-store",
  });
  const grant = await authzResponse.json().catch(() => ({ authorized: false, reason: "invalid_authorization_response" })) as Record<string, unknown>;
  if (!authzResponse.ok || grant.authorized !== true) {
    return fail("grant", "GRANT_ISSUANCE_DENIED", authzResponse.status >= 400 ? authzResponse.status : 403, {
      reason: grant.reason ?? "authorization_denied",
      request_id: requestId,
    });
  }
  console.info("elo_objective_continuity_test", { stage: "grant", code: "GRANT_ISSUED" });

  const { data: existingCheckpoint, error: checkpointError } = await admin
    .from("elo_objective_continuity_checkpoints")
    .select("state_version,last_progress_token,status")
    .eq("tenant_id", TEST_TENANT_ID)
    .eq("objective_id", TEST_OBJECTIVE_ID)
    .eq("workstream_id", TEST_WORKSTREAM_ID)
    .maybeSingle();
  if (checkpointError) return fail("checkpoint", "CHECKPOINT_LOOKUP_FAILED", 503);
  console.info("elo_objective_continuity_test", { stage: "checkpoint", code: existingCheckpoint ? "CHECKPOINT_RESOLVED" : "CHECKPOINT_INITIAL" });

  const origin = new URL(request.url).origin;
  const cycleRequestId = crypto.randomUUID();
  const cycleResponse = await fetch(`${origin}/api/elo/chat/prefinalize`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
      "x-elo-request-id": cycleRequestId,
    },
    body: JSON.stringify({
      tenant_id: TEST_TENANT_ID,
      objective_id: TEST_OBJECTIVE_ID,
      objective_title: "Teste real do handoff GPT ↔ ELO",
      workstream_id: TEST_WORKSTREAM_ID,
      progress_token: existingCheckpoint?.last_progress_token || "pr1079-contract-and-gates-green",
      proposed_next_action: "validar retorno ELO→GPT e checkpoint persistido",
      evidence_refs: [
        "github:pr:1079:merged:6fdf50ba742f27213ff44ed945e0d0c90ba582a3",
        "github:workflow:elo-evolution-gate:40202650716:success",
      ],
      expected_checkpoint_version: existingCheckpoint?.state_version ?? null,
      within_scope: true,
      authority_available: true,
      risk_level: "LOW",
      max_cycles: 3,
    }),
    cache: "no-store",
  });
  const cycle = await cycleResponse.json().catch(() => ({ code: "INVALID_CYCLE_RESPONSE" })) as Record<string, unknown>;
  if (!cycleResponse.ok) {
    return fail("cycle", "OBJECTIVE_CYCLE_FAILED", cycleResponse.status >= 400 ? cycleResponse.status : 500, {
      grant: {
        authorization_state: (grant.grant as Record<string, unknown> | undefined)?.authorization_state ?? grant.authorization_state,
        grant_id: (grant.grant as Record<string, unknown> | undefined)?.grant_id ?? grant.grant_id,
        expires_at: (grant.grant as Record<string, unknown> | undefined)?.expires_at ?? grant.expires_at,
        authorization_authority: grant.authorization_authority,
      },
      cycle,
    });
  }
  console.info("elo_objective_continuity_test", { stage: "cycle", code: "CYCLE_SUCCEEDED" });

  const nestedGrant = (grant.grant as Record<string, unknown> | undefined) ?? grant;
  return json({
    authorized: true,
    stage: "cycle",
    test: "ELO_DIALOGUE_HANDOFF_REAL",
    objective_id: TEST_OBJECTIVE_ID,
    workstream_id: TEST_WORKSTREAM_ID,
    operation: TEST_OPERATION,
    binding: {
      operation_class: binding.operation_class,
      repository: binding.repository_full_name,
    },
    grant: {
      authorization_state: nestedGrant.authorization_state,
      grant_id: nestedGrant.grant_id,
      expires_at: nestedGrant.expires_at,
      authorization_authority: grant.authorization_authority,
    },
    cycle,
  });
}
