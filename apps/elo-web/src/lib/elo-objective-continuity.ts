import { createClient, type SupabaseClient } from "@supabase/supabase-js";

export type ObjectiveLoopDecision = "CONTINUE" | "CORRECT" | "REPLAN" | "ESCALATE" | "COMPLETE";

export type ObjectiveCheckpoint = {
  tenant_id: string;
  objective_id: string;
  workstream_id: string;
  objective_title: string;
  status: "ACTIVE" | "COMPLETED" | "HUMAN_APPROVAL_REQUIRED" | "BLOCKED" | "FAILED";
  stage: string;
  next_action: string;
  iteration: number;
  state_version: number;
  last_progress_token: string;
  no_progress_streak: number;
  last_decision: ObjectiveLoopDecision;
  evidence_refs: string[];
  authorization_evidence_ref: string;
  authorization_identity_id: string;
  human_required: boolean;
};

export type ObjectiveCycleInput = {
  tenantId: string;
  objectiveId: string;
  objectiveTitle: string;
  workstreamId: string;
  expectedCheckpointVersion?: number | null;
  progressToken: string;
  evidenceRefs: string[];
  proposedNextAction: string;
  authorizationEvidenceRef: string;
  authorizationIdentityId: string;
  objectiveSatisfied?: boolean;
  withinScope?: boolean;
  authorityAvailable?: boolean;
  riskLevel?: string;
  maxCycles?: number;
};

export class ObjectiveContinuityError extends Error {
  constructor(public readonly code: string, message: string, public readonly status = 400) {
    super(message);
  }
}

function serverSupabase(): SupabaseClient {
  const url = (process.env.ELO_FORGE_SUPABASE_URL ?? process.env.NEXT_PUBLIC_SUPABASE_URL ?? "").trim();
  const key = (process.env.ELO_FORGE_SUPABASE_SERVICE_ROLE_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY ?? "").trim();
  if (!url || !key) throw new ObjectiveContinuityError("STORE_UNAVAILABLE", "Persistência governada do Objective Continuity não está configurada.", 503);
  return createClient(url, key, { auth: { persistSession: false, autoRefreshToken: false } });
}

function uniqueEvidence(...groups: string[][]) {
  return [...new Set(groups.flat().map((value) => value.trim()).filter(Boolean))];
}

function decide(input: ObjectiveCycleInput, noProgressStreak: number, iteration: number): ObjectiveLoopDecision {
  if (input.objectiveSatisfied === true) return "COMPLETE";
  if (input.withinScope === false || input.authorityAvailable === false) return "ESCALATE";
  if (["HIGH", "CRITICAL"].includes((input.riskLevel ?? "LOW").toUpperCase())) return "ESCALATE";
  if (iteration >= (input.maxCycles ?? 12)) return "ESCALATE";
  if (noProgressStreak >= 4) return "ESCALATE";
  if (noProgressStreak >= 2) return "REPLAN";
  if (noProgressStreak >= 1) return "CORRECT";
  return "CONTINUE";
}

function statusFor(decision: ObjectiveLoopDecision): ObjectiveCheckpoint["status"] {
  if (decision === "COMPLETE") return "COMPLETED";
  if (decision === "ESCALATE") return "HUMAN_APPROVAL_REQUIRED";
  return "ACTIVE";
}

function headline(decision: ObjectiveLoopDecision) {
  return {
    CONTINUE: "ELO confirmou continuidade do objetivo.",
    CORRECT: "ELO determinou correção antes de continuar.",
    REPLAN: "ELO determinou replanejamento governado.",
    ESCALATE: "ELO atingiu um limite que exige escalonamento.",
    COMPLETE: "ELO confirmou conclusão do objetivo.",
  }[decision];
}

function composeMessage(checkpoint: ObjectiveCheckpoint) {
  const shouldContinue = !checkpoint.human_required && ["CONTINUE", "CORRECT", "REPLAN"].includes(checkpoint.last_decision);
  const result = checkpoint.human_required
    ? "Resultado para o GPT: apresentar o retorno do ELO e aguardar intervenção humana."
    : shouldContinue
      ? "Resultado para o GPT: responder com este retorno e continuar do checkpoint persistido sem solicitar nova autorização conversacional."
      : "Resultado para o GPT: apresentar a conclusão e encerrar o ciclo do objetivo.";
  return [
    headline(checkpoint.last_decision),
    "",
    `Objetivo: ${checkpoint.objective_id}`,
    `Workstream: ${checkpoint.workstream_id}`,
    `Checkpoint: ${checkpoint.state_version}`,
    `Estado: ${checkpoint.status}`,
    `Decisão: ${checkpoint.last_decision}`,
    `Progress token: ${checkpoint.last_progress_token}`,
    `Próxima ação: ${checkpoint.next_action}`,
    "",
    "Controles observados:",
    "- persistência: PERSISTED",
    "- autorização: VALID",
    "- execução: EXECUTED",
    "- evidência: OBSERVED",
    `- referências de evidência: ${checkpoint.evidence_refs.length}`,
    "",
    result,
  ].join("\n");
}

