import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);
const MCP_PROTOCOL_VERSION = "2025-06-18";
const RESOURCE_PATH = "/functions/v1/elo-mcp";
const RESOURCE_METADATA_PATH = "/functions/v1/elo-mcp/oauth-protected-resource";
const AUTHZ_PATH = "/functions/v1/elo-authz";

const ALLOWED_TABLES = new Set([
  "taxonomia", "dimensoes", "modelos", "modelo_apresentacao", "kits",
  "kit_itens", "lista_mae", "estrutura_modular", "estrutura_modular_itens",
]);

function json(data: unknown, status = 200, extra: Record<string, string> = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "authorization, content-type, mcp-session-id, mcp-protocol-version",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      ...extra,
    },
  });
}

function rpc(id: unknown, result: unknown) {
  return json({ jsonrpc: "2.0", id, result });
}

function rpcError(id: unknown, code: number, message: string) {
  return json({ jsonrpc: "2.0", id, error: { code, message } });
}

function protectedResourceMetadata(req: Request) {
  const origin = new URL(req.url).origin;
  return json({
    resource: `${origin}${RESOURCE_PATH}`,
    authorization_servers: [`${SUPABASE_URL}/auth/v1`],
    bearer_methods_supported: ["header"],
  });
}

async function authenticate(req: Request) {
  const header = req.headers.get("Authorization") ?? "";
  const token = header.startsWith("Bearer ") ? header.slice(7) : "";
  if (!token) return { ok: false as const, reason: "missing_bearer" };

  const { data, error } = await supabase.auth.getUser(token);
  if (error || !data.user) return { ok: false as const, reason: "invalid_token" };

  const authorization = await authorizeRead(req, token);
  if (!authorization.ok) return { ok: false as const, reason: authorization.reason, user: data.user };

  const { data: identity, error: identityError } = await supabase
    .from("elo_identity_registry")
    .select("identity_id,auth_user_id,provider,provider_subject,display_name,enterprise_context,active")
    .eq("auth_user_id", data.user.id)
    .eq("active", true)
    .maybeSingle();
  if (identityError) return { ok: false as const, reason: "identity_lookup_failed", user: data.user };
  if (!identity) return { ok: false as const, reason: "operator_binding_missing", user: data.user };

  return { ok: true as const, user: data.user, identity, authorization };
}

