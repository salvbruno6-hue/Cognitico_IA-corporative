// Internal strategic-write policy helpers for the canonical elo-authz function.
//
// This module is NOT a separate authorization authority and is not deployed or
// invoked independently. It only centralizes deterministic policy constants and
// validation helpers for future integration into elo-authz/index.ts.

export const STRATEGIC_ACTION_CAPABILITY: Readonly<Record<string, string>> = {
  strategic_okr_propose: "PROPOSE",
  strategic_okr_review: "REVIEW",
  strategic_okr_approve: "APPROVE",
  strategic_okr_write: "CANONICAL_WRITE",
};

export const STRATEGIC_RECEIPT_TTL_SECONDS = 300;

export type EloScopeView = {
  scope_type?: unknown;
  scope_key?: unknown;
  active?: unknown;
};

export type GoogleIdentityView = {
  provider?: unknown;
  authorized_email?: unknown;
  active?: unknown;
  auth_user_id?: unknown;
};

export function strategicCapabilityForAction(action: string): string | null {
  return STRATEGIC_ACTION_CAPABILITY[action] ?? null;
}

export function isRegisteredGoogleIdentity(
  identity: GoogleIdentityView,
  authenticatedEmail: string,
): boolean {
  const email = authenticatedEmail.trim().toLowerCase();
  const authorizedEmail = String(identity?.authorized_email ?? "").trim().toLowerCase();
  const authUserId = String(identity?.auth_user_id ?? "").trim();
  return (
    identity?.active === true &&
    String(identity?.provider ?? "").trim().toLowerCase() === "google" &&
    Boolean(authUserId) &&
    Boolean(email) &&
    authorizedEmail === email
  );
}

export function hasEnterpriseTenantScope(scopes: EloScopeView[], tenantId: string): boolean {
  const tenant = tenantId.trim();
  if (!tenant) return false;
  return scopes.some((scope) =>
    scope?.active === true &&
    String(scope?.scope_type ?? "").trim() === "ENTERPRISE" &&
    String(scope?.scope_key ?? "").trim() === tenant
  );
}

export function isStrategicResourceRef(value: string): boolean {
  const ref = value.trim();
  if (!ref) return false;
  return (
    /^strategic_okr:objective:[^:]+$/.test(ref) ||
    /^strategic_okr:key_result:[^:]+$/.test(ref) ||
    /^strategic_okr:binding:[^:]+:[^:]+$/.test(ref)
  );
}

export function strategicReceiptExpiry(nowMs = Date.now()): string {
  return new Date(nowMs + STRATEGIC_RECEIPT_TTL_SECONDS * 1000).toISOString();
}
