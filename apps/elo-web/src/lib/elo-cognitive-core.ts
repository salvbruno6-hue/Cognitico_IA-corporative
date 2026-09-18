export type LocalCognitiveRequest = {
  requestId: string;
  correlationId: string;
  message: string;
  tenantId: string;
  principalId?: string;
  domain: string;
  sessionId: string;
  context?: Record<string, unknown>;
};

export type LocalCognitiveResult = {
  response: Record<string, unknown>;
  confidence: number;
  domain: string;
  hermes?: Record<string, unknown>;
  provenance: {
    request_id: string;
    correlation_id: string;
    tenant_id: string;
    domain: string;
    principal_id?: string;
    session_id: string;
    provider: string;
    evidence_refs: string[];
    policy_decision: string;
    validation_status: string;
    metadata?: Record<string, unknown>;
  };
};

const RUNTIME_PROBE_MISSION = "runtime_probe";
const RUNTIME_PROBE_CAPABILITY = "hermes:runtime_probe";

function requireTenant(tenantId: string) {
  if (!tenantId.trim()) throw new Error("tenant_id is required");
}

export function processLocalCognitiveMission(input: LocalCognitiveRequest): LocalCognitiveResult {
  requireTenant(input.tenantId);

  const mission = input.context?.hermes_mission;
  if (mission !== undefined) {
    if (!mission || typeof mission !== "object" || Array.isArray(mission)) {
      throw new Error("hermes_mission must be an object");
    }

    const missionRecord = mission as Record<string, unknown>;
    const missionClass = String(missionRecord.mission_class ?? "");
    const capabilities = Array.isArray(missionRecord.authorized_capabilities)
      ? missionRecord.authorized_capabilities.map(String)
      : [];

    if (missionClass !== RUNTIME_PROBE_MISSION) {
      throw new Error("unsupported Hermes mission class");
    }
    if (!capabilities.includes(RUNTIME_PROBE_CAPABILITY)) {
      throw new Error("Hermes runtime probe capability was not authorized by ELO");
    }

    return {
      response: {
        type: "hermes_execution",
        content: "Hermes runtime probe autorizado pela governança do ELO; execução deve ocorrer no runtime privado.",
        status: "authorized",
      },
      confidence: 1,
      domain: input.domain,
      hermes: {
        mission_class: RUNTIME_PROBE_MISSION,
        capability: RUNTIME_PROBE_CAPABILITY,
        constraints: { read_only: true, canonical_mutation: false },
        execution_policy: { bounded: true, approval_required_for_mutation: true },
        evidence_requirements: ["execution", "outcome"],
      },
      provenance: {
        request_id: input.requestId,
        correlation_id: input.correlationId,
        tenant_id: input.tenantId,
        domain: input.domain,
        principal_id: input.principalId,
        session_id: input.sessionId,
        provider: "elo-web-local-cognitive-core",
        evidence_refs: [input.requestId],
        policy_decision: "ALLOW",
        validation_status: "governed_runtime_probe",
      },
    };
  }

  return {
    response: { type: "analysis", content: input.message },
    confidence: 1,
    domain: input.domain,
    provenance: {
      request_id: input.requestId,
      correlation_id: input.correlationId,
      tenant_id: input.tenantId,
      domain: input.domain,
      principal_id: input.principalId,
      session_id: input.sessionId,
      provider: "elo-web-local-cognitive-core",
      evidence_refs: [],
      policy_decision: "ALLOW",
      validation_status: "validated",
    },
  };
}
