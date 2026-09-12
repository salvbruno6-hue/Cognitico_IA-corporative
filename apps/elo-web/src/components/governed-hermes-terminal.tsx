"use client";

import { useMemo, useState } from "react";
import type { CognitiveResponse } from "@/lib/elo-cognitive";

type Props = { accessToken: string; domain?: string };

type HistoryEntry = {
  input: string;
  output: string;
  status: "ok" | "error";
};

const CAPABILITIES = [
  { name: "terminal + process", mode: "execution", governance: "requires explicit mission" },
  { name: "files + patch", mode: "workspace", governance: "bounded by mission" },
  { name: "web search/extract", mode: "research", governance: "provider/capability contract" },
  { name: "browser automation", mode: "browser", governance: "provider/capability contract" },
  { name: "Skills", mode: "procedural", governance: "candidate/approval gate" },
  { name: "MCP", mode: "integration", governance: "server/tool allowlist" },
  { name: "delegate / execute_code", mode: "orchestration", governance: "bounded execution" },
  { name: "cron automation", mode: "automation", governance: "scheduled mission" },
  { name: "memory/session search", mode: "recall", governance: "ELO policy" },
  { name: "Vercel Sandbox", mode: "runtime", governance: "isolated runtime" },
];

const HELP = [
  "/help — mostra os comandos deste terminal",
  "/capabilities — mostra a varredura das capacidades Hermes identificadas",
  "/status — mostra o estado do terminal governado",
  "/probe — executa o primeiro runtime_probe real permitido pelo ELO",
  "/clear — limpa o histórico visual",
];

