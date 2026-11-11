export type GovernedSource = {
  source_id: string;
  source_type: string;
  title?: string | null;
  uri?: string | null;
};

export type GovernedSuggestion = {
  action_id: string;
  label: string;
  action_type: string;
  payload: Record<string, unknown>;
  requires_approval: boolean;
};

export type GovernedPcpResult = {
  response: Record<string, unknown>;
  confidence: number;
  sources: GovernedSource[];
  suggestions: GovernedSuggestion[];
  evidenceRefs: string[];
  validationStatus: string;
  policyDecision: string;
  metadata: Record<string, unknown>;
};

export type EloMcpToolInvoker = (
  name: string,
  args?: Record<string, unknown>,
) => Promise<Record<string, unknown>>;

const PCP_DOMAINS = new Set(["planejamento", "pcp", "planejamento_pcp", "planning"]);
const INDICATOR_TERMS = [
  "indicador", "indicadores", "kpi", "capacidade", "horas",
  "aderencia", "utilizacao", "carga", "produtividade",
];

function text(value: unknown) {
  return typeof value === "string" ? value.trim() : "";
}

function record(value: unknown): Record<string, unknown> | null {
  return value && typeof value === "object" && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function rows(value: unknown): Record<string, unknown>[] {
  return Array.isArray(value)
    ? value.map(record).filter((item): item is Record<string, unknown> => item !== null)
    : [];
}

function normalize(value: string) {
  return value.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLocaleLowerCase("pt-BR");
}

export function isPcpPlanningDomain(domain: string) {
  return PCP_DOMAINS.has(normalize(domain.trim()));
}

function isIndicatorIntent(message: string) {
  const normalized = normalize(message);
  return INDICATOR_TERMS.some((term) => normalized.includes(term));
}

function sourceRef(prefix: string, key: string) {
  return `${prefix}:${key.replace(/[^A-Za-z0-9_.:-]+/g, "_")}`;
}

function unavailableResult(): GovernedPcpResult {
  return {
    response: {
      type: "evidence_unavailable",
      status: "UNVERIFIED",
      content: "A consulta foi recebida, mas a evidência governada necessária não está disponível neste momento.",
    },
    confidence: 0,
    sources: [],
    suggestions: [],
    evidenceRefs: [],
    validationStatus: "UNVERIFIED",
    policyDecision: "EVIDENCE_UNAVAILABLE",
    metadata: { confidence_calibrated: false, must_not_infer: true },
  };
}

export function createEloMcpToolInvoker(input: {
  baseUrl: string;
  accessToken: string;
  requestId: string;
  fetchImpl?: typeof fetch;
}): EloMcpToolInvoker {
  const baseUrl = input.baseUrl.trim().replace(/\/$/, "");
  const accessToken = input.accessToken.trim();
  const requestId = input.requestId.trim();
  const fetchImpl = input.fetchImpl ?? fetch;
  if (!baseUrl || !accessToken || !requestId) {
    throw new Error("governed MCP boundary is not configured");
  }

  return async (name, args = {}) => {
    const response = await fetchImpl(`${baseUrl}/functions/v1/elo-mcp`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
        "mcp-protocol-version": "2025-06-18",
        "x-elo-request-id": requestId,
      },
      body: JSON.stringify({
        jsonrpc: "2.0",
        id: requestId,
        method: "tools/call",
        params: { name, arguments: args },
      }),
      cache: "no-store",
    });
    let envelope: Record<string, unknown>;
    try {
      envelope = await response.json() as Record<string, unknown>;
    } catch {
      throw new Error("governed MCP returned an invalid response");
    }
    if (!response.ok || envelope.error) {
      throw new Error("governed MCP read was denied or unavailable");
    }
    const result = record(envelope.result);
    const content = Array.isArray(result?.content) ? result.content : [];
    const textItem = content
      .map(record)
      .find((item) => item?.type === "text" && typeof item.text === "string");
    if (!textItem) throw new Error("governed MCP did not return evidence");
    try {
      return JSON.parse(String(textItem.text)) as Record<string, unknown>;
    } catch {
      throw new Error("governed MCP evidence is not structured");
    }
  };
}