async function authorizeRead(req: Request, token: string) {
  const requestId = req.headers.get("x-elo-request-id")?.trim() || crypto.randomUUID();
  const response = await fetch(`${SUPABASE_URL}${AUTHZ_PATH}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
      "x-elo-request-id": requestId,
    },
    body: JSON.stringify({ action: "read", repository: "", capability: "READ" }),
  });

  let body: any = {};
  try { body = await response.json(); } catch { return { ok: false as const, reason: "authorization_invalid_response" }; }
  if (!response.ok || body?.authorized !== true) {
    return { ok: false as const, reason: String(body?.reason ?? "authorization_denied") };
  }
  return { ok: true as const, body };
}

async function audit(userId: string | null, operation: string, status: string, metadata: Record<string, unknown> = {}) {
  await supabase.from("elo_audit_log").insert({
    actor_type: "mcp_chatgpt",
    operation,
    status,
    request_summary: `MCP ${operation}`,
    metadata: { ...metadata, actor_user_id: userId },
  });
}

const TOOLS = [
  {
    name: "elo_status",
    title: "ELO status",
    description: "Returns authenticated ELO operator status and the read-only MCP boundary.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "elo_read",
    title: "Read ELO data",
    description: "Reads rows from an explicitly allowlisted ELO table. No writes or schema changes are exposed.",
    inputSchema: {
      type: "object",
      properties: {
        table: { type: "string", enum: [...ALLOWED_TABLES] },
        limit: { type: "integer", minimum: 1, maximum: 100 },
        orderBy: { type: "string" },
        ascending: { type: "boolean" },
      },
      required: ["table"],
      additionalProperties: false,
    },
  },
  {
    name: "elo_pcp_demanda_crossing_status",
    title: "Read PCP demand crossing",
    description: "Reads the governed PCP demand-crossing state. When historical and forecast demand data are ready, returns the exact pending question that ELO must ask before performing the crossing.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "elo_pcp_dados_pendentes",
    title: "Read PCP missing data requests",
    description: "Returns the canonical PCP data gaps that ELO must ask the user for through GPT. It never invents missing values and identifies the current gate, authorized source, exact fields and question.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "elo_pcp_decisao_externa_status",
    title: "Read PCP external decision cockpit",
    description: "Reads the governed PCP external decision cockpit, including summary indicators, impacts, analytical reasons, missing information and pending validation.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "elo_dol_read",
    title: "Read Decision Outcome Loop",
    description: "Reads Decision Outcome Loop records from the cognitive projection. Read-only and audited.",
    inputSchema: {
      type: "object",
      properties: {
        decision_id: { type: "string" },
        state: {
          type: "string",
          enum: [
            "proposed", "approved", "executed", "observing", "evaluated",
            "attributed", "learned", "closed", "escalated", "reverted",
          ],
        },
        limit: { type: "integer", minimum: 1, maximum: 100 },
      },
      additionalProperties: false,
    },
  },
  {
    name: "elo_calibration_read",
    title: "Read calibration model",
    description: "Reads the current confidence calibration model projection. Read-only and audited.",
    inputSchema: { type: "object", properties: {}, additionalProperties: false },
  },
  {
    name: "elo_precedent_search",
    title: "Search decision precedents",
    description: "Searches the decision precedent index projection. Read-only and audited.",
    inputSchema: {
      type: "object",
      properties: {
        sector: { type: "string" },
        decision_type: { type: "string" },
        confidence_band: { type: "string" },
        limit: { type: "integer", minimum: 1, maximum: 50 },
      },
      additionalProperties: false,
    },
  },
];

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "authorization, content-type, mcp-session-id, mcp-protocol-version, x-elo-request-id",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    }});
  }

  const pathname = new URL(req.url).pathname.replace(/\/$/, "");
  if (req.method === "GET" && pathname.endsWith(RESOURCE_METADATA_PATH)) {
    return protectedResourceMetadata(req);
  }

  if (req.method === "GET") {
    return json({
      name: "ELO MCP",
      version: "0.2.0",
      protocolVersion: MCP_PROTOCOL_VERSION,
      authentication: "Supabase Auth OAuth 2.1 / Bearer JWT",
      mode: "read-only",
      endpoint: `${SUPABASE_URL}${RESOURCE_PATH}`,
      oauthProtectedResourceMetadata: `${SUPABASE_URL}${RESOURCE_METADATA_PATH}`,
      tools: TOOLS.map((t) => t.name),
    });
  }

  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405);

  const auth = await authenticate(req);
  if (!auth.ok) {
    await audit(auth.user?.id ?? null, "authentication", "denied", { reason: auth.reason });
    if (auth.reason === "missing_bearer" || auth.reason === "invalid_token") {
      return json({ error: "unauthorized", reason: auth.reason }, 401, {
        "WWW-Authenticate": `Bearer realm="ELO MCP", resource_metadata="${new URL(RESOURCE_METADATA_PATH, new URL(req.url).origin).toString()}"`,
      });
    }
    return json({ error: "forbidden", reason: auth.reason }, 403);
  }

  let body: any;
  try { body = await req.json(); } catch { return json({ error: "invalid_json" }, 400); }
  if (body?.jsonrpc !== "2.0") return json({ error: "invalid_jsonrpc" }, 400);

  const id = body.id;
  const method = body.method;

  if (method === "initialize") {
    await audit(auth.user.id, "initialize", "success");
    return rpc(id, {
      protocolVersion: MCP_PROTOCOL_VERSION,
      capabilities: { tools: {} },
      serverInfo: { name: "ELO MCP", version: "0.2.0" },
      instructions: "ELO is available through an authenticated, read-only boundary. Authorization is delegated to elo-authz. Do not infer write authority from this connection. Cognitive projections (DOL, calibration, precedents) are exposed as read-only tools. When elo_pcp_demanda_crossing_status reports a pending PCP demand crossing, ask its next_question before calculating or presenting the crossing; do not apply the factor to the RH headcount. When elo_pcp_dados_pendentes returns blocking requests, ask the first next_question (or the request question in priority order) through GPT, identify the canonical source and required fields, and never invent or estimate the missing value. When elo_pcp_decisao_externa_status reports a pending PCP external decision validation, ask its next_question before presenting the consolidated decision cockpit; do not infer hiring, headcount, availability or capacity from the cockpit alone.",
    });
  }
  if (method === "notifications/initialized") return new Response(null, { status: 202 });
  if (method === "ping") return rpc(id, {});

  if (method === "tools/list") {
    await audit(auth.user.id, "tools/list", "success");
    return rpc(id, { tools: TOOLS });
  }

  if (method === "tools/call") {
    const name = body.params?.name;
    const args = body.params?.arguments ?? {};

    if (name === "elo_status") {
      await audit(auth.user.id, "elo_status", "success", { identity_id: auth.identity.identity_id });
      return rpc(id, { content: [{ type: "text", text: JSON.stringify({
        authenticated: true,
        roles: auth.authorization.body.roles ?? [],
        identity_id: auth.identity.identity_id,
        display_name: auth.identity.display_name,
        provider: auth.identity.provider,
        mode: "read-only",
        writes_enabled: false,
        schema_changes_enabled: false,
        authorization_authority: "elo-authz",
        tools_available: TOOLS.map((t) => t.name),
      }) }] });
    }

    if (name === "elo_read") {
      const table = String(args.table ?? "");
      if (!ALLOWED_TABLES.has(table)) {
        await audit(auth.user.id, "elo_read", "denied", { table, reason: "table_not_allowed" });
        return rpcError(id, -32001, "table_not_allowed");
      }
      const limit = Math.min(Math.max(Number(args.limit ?? 50), 1), 100);
      const orderBy = typeof args.orderBy === "string" && /^[A-Za-z_][A-Za-z0-9_]*$/.test(args.orderBy) ? args.orderBy : null;
      let query = supabase.from(table).select("*").limit(limit);
      if (orderBy) query = query.order(orderBy, { ascending: args.ascending !== false });
      const { data, error } = await query;
      if (error) {
        await audit(auth.user.id, "elo_read", "error", { table, error: error.message });
        return rpcError(id, -32002, "read_failed");
      }
      await audit(auth.user.id, "elo_read", "success", { table, row_count: data?.length ?? 0 });
      return rpc(id, { content: [{ type: "text", text: JSON.stringify({ table, count: data?.length ?? 0, rows: data ?? [] }) }] });
    }

    if (name === "elo_pcp_demanda_crossing_status") {
      const { data: pending, error: pendingError } = await supabase
        .from("elo_automation_runs")
        .select("id,automation_id,started_at,status,rows_affected,details,elo_automation_registry!inner(code,name,requires_validation)")
        .eq("status", "PENDING_INPUT")
        .eq("elo_automation_registry.code", "elo_pcp_demanda_crossing")
        .order("started_at", { ascending: true })
        .limit(1)
        .maybeSingle();

      if (pendingError) {
        await audit(auth.user.id, "elo_pcp_demanda_crossing_status", "error", { error: pendingError.message });
        return rpcError(id, -32003, "pcp_crossing_status_failed");
      }

      const { data: factors, error: factorError } = await supabase
        .from("v_elo_pcp_referencia_demanda_comparavel")
        .select("natureza_demanda,modelo_codigo,modelo_nome,taxonomia_tipo,chave_comparabilidade,quantidade_historica,quantidade_prevista,fator_demanda,variacao_percentual,estado_comparabilidade,estado_fator")
        .limit(100);

      const { data: projections, error: projectionError } = await supabase
        .from("v_elo_pcp_demanda_humana_projetada_externa")
        .select("natureza_demanda,modelo_codigo,modelo_nome,funcao_codigo,funcao_nome,demanda_humana_historica_media_dia,fator_demanda,demanda_humana_projetada_media_dia,estado_projecao")
        .limit(100);

      await audit(auth.user.id, "elo_pcp_demanda_crossing_status", "success", {
        pending: Boolean(pending),
        factor_rows: factors?.length ?? 0,
        projection_rows: projections?.length ?? 0,
        factor_error: factorError?.message ?? null,
        projection_error: projectionError?.message ?? null,
      });

      return rpc(id, { content: [{ type: "text", text: JSON.stringify({
        ready: Boolean(pending),
        pending_run: pending ?? null,
        next_question: pending?.details?.next_question ?? null,
        rule: pending?.details?.rule ?? "Nao aplicar o fator ao quadro de RH.",
        fator_rows: factors ?? [],
        demanda_humana_projetada: projections ?? [],
      }) }] });
    }

    if (name === "elo_pcp_dados_pendentes") {
      const { data, error } = await supabase
        .from("v_elo_pcp_dados_pendentes")
        .select("prioridade,codigo,tipo_solicitacao,gate,fonte_autorizada,pergunta_gpt,motivo,bloqueia_execucao,campos_obrigatorios,atualizado_em")
        .order("prioridade", { ascending: true })
        .limit(20);

      if (error) {
        await audit(auth.user.id, "elo_pcp_dados_pendentes", "error", { error: error.message });
        return rpcError(id, -32005, "pcp_missing_data_failed");
      }

      const bloqueios = (data ?? []).filter((item: any) => item.bloqueia_execucao === true);
      await audit(auth.user.id, "elo_pcp_dados_pendentes", "success", {
        request_count: data?.length ?? 0,
        blocking_count: bloqueios.length,
      });

      return rpc(id, { content: [{ type: "text", text: JSON.stringify({
        action: data?.length ? "ASK_USER_FOR_DATA" : "NO_DATA_REQUEST_PENDING",
        must_not_infer: true,
        requests: data ?? [],
        next_question: data?.[0]?.pergunta_gpt ?? null,
        rule: "Quando houver solicitacao bloqueante, o ELO deve pedir o dado indicado ao usuario antes de calcular, recomendar ou preencher por inferencia.",
      }) }] });
    }

    if (name === "elo_pcp_decisao_externa_status") {
      const { data: pending, error: pendingError } = await supabase
        .from("elo_automation_runs")
        .select("id,automation_id,started_at,status,rows_affected,details,elo_automation_registry!inner(code,name,requires_validation)")
        .eq("status", "PENDING_INPUT")
        .eq("elo_automation_registry.code", "elo_pcp_decisao_externa")
        .order("started_at", { ascending: true })
        .limit(1)
        .maybeSingle();

      if (pendingError) {
        await audit(auth.user.id, "elo_pcp_decisao_externa_status", "error", { error: pendingError.message });
        return rpcError(id, -32004, "pcp_decisao_externa_status_failed");
      }

      const { data: summary, error: summaryError } = await supabase
        .from("v_elo_pcp_decisao_externa_resumo")
        .select("*")
        .limit(1)
        .maybeSingle();

      const { data: details, error: detailsError } = await supabase
        .from("v_elo_pcp_decisao_externa_detalhe")
        .select("*")
        .limit(200);

      await audit(auth.user.id, "elo_pcp_decisao_externa_status", "success", {
        pending: Boolean(pending),
        summary_available: Boolean(summary),
        detail_rows: details?.length ?? 0,
        summary_error: summaryError?.message ?? null,
        details_error: detailsError?.message ?? null,
      });

      return rpc(id, { content: [{ type: "text", text: JSON.stringify({
        ready: Boolean(pending),
        pending_run: pending ?? null,
        next_question: pending?.details?.next_question ?? null,
        rule: pending?.details?.rule ?? "A camada e analitica; nao inferir contratacao ou quadro de RH sem produtividade, composicao e validacao.",
        resumo: summary ?? null,
        detalhes: details ?? [],
        erros_leitura: {
          resumo: summaryError?.message ?? null,
          detalhes: detailsError?.message ?? null,
        },
      }) }] });
    }

    if (name === "elo_dol_read") {
      const decisionId = typeof args.decision_id === "string" ? args.decision_id : null;
      const state = typeof args.state === "string" ? args.state : null;
      const limit = Math.min(Math.max(Number(args.limit ?? 20), 1), 100);

      let query = supabase.from("elo_dol_projection").select("*").limit(limit);
      if (decisionId) query = query.eq("decision_id", decisionId);
      if (state) query = query.eq("state", state);

      const { data, error } = await query;
      if (error) {
        await audit(auth.user.id, "elo_dol_read", "error", { decision_id: decisionId, state, error: error.message });
        return rpc(id, { content: [{ type: "text", text: JSON.stringify({
          decision_id: decisionId,
          state,
          count: 0,
          records: [],
          note: "DOL projection not available. Canonical source: memory/ in the repository.",
        }) }] });
      }
      await audit(auth.user.id, "elo_dol_read", "success", { decision_id: decisionId, state, row_count: data?.length ?? 0 });
      return rpc(id, { content: [{ type: "text", text: JSON.stringify({
        decision_id: decisionId,
        state,
        count: data?.length ?? 0,
        records: data ?? [],
      }) }] });
    }

    if (name === "elo_calibration_read") {
      const { data, error } = await supabase
        .from("elo_calibration_model")
        .select("*")
        .limit(1)
        .maybeSingle();
      if (error) {
        await audit(auth.user.id, "elo_calibration_read", "error", { error: error.message });
        return rpc(id, { content: [{ type: "text", text: JSON.stringify({
          count: 0,
          model: null,
          note: "Calibration model projection not available. Canonical source: memory/calibration/ in the repository.",
        }) }] });
      }
      await audit(auth.user.id, "elo_calibration_read", "success");
      return rpc(id, { content: [{ type: "text", text: JSON.stringify({ count: data ? 1 : 0, model: data ?? null }) }] });
    }

    if (name === "elo_precedent_search") {
      const sector = typeof args.sector === "string" ? args.sector : null;
      const decisionType = typeof args.decision_type === "string" ? args.decision_type : null;
      const confidenceBand = typeof args.confidence_band === "string" ? args.confidence_band : null;
      const limit = Math.min(Math.max(Number(args.limit ?? 10), 1), 50);

      let query = supabase.from("elo_precedent_index").select("*").limit(limit);
      if (sector) query = query.eq("sector", sector);
      if (decisionType) query = query.eq("decision_type", decisionType);
      if (confidenceBand) query = query.eq("confidence_band", confidenceBand);

      const { data, error } = await query;
      if (error) {
        await audit(auth.user.id, "elo_precedent_search", "error", { sector, decision_type: decisionType, error: error.message });
        return rpc(id, { content: [{ type: "text", text: JSON.stringify({
          count: 0,
          precedents: [],
          note: "Precedent index projection not available. Canonical source: memory/precedents/ in the repository.",
        }) }] });
      }
      await audit(auth.user.id, "elo_precedent_search", "success", { sector, decision_type: decisionType, confidence_band: confidenceBand, row_count: data?.length ?? 0 });
      return rpc(id, { content: [{ type: "text", text: JSON.stringify({
        count: data?.length ?? 0,
        precedents: data ?? [],
      }) }] });
    }

    return rpcError(id, -32601, `Unknown tool: ${String(name)}`);
  }

  return rpcError(id, -32601, `Method not found: ${String(method)}`);
});