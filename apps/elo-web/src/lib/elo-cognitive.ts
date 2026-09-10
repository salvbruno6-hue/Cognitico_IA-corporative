export type CognitiveSource = {
  source_id: string;
  source_type: string;
  title?: string | null;
  uri?: string | null;
};

export type CognitiveSuggestion = {
  action_id: string;
  label: string;
  action_type: string;
  payload: Record<string, unknown>;
  requires_approval: boolean;
};

export type CognitiveResponse = {
  response_id: string;
  request_id: string;
  correlation_id: string;
  session_id: string;
  tenant_id: string;
  domain?: string | null;
  response: Record<string, unknown>;
  sources: CognitiveSource[];
  agents_used: Array<{ agent_id: string; role?: string | null; provider?: string | null; model?: string | null }>;
  confidence: number;
  provenance: {
    request_id: string;
    correlation_id: string;
    tenant_id: string;
    domain?: string | null;
    principal_id?: string | null;
    session_id?: string | null;
    provider?: string | null;
    model?: string | null;
    evidence_refs: string[];
    policy_decision?: string | null;
    validation_status?: string | null;
    metadata?: Record<string, unknown>;
  };
  suggestions: CognitiveSuggestion[];
  processing_time_ms: number;
  timestamp: string;
};

export class ELOCognitiveError extends Error {
  status: number;
  code: string;

  constructor(message: string, status = 500, code = "COGNITIVE_PROCESSING_FAILED") {
    super(message);
    this.name = "ELOCognitiveError";
    this.status = status;
    this.code = code;
  }
}

function requireConfig(name: string) {
  const value = process.env[name]?.trim();
  if (!value) throw new ELOCognitiveError(`${name} não está configurada no servidor.`, 500, "CONFIGURATION_ERROR");
  return value;
}

export async function executeCognitiveMission(input: {
  message: string;
  tenantId: string;
  principalId?: string;
  userId?: string;
  domain: string;
  sessionId?: string;
  context?: Record<string, unknown>;
}) {
  const baseUrl = requireConfig("ELO_COGNITIVE_API_URL").replace(/\/$/, "");
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30_000);

  try {
    const response = await fetch(`${baseUrl}/cognitive`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      cache: "no-store",
      signal: controller.signal,
      body: JSON.stringify({
        message: input.message,
        tenant_id: input.tenantId,
        principal_id: input.principalId,
        user_id: input.userId,
        domain: input.domain,
        session_id: input.sessionId,
        context: input.context ?? {},
      }),
    });

    const payload = await response.json().catch(() => null);
    if (!response.ok) {
      const message = typeof payload?.message === "string" ? payload.message : typeof payload?.detail === "string" ? payload.detail : "A API cognitiva recusou a missão.";
      throw new ELOCognitiveError(message, response.status, typeof payload?.code === "string" ? payload.code : "COGNITIVE_REQUEST_REJECTED");
    }
    return payload as CognitiveResponse;
  } catch (error) {
    if (error instanceof ELOCognitiveError) throw error;
    if (error instanceof DOMException && error.name === "AbortError") throw new ELOCognitiveError("Tempo limite excedido ao consultar o ELO Cognitivo.", 504, "COGNITIVE_TIMEOUT");
    throw new ELOCognitiveError("Não foi possível alcançar o ELO Cognitivo.", 502, "COGNITIVE_UNAVAILABLE");
  } finally {
    clearTimeout(timeout);
  }
}