function gapQuestion(item: Record<string, unknown>, index: number): GovernedSuggestion | null {
  const prompt = text(item.pergunta_gpt);
  if (!prompt) return null;
  const code = text(item.codigo) || `gap-${index + 1}`;
  const evidenceRef = sourceRef("pcp_gap", code);
  return {
    action_id: `ADM-${code.replace(/[^A-Za-z0-9_-]+/g, "_")}`,
    label: prompt,
    action_type: "admin_decision_question",
    payload: {
      gap_id: code,
      gate: text(item.gate) || null,
      source: text(item.fonte_autorizada) || null,
      required_fields: Array.isArray(item.campos_obrigatorios) ? item.campos_obrigatorios : [],
      why_needed: text(item.motivo) || null,
      evidence_refs: [evidenceRef],
      answer_contract: "HUMAN_EVIDENCE_CANDIDATE",
      answer_scope: "CURRENT_DECISION_CONTEXT_ONLY",
      canonical_mutation: false,
      must_not_infer: true,
    },
    requires_approval: true,
  };
}

function blockingGapResult(payload: Record<string, unknown>): GovernedPcpResult | null {
  const blocking = rows(payload.requests).filter(
    (item) => item.bloqueia_execucao === true && Boolean(text(item.pergunta_gpt)),
  );
  if (blocking.length === 0) return null;
  const suggestions = blocking
    .slice(0, 5)
    .map(gapQuestion)
    .filter((item): item is GovernedSuggestion => item !== null);
  const evidenceRefs = suggestions.flatMap((item) =>
    Array.isArray(item.payload.evidence_refs) ? item.payload.evidence_refs.map(String) : []
  );
  return {
    response: {
      type: "decision_required",
      status: "PARTIAL_SUPPORTED",
      content: `Há ${blocking.length} pendência(s) de evidência que bloqueiam a decisão. A parte comprovada pode ser apresentada, mas a parcela dependente desses dados permanece bloqueada.`,
      blocking_count: blocking.length,
      questions_returned: suggestions.length,
    },
    confidence: 0,
    sources: blocking.slice(0, 5).map((item, index) => {
      const code = text(item.codigo) || `gap-${index + 1}`;
      return {
        source_id: sourceRef("pcp_gap", code),
        source_type: "GOVERNED_PCP_GAP",
        title: text(item.gate) || code,
        uri: null,
      };
    }),
    suggestions,
    evidenceRefs,
    validationStatus: "PARTIAL_SUPPORTED",
    policyDecision: "HUMAN_EVIDENCE_REQUIRED",
    metadata: {
      must_not_infer: true,
      blocking_count: blocking.length,
      question_limit: 5,
      answer_contract: "HUMAN_EVIDENCE_CANDIDATE",
    },
  };
}

function indicatorResult(payload: Record<string, unknown>): GovernedPcpResult {
  const indicators = record(payload.indicadores);
  const capacity = record(indicators?.capacidade);
  const external = record(indicators?.montagem_externa);
  const kpi = record(payload.kpi_formal);
  const state = text(payload.state) || "INDETERMINADO";

  if (state === "BLOQUEADO_CATALOGO") {
    const missing = Array.isArray(payload.missing_sources) ? payload.missing_sources.map(String) : [];
    return {
      response: {
        type: "pcp_indicators",
        status: "BLOCKED_EVIDENCE",
        content: "Os indicadores não podem ser apresentados porque as fontes necessárias ainda não estão governadas no catálogo.",
        missing_source_count: missing.length,
      },
      confidence: 0,
      sources: [],
      suggestions: [],
      evidenceRefs: [],
      validationStatus: "BLOCKED_EVIDENCE",
      policyDecision: "GOVERNED_SOURCE_CATALOG_REQUIRED",
      metadata: { confidence_calibrated: false, must_not_infer: true },
    };
  }

  const capacityRows = rows(capacity?.rows);
  const definitionRows = rows(kpi?.definitions);
  const snapshotRows = rows(kpi?.snapshots);
  const externalRow = record(external?.row);
  const evidenceRefs = [
    text(capacity?.source_table),
    text(external?.source_table),
    text(kpi?.definition_source),
    text(kpi?.snapshot_source),
  ].filter(Boolean).map((item) => sourceRef("pcp_source", item));

  return {
    response: {
      type: "pcp_indicators",
      status: state,
      content: [
        `Capacidade: ${text(capacity?.state) || "INDETERMINADO"}.`,
        `Montagem externa: ${text(external?.state) || "INDETERMINADO"}.`,
        `KPI formal: ${text(kpi?.state) || "INDETERMINADO"}.`,
      ].join(" "),
      capacity_rows: capacityRows.length,
      external_observation_available: Boolean(externalRow),
      kpi_definition_count: definitionRows.length,
      kpi_snapshot_count: snapshotRows.length,
    },
    confidence: 0,
    sources: evidenceRefs.map((ref) => ({
      source_id: ref,
      source_type: "GOVERNED_PCP_READ_MODEL",
      title: ref.replace(/^pcp_source:/, ""),
      uri: null,
    })),
    suggestions: [],
    evidenceRefs,
    validationStatus: state === "CONSULTED" ? "OBSERVED_UNCALIBRATED" : state,
    policyDecision: "READ_ONLY_GOVERNED_SOURCE_SELECTION",
    metadata: {
      confidence_calibrated: false,
      automatic_kpi_promotion: false,
      read_only: true,
    },
  };
}

