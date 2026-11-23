import { test } from "node:test";
import assert from "node:assert/strict";
import {
  createEloMcpToolInvoker,
  isPcpPlanningDomain,
  processGovernedPcpMission,
  unverifiedDomainResult,
} from "../src/lib/elo-pcp-governed-response.ts";

function invoker(fixtures, calls) {
  return async (name) => {
    calls.push(name);
    if (fixtures[name] instanceof Error) throw fixtures[name];
    return fixtures[name] ?? {};
  };
}

test("PCP blocking gaps return exact bounded admin questions and stop further reads", async () => {
  const calls = [];
  const requests = Array.from({ length: 7 }, (_, index) => ({
    prioridade: index + 1,
    codigo: `GAP-${index + 1}`,
    gate: "PCP",
    fonte_autorizada: "registro operacional",
    pergunta_gpt: `Pergunta governada ${index + 1}?`,
    motivo: `Motivo ${index + 1}`,
    bloqueia_execucao: true,
    campos_obrigatorios: ["valor"],
  }));
  const result = await processGovernedPcpMission({
    message: "planeje a produção",
    invokeTool: invoker({ elo_pcp_dados_pendentes: { requests } }, calls),
  });

  assert.deepEqual(calls, ["elo_pcp_dados_pendentes"]);
  assert.equal(result.response.status, "PARTIAL_SUPPORTED");
  assert.equal(result.suggestions.length, 5);
  assert.equal(result.suggestions[0].label, "Pergunta governada 1?");
  assert.equal(result.suggestions[0].payload.answer_contract, "HUMAN_EVIDENCE_CANDIDATE");
  assert.equal(result.suggestions[0].payload.canonical_mutation, false);
  assert.equal(result.metadata.must_not_infer, true);
  assert.equal(result.confidence, 0);
});

test("indicator intent consults indicators only after no blocking PCP gap", async () => {
  const calls = [];
  const result = await processGovernedPcpMission({
    message: "qual a capacidade e o KPI?",
    invokeTool: invoker({
      elo_pcp_dados_pendentes: { requests: [] },
      elo_pcp_indicadores_status: {
        state: "CONSULTED",
        indicadores: {
          capacidade: { source_table: "capacidade_view", state: "OBSERVADO", rows: [{ a: 1 }] },
          montagem_externa: { source_table: "externa_view", state: "SEM_DADO_OPERACIONAL", row: null },
        },
        kpi_formal: {
          definition_source: "kpi_def",
          snapshot_source: "kpi_snap",
          state: "SEM_KPI_FORMAL_REGISTRADO",
          definitions: [],
          snapshots: [],
        },
      },
    }, calls),
  });

  assert.deepEqual(calls, ["elo_pcp_dados_pendentes", "elo_pcp_indicadores_status"]);
  assert.equal(result.response.type, "pcp_indicators");
  assert.match(String(result.response.content), /Capacidade: OBSERVADO/);
  assert.equal(result.response.kpi_definition_count, 0);
  assert.equal(result.metadata.automatic_kpi_promotion, false);
});

test("general PCP intent consults governed decision cockpit after gap gate", async () => {
  const calls = [];
  const result = await processGovernedPcpMission({
    message: "qual o estado da decisão?",
    invokeTool: invoker({
      elo_pcp_dados_pendentes: { requests: [] },
      elo_pcp_decisao_externa_status: {
        resumo: { estado: "EM_ANALISE" },
        detalhes: [{ id: 1 }, { id: 2 }],
        next_question: null,
      },
    }, calls),
  });

  assert.deepEqual(calls, ["elo_pcp_dados_pendentes", "elo_pcp_decisao_externa_status"]);
  assert.equal(result.response.type, "pcp_decision_status");
  assert.deepEqual(result.response.summary, { estado: "EM_ANALISE" });
  assert.equal(result.response.detail_count, 2);
  assert.notEqual(result.validationStatus, "validated");
});

test("pending external PCP validation becomes one exact admin question", async () => {
  const calls = [];
  const result = await processGovernedPcpMission({
    message: "posso concluir a decisão?",
    invokeTool: invoker({
      elo_pcp_dados_pendentes: { requests: [] },
      elo_pcp_decisao_externa_status: { next_question: "Confirme a produtividade observada." },
    }, calls),
  });

  assert.equal(result.suggestions.length, 1);
  assert.equal(result.suggestions[0].label, "Confirme a produtividade observada.");
  assert.equal(result.suggestions[0].requires_approval, true);
  assert.equal(result.validationStatus, "PARTIAL_SUPPORTED");
});

test("MCP failure is fail-closed and never validates or echoes the user request", async () => {
  const calls = [];
  const message = "inventar uma capacidade";
  const result = await processGovernedPcpMission({
    message,
    invokeTool: invoker({ elo_pcp_dados_pendentes: new Error("denied") }, calls),
  });

  assert.equal(result.confidence, 0);
  assert.equal(result.validationStatus, "UNVERIFIED");
  assert.equal(result.policyDecision, "EVIDENCE_UNAVAILABLE");
  assert.notEqual(result.response.content, message);
});

test("non-connected domains are explicitly unverified", () => {
  const result = unverifiedDomainResult("comercial");
  assert.equal(result.confidence, 0);
  assert.equal(result.validationStatus, "UNVERIFIED");
  assert.equal(result.policyDecision, "NEEDS_GOVERNED_EVIDENCE");
});

test("planning domain aliases resolve only to the bounded PCP lane", () => {
  assert.equal(isPcpPlanningDomain("planejamento"), true);
  assert.equal(isPcpPlanningDomain("PCP"), true);
  assert.equal(isPcpPlanningDomain("planning"), true);
  assert.equal(isPcpPlanningDomain("comercial"), false);
});

test("MCP invoker keeps bearer in request header and returns structured evidence", async () => {
  let captured;
  const invoke = createEloMcpToolInvoker({
    baseUrl: "https://example.supabase.co",
    accessToken: "secret-user-bearer",
    requestId: "req-1",
    fetchImpl: async (url, init) => {
      captured = { url, init };
      return new Response(JSON.stringify({
        jsonrpc: "2.0",
        id: "req-1",
        result: { content: [{ type: "text", text: JSON.stringify({ ok: true }) }] },
      }), { status: 200, headers: { "Content-Type": "application/json" } });
    },
  });

  const result = await invoke("elo_pcp_dados_pendentes");
  assert.deepEqual(result, { ok: true });
  assert.equal(captured.init.headers.Authorization, "Bearer secret-user-bearer");
  assert.doesNotMatch(captured.init.body, /secret-user-bearer/);
  assert.match(captured.url, /\/functions\/v1\/elo-mcp$/);
});
