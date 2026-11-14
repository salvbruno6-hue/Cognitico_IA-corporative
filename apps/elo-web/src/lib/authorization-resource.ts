/** Pure, client-side input validation only. Authorization remains exclusively in elo-authz. */
export const CANONICAL_REPOSITORY = "salvbruno6-hue/Cognitico_IA-corporative";

export function mergeGrantResource(pr: string, sha: string): string | null {
  if (!/^[1-9][0-9]*$/.test(pr) || !/^[a-fA-F0-9]{40}$/.test(sha)) return null;
  return `pr:${pr}@${sha.toLowerCase()}`;
}
