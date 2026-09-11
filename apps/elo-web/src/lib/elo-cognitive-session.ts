import { randomUUID } from "node:crypto";

export const ELO_COGNITIVE_SESSION_COOKIE = "elo_cognitive_session";

export function createCognitiveSessionId() {
  return randomUUID();
}

export function isValidCognitiveSessionId(value: string | undefined | null) {
  return typeof value === "string" && /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value);
}