function decisionResult(payload: Record<string, unknown>): GovernedPcpResult {
  const nextRuestion = text(payload.next_question);
  if (nextQuestion) {
    const suggestion: GovernedSuggestion = {
      action_id: "ADM-PCP-DECISAO-EXTERNA",
      label: nextRuestion,
      action_type: "admin_decision_question",
      payload: {
        gap_id: "PCP_DECISAO_EXTERNA",
        answer_contract: "HUMAN_EVIDENCE_CANDIDATE",
        answer_scope: "CURRENT_DECISION_CONTEXT_ONLY",
        canonical_mutation: false,
        must_not_infer: true,
      },
      requires_approval: true,
    };
    return {
      response: {
        type: "decision_required",
        status: "PARTIAL_SUPPORTED",
        content: "A decisão PCP possui uma validação pendente. O conteúdo já observado permanece disponível, mas a conclusão dependente dessa validação continua bloqueada.",
      },
      confidence: 0,
      sources: [],
      suggestions: [suggestion],
      evidenceRefs: [],
      validationStatus: "PARTIAL_SUPPORTED",
      policyDecision: "HUMAN_EVIDFNCE_REQUIRED",
      metadata: { confidence_calibrated: false, must_not_infer: true },
    };
  }

  const summary = record(payload.resumo);
  const details = rows(payload.detalhes);
  const evidenceRefs = summary
    ? [sourceRef("pcp_source", "decisao_externa_resumo")]
    : [];

  return {
    response: {
      type: "pcp_decision_status",
      status: summary ? "OBSERVED_UNCALIBRATED" : "NO_GOVERNED_SUMMARY",
      content: summary
        ? "O cockpit governado de decisão PCP foi consultado. O resumo observado está disponível para análise, sem promover recomendação a decisão aprovada."
        : "Não há resumo governado suficiente para concluir a decisão PCP neste momento.",
      summary: summary ?? null,
      detail_count: details.length,
    },
    confidence: 0,
    sources: evidenceRefs.map((ref) => ({
      source_id: ref,
      source_type: "GOVERNED_PCP_READ_MODEL",
      title: "Decisão externa PCP",
      uri: null,
    })),
    suggestions: [],
    evidenceRefs,
    validationStatus: summary ? "OBSERVED_UNCALIBRATED" : "UNVERIFIED",
    policyDecision: summary
      ? "READ_ONLY_GOVERNED_SOURCE_SELECTION"
      : "EVIDENCE_UNAVAILABLE",
    metadata: { confidence_calibrated: false, must_not_infer: true, read_only: true },
  };
}

export async function processGovernedPcpMission(input: {
  message: string;
  invokeTool: EloMcpToolInvoker;
}): Promise<GovernedPcpResult> {
  try {
    const gaps = await input.invokeTool("elo_pcp_dados_pendentes");
    const blocking = blockingGapResult(gaps);
    if (blocking) return blocking;

    if (isIndicatorIntent(input.message)) {
      return indicatorResult(await input.invokeTool("elo_pcp_indicadores_status"));
    }
    return decisionResult(await input.invokeTool("elo_pcp_decisao_externa_status"));
  } catch {
    return unavailableResult();
  }
}

export function unverifiedDomainResult(domain: string): GovernedPcpResult {
  return {
    ...unavailableResult(),
    response: {
      type: "evidence_required",
      status: "UNVERIFIED",
      content: `A solicitação do domínio ${domain || "não informado"} foi recebida, mas este runtime ainda não possui uma fonte governada conectada para produzir uma resposta factual.`,
    },
    policyDecision: "NEEDS_GOVERNED_EVIDENCE",
  };
}