export function GovernedHermesTerminal({ accessToken, domain = "planejamento" }: Props) {
  const [command, setCommand] = useState("");
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [busy, setBusy] = useState(false);

  const status = useMemo(
    () => ({
      browserBoundary: "ELO /api/cognitive",
      authority: "ELO Cognitive",
      connector: "Symbiont",
      runtime: "Hermes",
      mission: "runtime_probe",
      mutation: "blocked",
    }),
    [],
  );

  async function execute(raw: string) {
    const input = raw.trim();
    if (!input || busy) return;

    if (input === "/clear") {
      setHistory([]);
      setCommand("");
      return;
    }

    if (input === "/help") {
      setHistory((items) => [...items, { input, output: HELP.join("\n"), status: "ok" }]);
      setCommand("");
      return;
    }

    if (input === "/capabilities") {
      const output = CAPABILITIES.map((item) => `${item.name} · ${item.mode} · ${item.governance}`).join("\n");
      setHistory((items) => [...items, { input, output, status: "ok" }]);
      setCommand("");
      return;
    }

    if (input === "/status") {
      const output = Object.entries(status).map(([key, value]) => `${key}: ${value}`).join("\n");
      setHistory((items) => [...items, { input, output, status: "ok" }]);
      setCommand("");
      return;
    }

    const isProbe = input === "/probe" || input === "hermes probe" || input === "/hermes probe";
    if (!isProbe) {
      setHistory((items) => [...items, { input, output: "Comando ainda não autorizado. Use /help. O terminal não executa comandos Hermes arbitrários; o ELO primeiro autoriza a missão e a capacidade.", status: "error" }]);
      setCommand("");
      return;
    }

    setBusy(true);
    try {
      const response = await fetch("/api/cognitive", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        cache: "no-store",
        body: JSON.stringify({
          message: "Executar runtime_probe do Hermes sob governança do ELO.",
          tenant_id: process.env.NEXT_PUBLIC_ELO_TENANT_ID?.trim() || "multiteiner",
          domain,
          context: {
            source: "elo-governed-hermes-terminal",
            terminal_command: input,
            hermes_mission: {
              mission_class: "runtime_probe",
              authorized_capabilities: ["hermes:runtime_probe"],
            },
          },
        }),
      });
      const payload = (await response.json().catch(() => null)) as CognitiveResponse | { message?: string } | null;
      if (!response.ok) throw new Error(typeof payload?.message === "string" ? payload.message : "O ELO bloqueou a missão Hermes.");
      const result = payload as CognitiveResponse;
      const evidence = result.provenance?.evidence_refs?.length ?? 0;
      const hermesStatus = typeof result.response?.status === "string" ? result.response.status : "retorno recebido";
      setHistory((items) => [
        ...items,
        {
          input,
          output: `ELO autorizou a missão.\nprovider: ${result.provenance?.provider ?? "elo-hermes-via-symbiont"}\nstatus: ${hermesStatus}\nevidence_refs: ${evidence}\nvalidation: ${result.provenance?.validation_status ?? "não informado"}`,
          status: "ok",
        },
      ]);
    } catch (error) {
      setHistory((items) => [...items, { input, output: error instanceof Error ? error.message : "Falha na missão Hermes.", status: "error" }]);
    } finally {
      setBusy(false);
      setCommand("");
    }
  }

  return (
    <section className="overflow-hidden rounded-3xl border border-slate-800 bg-slate-950 text-slate-100 shadow-xl" aria-label="Terminal Hermes governado pelo ELO">
      <header className="flex flex-col gap-3 border-b border-white/10 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">ELO / Terminal Governado</div>
          <h2 className="mt-1 text-lg font-semibold">Entrada operacional Hermes</h2>
        </div>
        <div className="flex flex-wrap gap-2 text-[11px]">
          <span className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-3 py-1 text-emerald-300">ELO authority</span>
          <span className="rounded-full border border-sky-400/30 bg-sky-400/10 px-3 py-1 text-sky-300">Symbiont connector</span>
          <span className="rounded-full border border-violet-400/30 bg-violet-400/10 px-3 py-1 text-violet-300">Hermes runtime</span>
        </div>
      </header>

      <div className="grid lg:grid-cols-[1.6fr_0.8fr]">
        <div className="min-h-[420px] p-4 sm:p-5">
          <div className="mb-4 rounded-xl border border-white/10 bg-black/20 p-3 font-mono text-xs text-slate-400">
            <div>ELO terminal · comandos limitados por contrato</div>
            <div className="mt-1 text-slate-500">/help · /capabilities · /status · /probe · /clear</div>
          </div>

          <div className="min-h-[280px] space-y-3 font-mono text-sm">
            {history.length === 0 && (
              <div className="rounded-xl border border-dashed border-white/10 p-5 text-slate-500">
                Nenhuma execução registrada nesta sessão. Use <span className="text-slate-300">/probe</span> para o primeiro teste real governado.
              </div>
            )}
            {history.map((entry, index) => (
              <div key={`${entry.input}-${index}`} className="rounded-xl border border-white/10 bg-white/[0.03] p-4">
                <div className="text-slate-400"><span className="text-emerald-400">$</span> {entry.input}</div>
                <pre className={`mt-2 whitespace-pre-wrap text-xs leading-5 ${entry.status === "error" ? "text-rose-300" : "text-slate-300"}`}>{entry.output}</pre>
              </div>
            ))}
          </div>

          <form
            className="mt-4 flex gap-2"
            onSubmit={(event) => {
              event.preventDefault();
              void execute(command);
            }}
          >
            <label htmlFor="hermes-command" className="sr-only">Comando Hermes governado</label>
            <span className="grid w-9 shrink-0 place-items-center rounded-xl border border-white/10 bg-black/20 font-mono text-emerald-400">$</span>
            <input
              id="hermes-command"
              value={command}
              onChange={(event) => setCommand(event.target.value.slice(0, 300))}
              disabled={busy}
              autoComplete="off"
              spellCheck={false}
              placeholder="/probe"
              className="min-w-0 flex-1 rounded-xl border border-white/10 bg-black/30 px-4 py-3 font-mono text-sm text-white outline-none placeholder:text-slate-600 focus:border-sky-400/50 focus:ring-2 focus:ring-sky-400/20 disabled:opacity-50"
            />
            <button type="submit" disabled={busy || !command.trim()} className="rounded-xl bg-white px-4 py-3 text-sm font-semibold text-slate-950 disabled:cursor-not-allowed disabled:opacity-40">
              {busy ? "Executando…" : "Enviar"}
            </button>
          </form>
        </div>

        <aside className="border-t border-white/10 bg-white/[0.025] p-5 lg:border-l lg:border-t-0">
          <div className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Boundary</div>
          <div className="mt-3 space-y-3 text-xs">
            {Object.entries(status).map(([key, value]) => (
              <div key={key} className="flex items-start justify-between gap-4 border-b border-white/5 pb-3">
                <span className="text-slate-500">{key}</span>
                <span className="text-right text-slate-300">{value}</span>
              </div>
            ))}
          </div>
          <div className="mt-6 rounded-xl border border-amber-400/20 bg-amber-400/5 p-3 text-xs leading-5 text-amber-200/80">
            O terminal não recebe endpoint, token ou comando bruto do Hermes. Toda execução passa pelo ELO Cognitive e pelo Symbiont.
          </div>
        </aside>
      </div>
    </section>
  );
}
