import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

const AUTHZ_URL = `${SUPABASE_URL}/functions/v1/elo-authz`;
const CAPABILITY_MAP: Record<string, string> = {
  read: "READ",
  create_entity: "ADMIN",
  update_entity: "ADMIN",
  create_relation: "ADMIN",
  propose_schema: "ADMIN",
  create_schema: "ADMIN",
  alter_schema: "ADMIN",
  drop_schema: "ADMIN",
  lista_mae_insert: "LISTA_MAE_INSERT",
};

const READ_TABLES = new Set([
  "taxonomia",
  "dimensoes",
  "modelos",
  "modelo_apresentacao",
  "kits",
  "kit_itens",
  "lista_mae",
  "estrutura_modular",
  "estrutura_modular_itens",
]);

function json(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "authorization, content-type, x-elo-request-id",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
    },
  });
}

async function authorize(req: Request, action: string, repository: string) {
  const authorization = req.headers.get("Authorization") ?? "";
  if (!authorization.startsWith("Bearer ")) {
    return { ok: false as const, response: json({ authorized: false, reason: "missing_bearer" }, 401) };
  }

  const requestId = req.headers.get("x-elo-request-id")?.trim() || crypto.randomUUID();
  const capability = CAPABILITY_MAP[action];
  if (!capability) {
    return { ok: false as const, response: json({ authorized: false, reason: "unsupported_operation", request_id: requestId }, 400) };
  }

  const response = await fetch(AUTHZ_URL, {
    method: "POST",
    headers: {
      Authorization: authorization,
      "Content-Type": "application/json",
      "x-elo-request-id": requestId,
    },
    body: JSON.stringify({ action, capability, repository }),
  });

  const data = await response.json().catch(() => ({ authorized: false, reason: "invalid_authorization_response" }));
  if (!response.ok || data?.authorized !== true) {
    return { ok: false as const, response: json({ ...data, request_id: requestId }, response.status || 403) };
  }

  return { ok: true as const, requestId, capability, authorization: data };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, content-type, x-elo-request-id", "Access-Control-Allow-Methods": "POST, OPTIONS" } });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  try {
    const body = await req.json();
    const operation = String(body.operation ?? "");
    if (!operation) return json({ error: "operation_required" }, 400);

    const repository = String(body.repository ?? "").trim();
    const authz = await authorize(req, operation, repository);
    if (!authz.ok) return authz.response;


    if (operation === "lista_mae_insert") {
      const payload = body.data && typeof body.data === "object" ? body.data : {};
      const codItem = String(payload.cod_item ?? "").trim();
      const descricaoOficial = String(payload.descricao_oficial ?? "").trim();
      if (!codItem || !descricaoOficial) {
        return json({ error: "cod_item_and_descricao_oficial_required", request_id: authz.requestId }, 400);
      }

      const insertPayload = {
        cod_item: codItem,
        cod_produt: payload.cod_produt ? String(payload.cod_produt).trim() : null,
        descricao_oficial: descricaoOficial,
        aplicacao: payload.aplicacao ? String(payload.aplicacao).trim() : null,
        un: payload.un ? String(payload.un).trim() : null,
        valor_unitario: payload.valor_unitario === "" || payload.valor_unitario == null ? null : Number(payload.valor_unitario),
        curva: payload.curva ? String(payload.curva).trim() : null,
        modelos_aplicaveis: payload.modelos_aplicaveis ? String(payload.modelos_aplicaveis).trim() : null,
      };

      if (insertPayload.valor_unitario !== null && !Number.isFinite(insertPayload.valor_unitario)) {
        return json({ error: "valor_unitario_invalid", request_id: authz.requestId }, 400);
      }

      const authorization = req.headers.get("Authorization") ?? "";
      const userClient = createClient(
        SUPABASE_URL,
        Deno.env.get("SUPABASE_ANON_KEY")!,
        { global: { headers: { Authorization: authorization } } },
      );

      const { data: duplicate, error: duplicateError } = await userClient
        .from("lista_mae")
        .select("id")
        .eq("cod_item", codItem)
        .limit(1);

      if (duplicateError) {
        return json({ error: "duplicate_check_failed", request_id: authz.requestId }, 500);
      }
      if ((duplicate ?? []).length > 0) {
        return json({ error: "cod_item_already_exists", request_id: authz.requestId }, 409);
      }

      const { data, error } = await userClient
        .from("lista_mae")
        .insert(insertPayload)
        .select("*")
        .single();

      await supabase.from("elo_audit_log").insert({
        actor_type: "elo_control_plane",
        operation,
        entity_type: "lista_mae",
        entity_id: data?.id ?? null,
        request_summary: "Lista-Mãe INSERT " + codItem,
        status: error ? "error" : "success",
        metadata: {
          capability: authz.capability,
          request_id: authz.requestId,
          authorization_authority: "elo-authz",
          identity_id: authz.authorization.identity_id ?? null,
          session_id: authz.authorization.session_id ?? null,
          cod_item: codItem,
        },
      });

      if (error) return json({ error: "operation_failed", request_id: authz.requestId }, 500);
      return json({
        ok: true,
        operation,
        capability: authz.capability,
        authorization_authority: "elo-authz",
        request_id: authz.requestId,
        data,
      });
    }

    if (operation === "read") {
      const table = String(body.table ?? "");
      if (!READ_TABLES.has(table)) return json({ error: "table_not_allowed", request_id: authz.requestId }, 403);

      const limit = Math.min(Math.max(Number(body.limit ?? 100), 1), 500);
      const { data, error } = await supabase.from(table).select("*").limit(limit);
      const status = error ? "error" : "success";

      await supabase.from("elo_audit_log").insert({
        actor_type: "elo_control_plane",
        operation,
        entity_type: body.entity_type ?? null,
        entity_id: body.entity_id ?? null,
        request_summary: body.request_summary ?? null,
        status,
        metadata: {
          capability: authz.capability,
          table,
          request_id: authz.requestId,
          authorization_authority: "elo-authz",
          identity_id: authz.authorization.identity_id ?? null,
          session_id: authz.authorization.session_id ?? null,
        },
      });

      if (error) return json({ error: "operation_failed", request_id: authz.requestId }, 500);
      return json({ ok: true, operation, capability: authz.capability, authorization_authority: "elo-authz", request_id: authz.requestId, data });
    }

    return json({
      error: "operation_scaffold_only",
      message: "Write and schema operations are not executable by this gateway until their governed implementation is explicitly authorized.",
      capability: authz.capability,
      request_id: authz.requestId,
    }, 501);
  } catch (e) {
    return json({ error: "invalid_request", detail: String(e) }, 400);
  }
});
