import { processLocalCognitiveMission } from "@/lib/elo-cognitive-core";

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

export async function executeCognitiveMission(input: {
  message: string;
  tenantId: string;
  principalId?: string;
  userId?: string;
  domain: string;
  sessionId: string;
  context?: Record<string, unknown>;
}): Promise<CognitiveResponse> {
  const startedAt = performance.now();

  try {
    const result = await processLocalCognitiveMission({
      requestId: crypto.randomUUID(),
      correlationId: crypto.randomUUID(),
      message: input.message,
      tenantId: input.tenantId,
      principalId: input.principalId ?? input.userId,
      domain: input.domain,
      sessionId: input.sessionId,
      context: input.context ?? {},
    });

    return {
      response_id: crypto.randomUUID(),
      request_id: result.provenance.request_id,
      correlation_id: result.provenance.correlation_id,
      session_id: input.sessionId,
      tenant_id: input.tenantId,
      domain: input.domain,
      response: result.response,
      sources: [],
      agents_used: [],
      confidence: result.confidence,
      provenance: result.provenance,
      suggestions: [],
      processing_time_ms: Math.max(0, performance.now() - startedAt),
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    if (error instanceof Error) {
      throw new ELOCognitiveError(error.message, 400, "COGNITIVE_REQUEST_REJECTED");
    }
    throw new ELOCognitiveError("Falha ao processar a missão cognitiva.");
  }
}
