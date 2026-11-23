import { executeHermesInVercelSandbox } from "@/lib/elo-hermes-sandbox";
import {
  createEloMcpToolInvoker,
  isPcpPlanningDomain,
  processGovernedPcpMission,
  unverifiedDomainResult,
  type EloMcpToolInvoker,
  type GovernedSource,
  type GovernedSuggestion,
} from "@/lib/elo-pcp-governed-response";

export type LocalCognitiveRequest = {
  requestId: string;
  correlationId: string;
  message: string;
  tenantId: string;
  principalId?: string;
  domain: string;
  sessionId: string;
  context?: Record<string, unknown>;
  accessToken?: string;
  governedReader?: EloMcpToolInvoker;
};

export type LocalCognitiveResult = {
  response: Record<string, unknown>;
  confidence: number;
  domain: string;
  hermes?: Record<string, unknown>;
  sources?: GovernedSource[];
  suggestions?: GovernedSuggestion[];
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

export type ObjectiveContinuityDecision = "CONTINUE" | "CORRECT" | "REPLAN" | "ESCALATE" | "COMPLETE";

export type ObjectiveContinuityDecisionInput = {
  objectiveSatisfied: boolean;
  withinScope: boolean;
  authorityAvailable: boolean;
  riskLevel: string;
  iteration: number;
  maxCycles: number;
  noProgressStreak: number;
};

export type ObjectiveContinuityDecisionResult = {
  decision: ObjectiveContinuityDecision;
  reason: string;
};

const RUNTIME_PROBE_MISSION = "runtime_probe";
const RUNTIME_PROBE_CAPABILITY = "hermes:runtime_probe";

function requireTenant(tenantId: string) {
  if (!tenantId.trim()) throw new Error("tenant_id is required");
}

/**
 * Cognitive decision policy for one bounded Objective Continuity cycle.
 *
 * This function owns no persistence or authorization. It preserves the
 * canonical ObjectiveContinuityAdapter semantics inside the official ELO Web
 * runtime so the checkpoint store only persists the cognitive result.
 */
export function orchestrateObjectiveContinuityDecision(
  input: ObjectiveContinuityDecisionInput,
): ObjectiveContinuityDecisionResult {
  if (!Number.isInteger(input.iteration) || input.iteration < 1) {
    throw new Error("objective continuity iteration must be >= 1");
  }
  if (!Number.isInteger(input.maxCycles) || input.maxCycles < 2) {
    throw new Error("objective continuity maxCycles must be >= 2");
  }
  if (!Number.isInteger(input.noProgressStreak) || input.noProgressStreak < 0) {
    throw new Error("objective continuity noProgressStreak must be >= 0");
  }

  if (input.objectiveSatisfied) {
    return { decision: "COMPLETE", reason: "objective acceptance criteria satisfied" };
  }
  if (!input.withinScope) {
    return { decision: "ESCALATE", reason: "next action would leave approved objective scope" };
  }
  if (!input.authorityAvailable) {
    return { decision: "ESCALATE", reason: "required authority is unavailable" };
  }

  const risk = input.riskLevel.trim().toUpperCase();
  if (["HIGH", "CRITICAL", "ALTO", "CRITICO"].includes(risk)) {
    return { decision: "ESCALATE", reason: "risk exceeds bounded autonomous execution" };
  }
  if (input.iteration >= input.maxCycles) {
    return { decision: "ESCALATE", reason: "objective loop autonomy cycle budget exhausted" };
  }
  if (input.noProgressStreak >= 4) {
    return { decision: "ESCALATE", reason: "persistent no-progress after correction/replanning" };
  }
  if (input.noProgressStreak >= 2) {
    return { decision: "REPLAN", reason: "current approach is not producing objective-relevant progress" };
  }
  if (input.noProgressStreak >= 1) {
    return { decision: "CORRECT", reason: "local correction required before repeating the action" };
  }
  return { decision: "CONTINUE", reason: "objective-relevant progress observed" };
}

export async function processLocalCognitiveMission(input: LocalCognitiveRequest): Promise<LocalCognitiveResult> {
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

    const hermesResult = await executeHermesInVercelSandbox({
      request_id: input.requestId,
      intent: input.message,
      context: { domain: input.domain, mission: RUNTIME_PROBE_MISSION },
      tenant_scope: input.tenantId,
      mission_class: RUNTIME_PROBE_MISSION,
      authorized_capabilities: capabilities,
      method: "runtime_probe",
      constraints: { read_only: true, canonical_mutation: false },
      evidence_requirements: ["execution", "outcome"],
      execution_policy: {
        bounded: true,
        approval_required_for_mutation: true,
      },
      contract_version: "1.0",
    });

    return {
      response: {
        type: "hermes_execution",
        content: hermesResult.outcome,
        status: hermesResult.status,
      },
      confidence: 1,
      domain: input.domain,
      hermes: hermesResult,
      provenance: {
        request_id: input.requestId,
        correlation_id: input.correlationId,
        tenant_id: input.tenantId,
        domain: input.domain,
        principal_id: input.principalId,
        session_id: input.sessionId,
        provider: "elo-web-local-cognitive-core-via-private-hermes",
        evidence_refs: [input.requestId],
        policy_decision: "ALLOW",
        validation_status: "evidence_validated",
      },
    };
  }

  const baseUrl = (process.env.ELO_FORGE_SUPABASE_URL ?? process.env.NEXT_PUBLIC_SUPABASE_URL ?? "").trim();
  const governedReader = input.governedReader ?? (
    input.accessToken?.trim() && baseUrl
      ? createEloMcpToolInvoker({
          baseUrl,
          accessToken: input.accessToken,
          requestId: input.requestId,
        })
      : undefined
  );

  const governed = isPcpPlanningDomain(input.domain) && governedReader
    ? await processGovernedPcpMission({ message: input.message, invokeTool: governedReader })
    : unverifiedDomainResult(input.domain);

  return {
    response: governed.response,
    confidence: governed.confidence,
    domain: input.domain,
    sources: governed.sources,
    suggestions: governed.suggestions,
    provenance: {
      request_id: input.requestId,
      correlation_id: input.correlationId,
      tenant_id: input.tenantId,
      domain: input.domain,
      principal_id: input.principalId,
      session_id: input.sessionId,
      provider: isPcpPlanningDomain(input.domain) ? "elo-mcp-governed-pcp" : "elo-web-local-cognitive-core",
      evidence_refs: governed.evidenceRefs,
      policy_decision: governed.policyDecision,
      validation_status: governed.validationStatus,
      metadata: governed.metadata,
    },
  };
}
