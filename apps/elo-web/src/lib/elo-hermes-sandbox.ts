import { Sandbox } from "@vercel/sandbox";

export type HermesSandboxRequest = {
  correlationId: string;
  missionId: string;
  command: string;
  args?: string[];
  timeoutMs?: number;
};

export type HermesSandboxReceipt = {
  missionId: string;
  correlationId: string;
  executor: "hermes";
  runtime: "vercel-sandbox";
  status: "SUCCEEDED" | "FAILED";
  stdout: string;
  stderr: string;
  exitCode: number;
};

function requireGitToken() {
  const token = process.env.ELO_HERMES_GIT_TOKEN?.trim();
  if (!token) {
    throw new Error("ELO_HERMES_GIT_TOKEN is required to clone the private governed Hermes repository.");
  }
  return token;
}

/**
 * Server-only governed execution primitive.
 * Browser code must never import or invoke this module directly.
 * Authorization and mission policy remain owned by ELO Cognitive/Symbiont.
 */
export async function executeHermesInVercelSandbox(input: HermesSandboxRequest): Promise<HermesSandboxReceipt> {
  const gitToken = requireGitToken();
  const timeoutMs = Math.min(Math.max(input.timeoutMs ?? 5 * 60 * 1000, 10_000), 45 * 60 * 1000);

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
    networkPolicy: {
      allow: ["api.openai.com", "github.com", "raw.githubusercontent.com"],
    },
  });

  try {
    const result = await sandbox.runCommand({
      cmd: input.command,
      args: input.args ?? [],
    });

    const stdout = (await result.stdout()).trim();
    const stderr = (await result.stderr()).trim();
    return {
      missionId: input.missionId,
      correlationId: input.correlationId,
      executor: "hermes",
      runtime: "vercel-sandbox",
      status: result.exitCode === 0 ? "SUCCEEDED" : "FAILED",
      stdout,
      stderr,
      exitCode: result.exitCode,
    };
  } finally {
    await sandbox.stop();
  }
}
