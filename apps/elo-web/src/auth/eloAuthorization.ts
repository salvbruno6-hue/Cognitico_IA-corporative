export type ELOAuthorizationAction =
  | "establish_session"
  | "revoke_session"
  | "read"
  | "consult"
  | "search"
  | "inspect";

export type ELOAuthorizationResult = {
  authorized: boolean;
  reason?: string;
  action?: string;
  identity_id?: string;
  session_id?: string;
  reused?: boolean;
  revoked?: number;
  authorization_authority?: string;
  [key: string]: unknown;
};

export async function callELOAuthorization(
  accessToken: string,
  action: ELOAuthorizationAction = "establish_session",
): Promise<ELOAuthorizationResult> {
  const response = await fetch("/api/authorization", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ action }),
    cache: "no-store",
  });

  const payload: unknown = await response.json().catch(() => null);
  if (!payload || typeof payload !== "object") {
    throw new Error("Resposta inválida da autorização ELO.");
  }

  const result = payload as ELOAuthorizationResult;
  if (!response.ok || result.authorized !== true) {
    throw new Error(result.reason || "Não foi possível autorizar o ELO.");
  }

  return result;
}
