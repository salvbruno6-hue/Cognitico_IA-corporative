import { Sandbox } from "@vercel/sandbox";

export type HermesExecutionRequest = {
  request_id: string;
  intent: string;
  context: Record<string, unknown>;
  tenant_scope: string;
  mission_class: string;
  authorized_capabilities: string[];
  method?: string | null;
  constraints?: Record<string, unknown>;
  evidence_requirements?: string[];
  execution_policy?: Record<string, unknown>;
  contract_version?: string;
};

export type HermesExecutionResult = {
  request_id: string;
  status: "completed" | "partial" | "blocked" | "failed";
  execution: Record<string, unknown>;
  artifacts: Array<Record<string, unknown>>;
  evidence: Array<Record<string, unknown>>;
  tool_usage: Array<Record<string, unknown>>;
  skills_used: string[];
  outcome: Record<string, unknown>;
  gaps: string[];
  conflicts: string[];
  metrics: Record<string, unknown>;
  learning_candidate: Record<string, unknown> | null;
  contract_version: "1.0";
};

function requireEnv(name: string) {
  const value = process.env[name]?.trim();
  if (!value) throw new Error(`${name} is required for the governed Hermes runtime boundary.`);
  return value;
}

function missionCommand(request: HermesExecutionRequest): { cmd: string; args: string[] } {
  if (request.mission_class === "runtime_probe" && request.authorized_capabilities.includes("hermes.runtime.probe")) {
    return { cmd: "python", args: ["-m", "hermes_cli.main", "--version"] };
  }
  throw new Error("Mission is not an allowed Vercel Hermes sandbox operation.");
}

/** Server-only. The browser cannot invoke this module or select an arbitrary command. */
export async function executeHermesInVercelSandbox(request: HermesExecutionRequest): Promise<HermesExecutionResult> {
  const gitToken = requireEnv("ELO_HERMES_GIT_TOKEN");
  const runtimeSecret = requireEnv("ELO_HERMES_RUNTIME_TOKEN");
  const command = missionCommand(request);
  const timeoutMs = Math.min(Math.max(Number(request.execution_policy?.timeout_ms ?? 5 * 60 * 1000), 10_000), 45 * 60 * 1000);

  const sandbox = await Sandbox.create({
    persistent: false,
    runtime: "python3.13",
    timeout: timeoutMs,
    source: {
      type: "git",
      url: "https://github.com/salvbruno6-hue/ELO-Hermes-Agent.git",
      username: "x-access-token",
      password: gitToken,
    },
    env: { ELO_HERMES_RUNTIME_TOKEN: runtimeSecret },
    networkPolicy: { allow: ["api.openai.com", "github.com", "raw.githubusercontent.com"] },
  });

  try {
    const result = await sandbox.runCommand(command);
    const stdout = (await result.stdout()).trim();
    const stderr = (await result.stderr()).trim();
    const succeeded = result.exitCode === 0;
    return {
      request_id: request.request_id,
      status: succeeded ? "completed" : "failed",
      execution: { runtime: "vercel-sandbox", executor: "hermes", exit_code: result.exitCode },
      artifacts: [],
      evidence: [{ type: "execution", source: "vercel-sandbox", stdout, stderr, exit_code: result.exitCode }],
      tool_usage: [],
      skills_used: [],
      outcome: { completed: succeeded, mission_class: request.mission_class },
      gaps: succeeded ? [] : ["hermes_runtime_probe_failed"],
      conflicts: [],
      metrics: { stdout_length: stdout.length, stderr_length: stderr.length },
      learning_candidate: null,
      contract_version: "1.0",
    };
  } finally {
    await sandbox.stop();
  }
}
