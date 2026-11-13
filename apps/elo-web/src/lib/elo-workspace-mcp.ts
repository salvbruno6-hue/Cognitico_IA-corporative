/** Adapter to the existing elo-mcp boundary; no generic table access or new authority. */
export const workspaceTools = ["elo_status", "elo_pcp_dados_pendentes", "elo_pcp_demanda_crossing_status", "elo_pcp_decisao_externa_status", "elo_pcp_comunicacao_melhoria", "elo_pcp_orquestrador_dialogo"] as const;
export type WorkspaceTool = typeof workspaceTools[number];
export type MCPValue = Record<string, unknown>;

export async function callWorkspaceTool(baseUrl: string, accessToken: string, name: WorkspaceTool, args: Record<string, unknown> = {}, signal?: AbortSignal): Promise<MCPValue> {
  if (!workspaceTools.includes(name)) throw new Error("Consulta não disponível neste workspace.");
  const id = crypto.randomUUID();
  const response = await fetch(`${baseUrl.replace(/\/$/, "")}/functions/v1/elo-mcp`, {
    method: "POST", cache: "no-store", signal,
    headers: { Authorization: `Bearer ${accessToken}`, "Content-Type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id, method: "tools/call", params: { name, arguments: args } }),
  });
  if (response.status === 401 || response.status === 403) throw new Error("Não foi possível autorizar esta consulta. Verifique seu acesso com o administrador.");
  const payload = await response.json().catch(() => null);
  if (!response.ok || payload?.error || payload?.result?.isError || payload?.jsonrpc !== "2.0" || payload?.id !== id) throw new Error("O ELO não conseguiu concluir esta consulta. Tente novamente.");
  const block = payload.result?.content?.find((entry: { type?: string }) => entry.type === "text");
  let value: unknown;
  try { value = JSON.parse(block?.text ?? ""); } catch { throw new Error("O ELO retornou uma resposta inválida. Tente novamente."); }
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("O ELO retornou uma resposta inválida. Tente novamente.");
  return value as MCPValue;
}
