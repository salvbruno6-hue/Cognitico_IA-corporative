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
    name: "elo_pcp_comunicacao_melhoria",
    title: "Create ELO communication and improvement points",
    description: "Builds a governed communication from current PCP gaps/evidence and identifies missing inputs, process points to insert, and points to improve. Communication is autonomous at the GPT channel; facts, rules and operational data are never invented or changed.",
    inputSchema: {
      type: "object",
      properties: {
        contexto: { type: "string", description: "Optional context or audience for the communication." },
      },
      additionalProperties: false,
    },
  },
  {
    name: "elo_pcp_orquestrador_dialogo",
    title: "Orchestrate PCP data collection dialogue",
    description: "Runs the governed PCP collection dialogue one step at a time. It reads the first blocking gap, records the user's response, validates explicitly supplied fields without inference, and returns the next question or a validated handoff. It does not change canonical operational data.",
    inputSchema: {
      type: "object",
      properties: {
        sessao_id: { type: "string", description: "Optional UUID for the dialogue session. A new session is created when omitted." },
        resposta: { type: "string", description: "The user's latest answer, preserved verbatim for traceability." },
        dados_fornecidos: { type: "object", description: "Structured fields explicitly supplied by the user in the latest answer. Missing fields must be omitted, never guessed." },
        fonte_informada: { type: "string", description: "The source named by the user for the supplied data, if any." }
      },
      additionalProperties: false,
    },
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
    name: "elo_pcp_indicadores_status",
    title: "Read governed PCP indicators and formal KPI state",
    description: "Reads capacity and external-operation indicators only after their sources are enabled in the canonical catalog, and reports whether a formal KPI definition/snapshot exists. Indicators are never promoted automatically to KPI.",
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
      instructions: "ELO is available through an authenticated, read-only boundary. Authorization is delegated to elo-authz. Do not infer write authority from this connection. Cognitive projections (DOL, calibration, precedents) are exposed as read-only tools. When elo_pcp_demanda_crossing_status reports a pending PCP demand crossing, ask its next_question before calculating or presenting the crossing; do not apply the factor to the RH headcount. When elo_pcp_dados_pendentes returns blocking requests, ask the first next_question (or the request question in priority order) through GPT, identify the canonical source and required fields, and never invent or estimate the missing value. Use elo_pcp_orquestrador_dialogo to persist each turn, validate explicitly supplied fields, explain missing fields one at a time, and continue until the current gap is closed or the source is unresolved. The ELO is also authorized to autonomously create a communication and point out missing inputs, process items that should be inserted, and improvement points. It does not need a separate approval to communicate a governed gap; it must not alter canonical data/rules or execute a blocked decision. When elo_pcp_decisao_externa_status reports a pending PCP external decision validation, ask its next_question before presenting the consolidated decision cockpit; do not infer hiring, headcount, availability or capacity from the cockpit alone. Use elo_pcp_indicadores_status for governed capacity/external-operation indicators and formal KPI registry state; when it reports BLOQUEADO_CATALOGO or SEM_KPI_FORMAL_REGISTRADO, do not invent, promote or label an indicator as a KPI.",
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

    if (name === "elo_pcp_comunicacao_melhoria") {
      const { data, error } = await supabase
        .from("v_elo_pcp_dados_pendentes")
        .select("prioridade,codigo,gate,fonte_autorizada,pergunta_gpt,motivo,bloqueia_execucao,campos_obrigatorios")
        .order("prioridade", { ascending: true })
        .limit(20);

      if (error) {
        await audit(auth.user.id, "elo_pcp_comunicacao_melhoria", "error", { error: error.message });
        return rpcError(id, -32006, "pcp_communication_failed");
      }

      const requests = data ?? [];
      const contexto = typeof args.contexto === "string" ? args.contexto.trim() : "";
      const primeiro = requests[0] ?? null;
      const comunicado = primeiro
        ? [
            "COMUNICADO ELO — PONTO DE ATENÇÃO PCP",
            contexto ? `Contexto: ${contexto}` : null,
            "",
            `Situação: o gate "${primeiro.gate}" está bloqueado por ausência/validação de dado.`,
            `Dado necessário: ${primeiro.codigo}.`,
            `Fonte autorizada: ${primeiro.fonte_autorizada}.`,
            `Ação solicitada: ${primeiro.pergunta_gpt}`,
            `Motivo: ${primeiro.motivo}`,
            "",
            "O cálculo/decisão permanece bloqueado até a informação ser fornecida e validada.",
          ].filter(Boolean).join("\n")
        : "COMUNICADO ELO — Não há solicitação bloqueante de dados neste momento.";

      const pontos = requests.map((r: any) => ({
        tipo: "INSERIR_OU_MELHORAR",
        prioridade: r.prioridade,
        gate: r.gate,
        ponto: r.codigo,
        acao: r.pergunta_gpt,
        fonte: r.fonte_autorizada,
        motivo: r.motivo,
      }));

      await audit(auth.user.id, "elo_pcp_comunicacao_melhoria", "success", {
        blocking_count: requests.filter((r: any) => r.bloqueia_execucao).length,
        point_count: pontos.length,
      });

      return rpc(id, { content: [{ type: "text", text: JSON.stringify({
        autonomia: {
          criar_comunicado: true,
          apontar_pontos_faltantes: true,
          apontar_melhorias: true,
          alterar_dados: false,
          alterar_regras_canonicas: false,
          executar_decisao_bloqueada: false,
        },
        comunicado,
        pontos_melhorar_inserir: pontos,
        regra: "O ELO pode comunicar e apontar autonomamente; qualquer alteração de dado, regra canônica ou execução bloqueada segue a governança correspondente.",
      }) }] });
    }

    if (name === "elo_pcp_orquestrador_dialogo") {
      const suppliedSessionId = typeof args.sessao_id === "string" && /^[0-9a-fA-F-]{36}$/.test(args.sessao_id)
        ? args.sessao_id
        : null;
      const sessionId = suppliedSessionId ?? crypto.randomUUID();
      const resposta = typeof args.resposta === "string" ? args.resposta : "";
      const dados = args.dados_fornecidos && typeof args.dados_fornecidos === "object" && !Array.isArray(args.dados_fornecidos)
        ? args.dados_fornecidos
        : {};
      const fonte = typeof args.fonte_informada === "string" ? args.fonte_informada.trim() : null;

      const { data: requests, error: requestError } = await supabase
        .from("v_elo_pcp_dados_pendentes")
        .select("prioridade,codigo,tipo_solicitacao,gate,fonte_autorizada,pergunta_gpt,motivo,bloqueia_execucao,campos_obrigatorios")
        .order("prioridade", { ascending: true })
        .limit(20);

      if (requestError) {
        await audit(auth.user.id, "elo_pcp_orquestrador_dialogo", "error", { error: requestError.message });
        return rpcError(id, -32007, "pcp_dialogue_rules_failed");
      }

      const primeiro = requests?.[0] ?? null;

      if (!primeiro) {
        await audit(auth.user.id, "elo_pcp_orquestrador_dialogo", "success", { session_id: sessionId, state: "CICLO_SEM_GAP_PENDENTE" });
        return rpc(id, { content: [{ type: "text", text: JSON.stringify({
          sessao_id: sessionId,
          estado: "CICLO_SEM_GAP_PENDENTE",
          mensagem: "Não há GAP bloqueante pendente no PCP neste momento. O orquestrador não deve criar uma nova solicitação por conta própria.",
          proxima_pergunta: null,
          pode_calcular: true,
          regra: "A ausência de GAP nesta fila não substitui os gates de validação do processo canônico.",
        }) }] });
      }

      const required = Array.isArray(primeiro.campos_obrigatorios) ? primeiro.campos_obrigatorios.map(String) : [];
      const providedKeys = Object.keys(dados);
      const missing = required.filter((field: string) => {
        const value = (dados as any)[field];
        return value === undefined || value === null || (typeof value === "string" && value.trim() === "");
      });
      const validProvided = required.filter((field: string) => {
        const value = (dados as any)[field];
        return value !== undefined && value !== null && !(typeof value === "string" && value.trim() === "");
      });

      const outsideFields = providedKeys.filter((field: string) => !required.includes(field));
      const hasResponse = resposta.trim().length > 0 || Object.keys(dados).length > 0 || Boolean(fonte);

      let state = "PENDENTE";
      let message = primeiro.pergunta_gpt;
      let nextQuestion = primeiro.pergunta_gpt;
      const semanticErrors: string[] = [];

      if (primeiro.codigo === "HISTORICO_COMPARAVEL" && hasResponse) {
        const inicio = typeof (dados as any).periodo_inicio === "string" ? String((dados as any).periodo_inicio) : "";
        const fim = typeof (dados as any).periodo_fim === "string" ? String((dados as any).periodo_fim) : "";
        const quantidade = Number((dados as any).quantidade_real);
        const semChave = (dados as any).sem_chave_comparabilidade === true;

        if (inicio && !/^\d{4}-\d{2}-\d{2}$/.test(inicio)) semanticErrors.push("periodo_inicio deve estar no formato AAAA-MM-DD.");
        if (fim && !/^\d{4}-\d{2}-\d{2}$/.test(fim)) semanticErrors.push("periodo_fim deve estar no formato AAAA-MM-DD.");
        if (inicio && /^\d{4}-\d{2}-\d{2}$/.test(inicio) && inicio < "2025-09-01") semanticErrors.push("periodo_inicio está antes do horizonte histórico autorizado.");
        if (fim && /^\d{4}-\d{2}-\d{2}$/.test(fim) && fim > "2026-02-28") semanticErrors.push("periodo_fim está depois do horizonte histórico autorizado.");
        if (inicio && fim && /^\d{4}-\d{2}-\d{2}$/.test(inicio) && /^\d{4}-\d{2}-\d{2}$/.test(fim) && inicio > fim) semanticErrors.push("periodo_inicio não pode ser posterior ao periodo_fim.");
        if (Number.isNaN(quantidade) || quantidade < 0) semanticErrors.push("quantidade_real deve ser um número maior ou igual a zero.");
        if (!String((dados as any).natureza_demanda ?? "").trim()) semanticErrors.push("natureza_demanda precisa ser informada conforme a fonte oficial.");
        if (!String((dados as any).chave_comparabilidade ?? "").trim() && !semChave) semanticErrors.push("chave_comparabilidade precisa ser informada ou o usuário deve declarar explicitamente que não existe correspondência comparável.");
        if (semChave && String((dados as any).chave_comparabilidade ?? "").trim()) semanticErrors.push("Não informe chave e sem_chave_comparabilidade ao mesmo tempo; escolha a condição real.");
        if (String((dados as any).modelo_id ?? "").trim()) {
          const { data: modelo, error: modeloError } = await supabase
            .from("modelos")
            .select("id,codigo,nome,ativo")
            .eq("id", String((dados as any).modelo_id))
            .maybeSingle();
          if (modeloError || !modelo) semanticErrors.push("modelo_id não foi localizado no cadastro oficial de modelos.");
          else if (modelo.ativo !== true) semanticErrors.push("modelo_id localizado, mas o modelo não está ativo no cadastro oficial.");
        }
      }

      if (hasResponse) {
        const validSource = !fonte || fonte === primeiro.fonte_autorizada;
        const sourceIssue = fonte && !validSource
          ? `A fonte informada "${fonte}" não corresponde à fonte autorizada "${primeiro.fonte_autorizada}". Não vou substituir a fonte autorizada por inferência.`
          : null;

        if (missing.length === 0 && validSource && semanticErrors.length === 0) {
          state = "VALIDADO";
          message = `Recebi os campos necessários para o GAP "${primeiro.codigo}" e a validação estrutural passou. Isso ainda não grava o dado na tabela operacional: a resposta permanece registrada no diálogo até a confirmação da fonte e da autoridade de gravação.`;
          nextQuestion = `Confirme a fonte oficial "${primeiro.fonte_autorizada}" e, se houver mais registros históricos, envie o próximo registro. Se este for o último registro, informe "último registro" para o orquestrador iniciar o fechamento do conjunto.`;
        } else {
          state = "PENDENTE";
          const missingText = missing.length ? `Ainda faltam: ${missing.join(", ")}.` : "";
          const semanticText = semanticErrors.length ? `Também encontrei: ${semanticErrors.join(" ")}` : "";
          message = [
            "Recebi sua resposta, mas o GAP ainda não pode ser fechado.",
            sourceIssue,
            missingText,
            semanticText,
            outsideFields.length ? `Também recebi campos que não pertencem ao pedido atual: ${outsideFields.join(", ")}. Não vou usá-los neste gate.` : null,
          ].filter(Boolean).join(" ");
          nextQuestion = missing.length
            ? `Vamos completar somente o que falta. ${missing.map((field: string) => {
                const labels: Record<string,string> = {
                  modelo_id: "qual é o modelo/produto identificado no cadastro oficial?",
                  periodo_inicio: "qual é a data inicial do registro?",
                  periodo_fim: "qual é a data final do registro?",
                  quantidade_real: "qual é a quantidade real registrada?",
                  natureza_demanda: "qual é a natureza da demanda conforme o cadastro/relatório oficial?",
                  chave_comparabilidade: "qual é a chave de comparabilidade? Se não existir porque a demanda não é comparável, declare explicitamente que não existe correspondência comparável.",
                };
                return labels[field] ? `${field}: ${labels[field]}` : field;
              }).join(" ")}`
            : (semanticErrors.length ? semanticErrors.join(" ") : (sourceIssue ?? nextQuestion));
        }

        const { data: lastTurn, error: lastTurnError } = await supabase
          .schema("elo_private")
          .from("pcp_dialogo_turnos")
          .select("turno")
          .eq("sessao_id", sessionId)
          .order("turno", { ascending: false })
          .limit(1)
          .maybeSingle();

        if (lastTurnError) {
          await audit(auth.user.id, "elo_pcp_orquestrador_dialogo", "error", { session_id: sessionId, error: lastTurnError.message });
          return rpcError(id, -32008, "pcp_dialogue_state_read_failed");
        }

        const turno = Number(lastTurn?.turno ?? 0) + 1;
        const { error: turnError } = await supabase
          .schema("elo_private")
          .from("pcp_dialogo_turnos")
          .insert({
            sessao_id: sessionId,
            turno,
            actor_user_id: auth.user.id,
            gap_codigo: primeiro.codigo,
            gate: primeiro.gate,
            resposta_original: resposta || null,
            dados_fornecidos: dados,
            fonte_informada: fonte,
            estado: state,
            campos_validos: validProvided,
            campos_faltantes: missing,
            mensagem_orquestrador: message,
          });

        if (turnError) {
          await audit(auth.user.id, "elo_pcp_orquestrador_dialogo", "error", { session_id: sessionId, error: turnError.message });
          return rpcError(id, -32008, "pcp_dialogue_state_write_failed");
        }
      }

      await audit(auth.user.id, "elo_pcp_orquestrador_dialogo", "success", {
        session_id: sessionId,
        gap: primeiro.codigo,
        state,
        missing_fields: missing,
      });

      return rpc(id, { content: [{ type: "text", text: JSON.stringify({
        sessao_id: sessionId,
        estado: state,
        gap_atual: {
          codigo: primeiro.codigo,
          gate: primeiro.gate,
          fonte_autorizada: primeiro.fonte_autorizada,
          bloqueia_execucao: primeiro.bloqueia_execucao,
        },
        resposta_registrada: hasResponse,
        campos_validos: validProvided,
        campos_faltantes: missing,
        mensagem: message,
        proxima_pergunta: nextQuestion,
        deve_perguntar_antes_de_calcular: primeiro.bloqueia_execucao === true,
        pode_alterar_dado_canonico: false,
        regra: "O orquestrador conduz, explica, registra e valida explicitamente fornecimentos; não inventa valores, não altera regras canônicas e não libera cálculo bloqueado.",
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

    if (name === "elo_pcp_indicadores_status") {
      const requiredSources = [
        "v_elo_pcp_carga_capacidade_periodo",
        "v_elo_pcp_indicadores_montagem_externa",
        "mt_definicoes_kpi",
        "mt_snapshots_kpi",
      ];

      const { data: catalogRows, error: catalogError } = await supabase
        .from("elo_aprendizado_fontes")
        .select("table_name,dominio_codigo,regra_extracao,enabled,extracao_ativa")
        .in("table_name", requiredSources)
        .eq("enabled", true)
        .eq("extracao_ativa", true);

      if (catalogError) {
        await audit(auth.user.id, "elo_pcp_indicadores_status", "error", { error: catalogError.message });
        return rpcError(id, -32009, "pcp_indicator_catalog_read_failed");
      }

      const governed = new Set((catalogRows ?? []).map((row: any) => String(row.table_name)));
      const missingSources = requiredSources.filter((table) => !governed.has(table));
      if (missingSources.length) {
        await audit(auth.user.id, "elo_pcp_indicadores_status", "success", {
          state: "BLOQUEADO_CATALOGO",
          missing_sources: missingSources,
        });
        return rpc(id, { content: [{ type: "text", text: JSON.stringify({
          state: "BLOQUEADO_CATALOGO",
          read_only: true,
          automatic_kpi_promotion: false,
          catalog_authority: "elo_aprendizado_fontes",
          missing_sources: missingSources,
          rule: "A tool nao le indicadores ou registros de KPI fora do catalogo governado. Aplicar primeiro a migration canonica e validar as fontes.",
        }) }] });
      }

      const { data: capacity, error: capacityError } = await supabase
        .from("v_elo_pcp_carga_capacidade_periodo")
        .select("data_referencia,centro_trabalho_id,centro_trabalho_codigo,centro_trabalho_nome,unidade_capacidade,quantidade_planejada,carga_horas_planejada,capacidade_disponivel,capacidade_padrao,capacidade_recuperacao,capacidade_bloqueada,folga_horas,utilizacao_pct,excesso_carga")
        .limit(200);

      const { data: external, error: externalError } = await supabase
        .from("v_elo_pcp_indicadores_montagem_externa")
        .select("ordens_total,ordens_abertas,ordens_atrasadas,modulos_total,colaboradores_alocados,funcoes_ativas,horas_planejadas_ordens,horas_realizadas_ordens,horas_planejadas_equipe,horas_mao_obra_realizadas,aderencia_horas_pct")
        .limit(1)
        .maybeSingle();

      const { data: definitions, error: definitionsError } = await supabase
        .from("mt_definicoes_kpi")
        .select("id,codigo_kpi,nome,dominio,unidade,formula,ativo")
        .limit(100);

      const { data: snapshots, error: snapshotsError } = await supabase
        .from("mt_snapshots_kpi")
        .select("id,kpi_id,data_referencia,valor,numerador,denominador,contexto,calculado_em")
        .order("data_referencia", { ascending: false })
        .limit(100);

      const capacityState = capacityError
        ? "INDETERMINADO"
        : (capacity?.length ?? 0) > 0 ? "OBSERVADO" : "SEM_DADO_OPERACIONAL";

      const externalNumericFields = [
        "ordens_total", "ordens_abertas", "ordens_atrasadas", "modulos_total",
        "colaboradores_alocados", "funcoes_ativas", "horas_planejadas_ordens",
        "horas_realizadas_ordens", "horas_planejadas_equipe", "horas_mao_obra_realizadas",
      ];
      const hasExternalActivity = external
        ? externalNumericFields.some((field) => Number((external as any)[field] ?? 0) !== 0)
        : false;
      const externalState = externalError
        ? "INDETERMINADO"
        : !external ? "SEM_DADO_OPERACIONAL"
        : hasExternalActivity || external.aderencia_horas_pct !== null
          ? "OBSERVADO"
          : "SEM_ATIVIDADE_OPERACIONAL";

      const formalKpiState = definitionsError
        ? "INDETERMINADO"
        : (definitions?.length ?? 0) > 0
          ? "KPI_FORMAL_REGISTRADO"
          : "SEM_KPI_FORMAL_REGISTRADO";

      await audit(auth.user.id, "elo_pcp_indicadores_status", "success", {
        state: "CONSULTED",
        capacity_state: capacityState,
        capacity_rows: capacity?.length ?? 0,
        external_state: externalState,
        kpi_state: formalKpiState,
        kpi_definitions: definitions?.length ?? 0,
        kpi_snapshots: snapshots?.length ?? 0,
        read_errors: {
          capacity: capacityError?.message ?? null,
          external: externalError?.message ?? null,
          definitions: definitionsError?.message ?? null,
          snapshots: snapshotsError?.message ?? null,
        },
      });

      return rpc(id, { content: [{ type: "text", text: JSON.stringify({
        state: "CONSULTED",
        read_only: true,
        catalog_authority: "elo_aprendizado_fontes",
        automatic_kpi_promotion: false,
        indicadores: {
          capacidade: {
            source_table: "v_elo_pcp_carga_capacidade_periodo",
            state: capacityState,
            rows: capacity ?? [],
          },
          montagem_externa: {
            source_table: "v_elo_pcp_indicadores_montagem_externa",
            state: externalState,
            row: external ?? null,
          },
        },
        kpi_formal: {
          definition_source: "mt_definicoes_kpi",
          snapshot_source: "mt_snapshots_kpi",
          state: formalKpiState,
          definitions: definitions ?? [],
          snapshots: snapshots ?? [],
        },
        read_errors: {
          capacity: capacityError?.message ?? null,
          external: externalError?.message ?? null,
          definitions: definitionsError?.message ?? null,
          snapshots: snapshotsError?.message ?? null,
        },
        rule: "Indicadores permanecem indicadores. Somente uma definicao existente em mt_definicoes_kpi autoriza classifica-los como KPI formal; ausencia de dado nao e convertida em zero.",
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