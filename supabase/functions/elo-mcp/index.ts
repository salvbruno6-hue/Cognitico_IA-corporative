import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);
const MCP_PROTOCOL_VERSION = "2025-06-18";
const RESOURCE_PATH = "/functions/v1/elo-mcp";
const RESOURCE_METADATA_PATH = "/functions/v1/elo-mcp/oauth-protected-resource";

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

  const { data: identity, error: identityError } = await supabase
    .from("elo_identity_registry")
    .select("identity_id,auth_user_id,provider,provider_subject,display_name,enterprise_context,active")
    .eq("auth_user_id", data.user.id)
    .eq("active", true)
    .maybeSingle();
  if (identityError) return { ok: false as const, reason: "identity_lookup_failed", user: data.user };
  if (!identity) return { ok: false as const, reason: "operator_binding_missing", user: data.user };

  const { data: roleRows, error: roleError } = await supabase
    .from("elo_identity_roles")
    .select("role_id,elo_roles(code,active)")
    .eq("identity_id", identity.identity_id);
  if (roleError) return { ok: false as const, reason: "role_lookup_failed", user: data.user };

  const isAdmin = (roleRows ?? []).some((row: any) =>
    row.elo_roles?.code === "ELO_ADMIN" && row.elo_roles?.active === true
  );
  if (!isAdmin) return { ok: false as const, reason: "elo_admin_required", user: data.user, identity };

  return { ok: true as const, user: data.user, identity };
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
];

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "authorization, content-type, mcp-session-id, mcp-protocol-version",
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
      version: "0.1.0",
      protocolVersion: MCP_PROTOCOL_VERSION,
      authentication: "Supabase Auth OAuth 2.1 / Bearer JWT",
      mode: "read-only",
      endpoint: `${SUPABASE_URL}${RESOURCE_PATH}`,
      oauthProtectedResourceMetadata: `${SUPABASE_URL}${RESOURCE_METADATA_PATH}`,
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
      serverInfo: { name: "ELO MCP", version: "0.1.0" },
      instructions: "ELO is available through an authenticated, read-only boundary. Do not infer write authority from this connection.",
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
        role: "ELO_ADMIN",
        identity_id: auth.identity.identity_id,
        display_name: auth.identity.display_name,
        provider: auth.identity.provider,
        mode: "read-only",
        writes_enabled: false,
        schema_changes_enabled: false,
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
    return rpcError(id, -32601, `Unknown tool: ${String(name)}`);
  }

  return rpcError(id, -32601, `Method not found: ${String(method)}`);
});