export async function runObjectiveCycle(input: ObjectiveCycleInput) {
  if (!input.tenantId.trim() || !input.objectiveId.trim() || !input.workstreamId.trim()) {
    throw new ObjectiveContinuityError("INVALID_OBJECTIVE", "tenant_id, objective_id e workstream_id são obrigatórios.");
  }
  if (!input.progressToken.trim() || !input.proposedNextAction.trim() || input.evidenceRefs.filter(Boolean).length === 0) {
    throw new ObjectiveContinuityError("INSUFFICIENT_EVIDENCE", "progress_token, proposed_next_action e evidence_refs são obrigatórios.");
  }
  if (!input.authorizationEvidenceRef.trim() || !input.authorizationIdentityId.trim()) {
    throw new ObjectiveContinuityError("AUTHORIZATION_REQUIRED", "Evidência de autorização canônica é obrigatória.", 403);
  }

  const supabase = serverSupabase();
  const key = {
    tenant_id: input.tenantId.trim(),
    objective_id: input.objectiveId.trim(),
    workstream_id: input.workstreamId.trim(),
  };
  const { data: existing, error: readError } = await supabase
    .from("elo_objective_continuity_checkpoints")
    .select("*")
    .match(key)
    .maybeSingle();
  if (readError) throw new ObjectiveContinuityError("STORE_READ_FAILED", "Falha ao ler checkpoint persistente do ELO.", 503);

  if (existing && input.expectedCheckpointVersion != null && existing.state_version !== input.expectedCheckpointVersion) {
    throw new ObjectiveContinuityError(
      "STALE_CHECKPOINT",
      `Checkpoint stale: esperado ${input.expectedCheckpointVersion}, observado ${existing.state_version}.`,
      409,
    );
  }
  if (!existing && input.expectedCheckpointVersion != null && input.expectedCheckpointVersion > 1) {
    throw new ObjectiveContinuityError("STALE_CHECKPOINT", "Checkpoint esperado não existe no store persistente.", 409);
  }
  if (existing && ["COMPLETED", "HUMAN_APPROVAL_REQUIRED", "BLOCKED", "FAILED"].includes(existing.status)) {
    throw new ObjectiveContinuityError("TERMINAL_CHECKPOINT", `Objetivo está em estado terminal: ${existing.status}.`, 409);
  }

  const progressToken = input.progressToken.trim();
  const noProgressStreak = existing
    ? existing.last_progress_token === progressToken ? Number(existing.no_progress_streak ?? 0) + 1 : 0
    : 0;
  const iteration = existing ? Number(existing.iteration) + 1 : 1;
  const decision = decide(input, noProgressStreak, iteration);
  const humanRequired = decision === "ESCALATE";
  const version = existing ? Number(existing.state_version) + 1 : 1;
  const row = {
    ...key,
    objective_title: input.objectiveTitle.trim() || input.objectiveId.trim(),
    status: statusFor(decision),
    stage: "OBJECTIVE_CONTINUITY",
    next_action: input.proposedNextAction.trim(),
    iteration,
    state_version: version,
    last_progress_token: progressToken,
    no_progress_streak: noProgressStreak,
    last_decision: decision,
    evidence_refs: uniqueEvidence(Array.isArray(existing?.evidence_refs) ? existing.evidence_refs : [], input.evidenceRefs, [input.authorizationEvidenceRef]),
    authorization_evidence_ref: input.authorizationEvidenceRef.trim(),
    authorization_identity_id: input.authorizationIdentityId.trim(),
    human_required: humanRequired,
    updated_at: new Date().toISOString(),
  };

  let persisted: ObjectiveCheckpoint | null = null;
  if (!existing) {
    const { data, error } = await supabase.from("elo_objective_continuity_checkpoints").insert(row).select("*").single();
    if (error) {
      if (error.code === "23505") throw new ObjectiveContinuityError("STALE_CHECKPOINT", "Outro ciclo criou o checkpoint antes desta execução.", 409);
      throw new ObjectiveContinuityError("STORE_WRITE_FAILED", "Falha ao persistir checkpoint inicial do ELO.", 503);
    }
    persisted = data as ObjectiveCheckpoint;
  } else {
    const { data, error } = await supabase
      .from("elo_objective_continuity_checkpoints")
      .update(row)
      .match(key)
      .eq("state_version", existing.state_version)
      .select("*")
      .maybeSingle();
    if (error) throw new ObjectiveContinuityError("STORE_WRITE_FAILED", "Falha ao avançar checkpoint persistente do ELO.", 503);
    if (!data) throw new ObjectiveContinuityError("STALE_CHECKPOINT", "Checkpoint foi avançado por outra execução.", 409);
    persisted = data as ObjectiveCheckpoint;
  }

  const shouldContinueAutomatically = !persisted.human_required && ["CONTINUE", "CORRECT", "REPLAN"].includes(persisted.last_decision);
  return {
    final_message: composeMessage(persisted),
    decision: persisted.last_decision,
    next_action: persisted.next_action,
    progress_token: persisted.last_progress_token,
    checkpoint_version: persisted.state_version,
    should_continue_automatically: shouldContinueAutomatically,
    human_required: persisted.human_required,
    evidence_refs: persisted.evidence_refs,
    scenario_code: `${persisted.last_decision}.PERSISTED.VALID.EXECUTED.OBSERVED`,
    replay_count: 1,
    next_trigger: shouldContinueAutomatically
      ? {
          trigger_type: "CONTINUE_OBJECTIVE",
          objective_id: persisted.objective_id,
          workstream_id: persisted.workstream_id,
          checkpoint_version: persisted.state_version,
          next_action: persisted.next_action,
          progress_token: persisted.last_progress_token,
        }
      : null,
  };
}
