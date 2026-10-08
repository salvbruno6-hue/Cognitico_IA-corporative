"use client";

import { useEffect, useState } from "react";

const tables = [
  { key: "lista_mae", label: "Lista-Mãe", columns: [["cod_item", "Código"], ["descricao_oficial", "Descrição"], ["un", "Unidade"], ["valor_unitario", "Valor unitário"], ["modelos_aplicaveis", "Modelos aplicáveis"]] },
  { key: "modelos", label: "Modelos", columns: [["codigo", "Código"], ["nome", "Modelo"], ["familia", "Família"], ["area_util_m2", "Área útil (m²)"]] },
  { key: "kits", label: "Kits", columns: [["codigo", "Código"], ["nome", "Kit"], ["descricao", "Descrição"], ["versao", "Versão"]] },
];
type Row = Record<string, unknown>;
function value(raw: unknown, key: string) {
  if (raw == null || raw === "") return "—";
  if (key === "valor_unitario" && Number.isFinite(Number(raw))) return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(Number(raw));
  return typeof raw === "object" ? JSON.stringify(raw) : String(raw);
}

export function EloOperationalData({ accessToken }: { accessToken: string }) {
  const [table, setTable] = useState(tables[0]);
  const [rows, setRows] = useState<Row[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [revision, setRevision] = useState(0);
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true); setError(null); setRows([]);
    async function load() {
      try {
        const baseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim();
        if (!baseUrl) throw new Error("Consulta não configurada. Contate o administrador.");
        const response = await fetch(`${baseUrl}/functions/v1/elo-data-gateway`, {
          method: "POST", cache: "no-store", signal: controller.signal,
          headers: { Authorization: `Bearer ${accessToken}`, "Content-Type": "application/json" },
          body: JSON.stringify({ operation: "read", table: table.key, limit: 500, repository: "salvbruno6-hue/Cognitico_IA-corporative" }),
        });
        if (response.status === 401 || response.status === 403) throw new Error("Seu acesso não permite esta consulta. Verifique as permissões com o administrador.");
        const payload = await response.json();
        if (!response.ok || payload?.ok !== true || !Array.isArray(payload.data) || !payload.data.every((row: unknown) => row !== null && typeof row === "object" && !Array.isArray(row))) throw new Error("Não foi possível consultar os dados. Tente atualizar novamente.");
        if (!controller.signal.aborted) setRows(payload.data);
      } catch (reason) { if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : "Não foi possível consultar os dados."); }
      finally { if (!controller.signal.aborted) setLoading(false); }
    }
    void load();
    return () => controller.abort();
  }, [accessToken, table, revision]);
  const filtered = rows.filter(row => table.columns.some(([key]) => value(row[key], key).toLocaleLowerCase("pt-BR").includes(search.toLocaleLowerCase("pt-BR"))));
  return <section aria-labelledby="data-title">
    <h2 id="data-title" className="text-2xl font-semibold">Base de trabalho</h2>
    <p className="mt-2 text-sm text-slate-600">Cadastros compartilhados para apoiar orçamento e planejamento.</p>
    <nav aria-label="Cadastros" className="mt-5 flex flex-wrap gap-2">{tables.map(item => <button key={item.key} type="button" aria-pressed={table.key === item.key} onClick={() => { setTable(item); setSearch(""); }} className={`rounded-lg px-4 py-2 text-sm focus-visible:outline-2 focus-visible:outline-offset-2 ${table.key === item.key ? "bg-slate-900 font-semibold text-white" : "border border-slate-300 hover:bg-slate-100"}`}>{item.label}</button>)}</nav>
    <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between"><label className="text-sm font-medium">Buscar em {table.label}<input type="search" value={search} onChange={event => setSearch(event.target.value)} disabled={loading || !!error} className="mt-1 block w-full rounded-lg border border-slate-300 bg-[var(--elo-panel)] px-3 py-2 sm:w-80 focus-visible:outline-2 focus-visible:outline-offset-2" /></label><button type="button" disabled={loading} onClick={() => setRevision(current => current + 1)} className="rounded-lg border border-slate-300 px-4 py-2 text-sm hover:bg-slate-100 disabled:opacity-50 focus-visible:outline-2 focus-visible:outline-offset-2">Atualizar dados</button></div>
    <div className="mt-4" aria-live="polite">{loading ? <p className="py-8 text-sm text-slate-600">Consultando {table.label}…</p> : error ? <p role="alert" className="py-6 text-sm text-red-700">{error}</p> : <>
      <p className="mb-3 text-sm text-slate-600">{filtered.length} de {rows.length} registros carregados{rows.length === 500 ? " · limite de 500 registros; a consulta pode estar incompleta" : ""}.</p>
      {filtered.length === 0 ? <p className="py-6 text-sm text-slate-600">{search ? "Nenhum registro corresponde à busca." : "Nenhum registro disponível para esta consulta."}</p> : <div className="max-h-[32rem] overflow-auto rounded-xl border border-slate-200" tabIndex={0} role="region" aria-label={`Registros de ${table.label}`}><table className="w-full text-left text-sm"><caption className="sr-only">{table.label} — dados consultados no ELO</caption><thead className="sticky top-0 bg-[var(--elo-panel)]"><tr>{table.columns.map(([key, label]) => <th scope="col" key={key} className="whitespace-nowrap border-b border-slate-200 px-4 py-3 font-semibold">{label}</th>)}</tr></thead><tbody>{filtered.map((row, index) => <tr key={String(row.id ?? index)} className="border-b border-slate-200 last:border-0 hover:bg-slate-100">{table.columns.map(([key]) => <td key={key} className="min-w-24 px-4 py-3 align-top tabular-nums">{value(row[key], key)}</td>)}</tr>)}</tbody></table></div>}
      <p className="mt-3 text-xs text-slate-600">Fonte: {table.label}. Consulta sujeita às permissões da sua sessão.</p>
    </>}</div>
  </section>;
}
